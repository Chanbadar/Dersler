import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg

APP_VERSION = "1.1"

app = Flask(__name__)

# Secret key configuration
app_secret_file = os.environ.get("APP_SECRET_FILE", "/run/secrets/app_secret")
if Path(app_secret_file).exists():
    with open(app_secret_file, "r") as f:
        app.secret_key = f.read().strip()
else:
    app.secret_key = os.environ.get("APP_SECRET", "default-dev-secret-key")

# Database configuration
db_host = os.environ.get("DB_HOST", "db")
db_port = int(os.environ.get("DB_PORT", "5432"))
db_name = os.environ.get("DB_NAME", "dersnotlari")
db_user = os.environ.get("DB_USER", "dersuser")

db_password_file = os.environ.get("DB_PASSWORD_FILE", "/run/secrets/db_password")
if Path(db_password_file).exists():
    with open(db_password_file, "r") as f:
        db_password = f.read().strip()
else:
    db_password = os.environ.get("DB_PASSWORD", "postgrespassword")

def get_db_connection():
    return psycopg.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password,
        connect_timeout=3
    )

def init_db():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS dersnotlari (
                        id SERIAL PRIMARY KEY,
                        numara VARCHAR(50) NOT NULL,
                        baslik VARCHAR(200) NOT NULL,
                        aciklama TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                conn.commit()
    except Exception as e:
        print(f"Database init warning (might be offline yet): {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        numara = request.form.get("numara", "").strip()
        baslik = request.form.get("baslik", "").strip()
        aciklama = request.form.get("aciklama", "").strip()
        if numara and baslik:
            try:
                with get_db_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            "INSERT INTO dersnotlari (numara, baslik, aciklama) VALUES (%s, %s, %s)",
                            (numara, baslik, aciklama)
                        )
                        conn.commit()
            except Exception as e:
                return f"Veritabanı kayıt hatası: {e}", 500
        return redirect(url_for("index"))

    # GET
    kayitlar = []
    db_error = None
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT numara, baslik, aciklama, created_at FROM dersnotlari ORDER BY id ASC")
                kayitlar = cur.fetchall()
    except Exception as e:
        db_error = str(e)

    return render_template("index.html", kayitlar=kayitlar, version=APP_VERSION, db_error=db_error)

@app.route("/health/live")
def health_live():
    return jsonify({"status": "ok"}), 200

@app.route("/health/ready")
def health_ready():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
        return jsonify({"status": "ready", "version": APP_VERSION}), 200
    except Exception as e:
        return jsonify({"status": "unready", "error": str(e), "version": APP_VERSION}), 503

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000)
