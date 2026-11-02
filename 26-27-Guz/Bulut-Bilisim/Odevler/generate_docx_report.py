import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_report():
    doc = docx.Document()

    # Page Margins: Standard 1 inch (2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

    # Palette
    COLOR_PRIMARY = RGBColor(27, 54, 93)     # Deep Navy Blue
    COLOR_SECONDARY = RGBColor(46, 91, 136)  # Slate Blue
    COLOR_ACCENT = RGBColor(49, 130, 206)    # Cerulean Blue
    COLOR_TEXT = RGBColor(45, 55, 72)        # Charcoal Text
    COLOR_MUTED = RGBColor(113, 128, 150)    # Muted Gray
    COLOR_CODE_BG = "F7FAFC"
    COLOR_BORDER = "CBD5E0"
    COLOR_TABLE_HEADER = "1B365D"
    COLOR_ROW_ALT = "F7FAFC"

    # Helper: Set Cell Shading
    def set_cell_shading(cell, color_hex):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    # Helper: Set Cell Borders
    def set_cell_borders(cell, top="none", bottom="none", left="none", right="none", 
                         color="CBD5E0", sz="4"):
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="{top}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="{left}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="{bottom}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:right w:val="{right}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)

    # Helper: Cell Margins (padding)
    def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(
            f'<w:tcMar {nsdecls("w")}>'
            f'<w:top w:w="{top}" w:type="dxa"/>'
            f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
            f'<w:left w:w="{left}" w:type="dxa"/>'
            f'<w:right w:w="{right}" w:type="dxa"/>'
            f'</w:tcMar>'
        )
        tcPr.append(tcMar)

    # Helper: Add Heading 1
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    # Helper: Add Heading 2
    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = COLOR_SECONDARY
        return p

    # Helper: Add Heading 3
    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_ACCENT
        return p

    # Helper: Add Body Paragraph
    def add_p(text, bold_prefix=None, italic_prefix=None, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            run_b = p.add_run(bold_prefix)
            run_b.font.name = "Calibri"
            run_b.font.size = Pt(10.5)
            run_b.font.bold = True
            run_b.font.color.rgb = COLOR_TEXT
        if italic_prefix:
            run_i = p.add_run(italic_prefix)
            run_i.font.name = "Calibri"
            run_i.font.size = Pt(10.5)
            run_i.font.italic = True
            run_i.font.color.rgb = COLOR_TEXT
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10.5)
        run.font.color.rgb = COLOR_TEXT
        return p

    # Helper: Add Bullet Item
    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            run_b = p.add_run(bold_prefix)
            run_b.font.name = "Calibri"
            run_b.font.size = Pt(10.5)
            run_b.font.bold = True
            run_b.font.color.rgb = COLOR_TEXT
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10.5)
        run.font.color.rgb = COLOR_TEXT
        return p

    # Helper: Add Callout Box
    def add_callout(title, text, callout_type="NOTE"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        bg = "EBF8FF" if callout_type == "NOTE" else "FEFCBF" if callout_type == "WARN" else "F0FFF4"
        border_col = "3182CE" if callout_type == "NOTE" else "D69E2E" if callout_type == "WARN" else "38A169"
        set_cell_shading(cell, bg)
        set_cell_borders(cell, left="single", sz="24", color=border_col)
        set_cell_margins(cell, top=140, bottom=140, left=200, right=180)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        run_t = p.add_run(f"[{callout_type}] {title}\n")
        run_t.font.name = "Calibri"
        run_t.font.size = Pt(10.5)
        run_t.font.bold = True
        run_t.font.color.rgb = COLOR_PRIMARY
        
        run_b = p.add_run(text)
        run_b.font.name = "Calibri"
        run_b.font.size = Pt(10)
        run_b.font.color.rgb = COLOR_TEXT
        
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(4)

    # Helper: Add Terminal / Code Block
    def add_code_block(title, code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_shading(cell, "F8F9FA")
        set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color="E2E8F0", sz="6")
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        if title:
            run_h = p.add_run(f"Terminal / Kod: {title}\n")
            run_h.font.name = "Consolas"
            run_h.font.size = Pt(9)
            run_h.font.bold = True
            run_h.font.color.rgb = COLOR_SECONDARY
        
        run_c = p.add_run(code_text.strip())
        run_c.font.name = "Consolas"
        run_c.font.size = Pt(8.5)
        run_c.font.color.rgb = RGBColor(26, 32, 44)
        
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(4)

    # Helper: Add Formatted Table
    def add_styled_table(headers, rows_data, col_widths=None):
        tbl = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Header Row
        hdr_cells = tbl.rows[0].cells
        for i, header_text in enumerate(headers):
            cell = hdr_cells[i]
            if col_widths and i < len(col_widths):
                cell.width = Inches(col_widths[i])
            set_cell_shading(cell, COLOR_TABLE_HEADER)
            set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color=COLOR_BORDER, sz="6")
            set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(header_text)
            run.font.name = "Calibri"
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            
        # Data Rows
        for r_idx, row_items in enumerate(rows_data):
            row_cells = tbl.rows[r_idx + 1].cells
            bg_color = COLOR_ROW_ALT if (r_idx % 2 == 1) else "FFFFFF"
            for c_idx, val in enumerate(row_items):
                cell = row_cells[c_idx]
                if col_widths and c_idx < len(col_widths):
                    cell.width = Inches(col_widths[c_idx])
                set_cell_shading(cell, bg_color)
                set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color=COLOR_BORDER, sz="4")
                set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_after = Pt(0)
                run = p.add_run(str(val))
                run.font.name = "Calibri"
                run.font.size = Pt(9)
                run.font.color.rgb = COLOR_TEXT
                
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(6)
        return tbl

    # ==================== COVER PAGE ====================
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(36)
    title_p.paragraph_format.space_after = Pt(12)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_t0 = title_p.add_run("T.C.\nBİLGİSAYAR MÜHENDİSLİĞİ BÖLÜMÜ\n")
    run_t0.font.name = "Calibri"
    run_t0.font.size = Pt(14)
    run_t0.font.bold = True
    run_t0.font.color.rgb = COLOR_SECONDARY

    run_t1 = title_p.add_run("BULUT BİLİŞİM DERSİ (2026-2027 GÜZ YARIYILI)\n")
    run_t1.font.name = "Calibri"
    run_t1.font.size = Pt(16)
    run_t1.font.bold = True
    run_t1.font.color.rgb = COLOR_PRIMARY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(18)
    sub_p.paragraph_format.space_after = Pt(36)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = sub_p.add_run("HAFTA 6 UYGULAMA RAPORU:\nKUBERNETES İLE KONTEYNER ORKESTRASYONU, MİKROSERVİS DAĞITIMI, KALICI DEPOLAMA, SAĞLIK KONTROLLERİ, ÖLÇEKLEME VE BULUTA GEÇİŞ DEĞERLENDİRMESİ")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(18)
    run_sub.font.bold = True
    run_sub.font.color.rgb = COLOR_ACCENT

    # Cover Meta Box
    meta_tbl = doc.add_table(rows=5, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_info = [
        ("Öğrenci Adı Soyadı:", "Arda Kumartaşlıoğlu"),
        ("Öğrenci Numarası:", "16008122022"),
        ("Ders Adı:", "Bulut Bilişim"),
        ("Çalışma Haftası / Konusu:", "Hafta 6 - Kubernetes ve Konteyner Orkestrasyonu"),
        ("Teslim Tarihi:", "Kasım 2026")
    ]
    for idx, (label, val) in enumerate(meta_info):
        c0, c1 = meta_tbl.rows[idx].cells
        c0.width = Inches(2.2)
        c1.width = Inches(4.0)
        set_cell_shading(c0, "F0F4F8")
        set_cell_shading(c1, "FFFFFF")
        set_cell_borders(c0, top="single", bottom="single", left="single", right="single", color=COLOR_BORDER)
        set_cell_borders(c1, top="single", bottom="single", left="single", right="single", color=COLOR_BORDER)
        set_cell_margins(c0, top=100, bottom=100, left=140, right=140)
        set_cell_margins(c1, top=100, bottom=100, left=140, right=140)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(label)
        r0.font.name = "Calibri"
        r0.font.size = Pt(10.5)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_PRIMARY
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(val)
        r1.font.name = "Calibri"
        r1.font.size = Pt(10.5)
        r1.font.bold = (idx < 2)
        r1.font.color.rgb = COLOR_TEXT

    doc.add_page_break()

    # ==================== SECTION 1 ====================
    add_h1("1. GİRİŞ VE ÇALIŞMANIN AMACI")
    add_p(
        "Modern bulut bilişim ekosisteminde konteynerleştirme teknolojileri (Docker vb.), uygulamaların bağımlılıklarıyla birlikte "
        "yalıtılmış ve taşınabilir bir biçimde paketlenmesini sağlamıştır. Ancak, yüzlerce mikroservisten oluşan ve dinamik yük altında çalışan "
        "büyük ölçekli sistemlerde münferit konteynerlerin manuel olarak yönetilmesi, düğüm arızalarının karşılanması, ağ yönlendirmesi, "
        "yük dengeleme ve veri sürekliliğinin temini insan kapasitesini aşmaktadır. İşte bu noktada konteyner orkestrasyonu devreye girmektedir."
    )
    add_p(
        "Kubernetes, konteynerize edilmiş iş yüklerinin otomatik dağıtımı, ölçeklenmesi, yük dengelemesi ve kendi kendini iyileştirmesi "
        "(self-healing) için tasarlanmış açık kaynaklı, endüstri standardı bir orkestrasyon platformudur. Kubernetes mimarisinin merkezinde "
        "bildirimsel (declarative) yönetim ilkesi yer alır. Bu ilkeye göre sistem yöneticisi veya yazılım mühendisi 'ne yapılması gerektiğini' "
        "adım adım komutlarla emretmek (imperative yaklaşım) yerine; sistemin 'hangi nihai durumda bulunması gerektiğini' (desired state) "
        "YAML manifestoları aracılığıyla beyan eder. Kubernetes kontrol düzlemi (control plane) içerisindeki kontrol döngüleri (controller loops), "
        "kümenin anlık durumunu (actual state) sürekli gözlemleyerek bildirilen durum ile gerçek durum arasındaki farkı uzlaştırır (reconciliation)."
    )
    add_p(
        "Bu rapor; Hafta 6 kapsamında gerçekleştirilen yerel Kubernetes kümesi hazırlığını, 'Ders Notları Kayıt Uygulaması'nın mikroservis "
        "mimarisine uygun olarak Kubernetes nesneleriyle (Deployment, Service, ConfigMap, Secret, PersistentVolumeClaim) dağıtılmasını, "
        "veri kalıcılığının doğrulanmasını, kontrollü kesinti deneyleriyle sağlık kontrollerinin (readiness ve liveness probes) davranışlarının "
        "incelenmesini, elle yatay ölçeklemeyi, kademeli güncelleme (rolling update) ve geri dönüş (rollout undo) mekanizmalarını ve son olarak "
        "yönetilen bulut ortamlarına (AWS EKS, Azure AKS, Google Cloud GKE) geçiş dinamiklerini kapsamlı bir biçimde belgelemektedir."
    )

    add_callout(
        "Temel Hedef ve Kriterler",
        "Bu çalışmanın başarı kriteri, Pod'ların yalnızca 'Running' durumunda görünmesi değildir. Uygulamanın uçtan uca çalışabilmesi, "
        "bileşenlerin iç ağ üzerinden iletişim kurabilmesi, kalıcı depolama sayesinde verilerin Pod silinmelerinden etkilenmemesi, "
        "sağlık denetimlerinin hata durumlarında trafiği doğru yönetmesi ve güncelleme/geri dönüş adımlarının veri kaybı olmaksızın "
        "gerçekleştirilmesi deneysel kanıtlarla doğrulanmıştır.",
        "NOTE"
    )

    # ==================== SECTION 2 ====================
    add_h1("2. ÇALIŞMA ORTAMI VE YEREL KÜME HAZIRLIĞI")
    add_p(
        "Kubernetes çalışmalarında yerel geliştirme ve test ortamları için Docker Desktop (kubeadm/kind) ve Minikube iki ana alternatif olarak "
        "öne çıkmaktadır. Bu çalışmada kılavuzun (Ek 1) önerdiği ilkeler doğrultusunda, izole ve tekrarlanabilir bir küme ortamı sunan "
        "Minikube platformu tercih edilmiştir. Minikube üzerinde 'hafta6' adında özel bir profil tanımlanmış, Linux çekirdeğinin yerel KVM2 "
        "(Kernel-based Virtual Machine) hipervizör sürücüsü ve modern 'containerd (v2.3.4)' konteyner çalışma zamanı kullanılarak tek düğümlü "
        "bir Kubernetes v1.37.0 kümesi ayağa kaldırılmıştır."
    )

    add_h2("2.1 Küme Bileşenleri ve Düğüm Durumu")
    add_p(
        "Kümenin başlatılmasının ardından 'kubectl' komut satırı aracı küme bağlamına (context) yönlendirilmiş ve küme düğümünün sağlık durumu "
        "denetlenmiştir. 'kubectl get nodes' komutu ile kontrol düzlemi ve işçi rollerini üstlenen 'hafta6' düğümünün 'Ready' durumunda "
        "olduğu teyit edilmiştir:"
    )

    add_code_block("Düğüm ve Bağlam Doğrulaması",
"""$ kubectl config current-context
hafta6

$ kubectl get nodes -o wide
NAME     STATUS   ROLES           AGE   VERSION   INTERNAL-IP       OS-IMAGE             KERNEL-VERSION     CONTAINER-RUNTIME
hafta6   Ready    control-plane   2m    v1.37.0   192.168.122.187   Buildroot 2023.02.9  6.6.152            containerd://2.3.4""")

    add_h2("2.2 Depolama Sınıfı (StorageClass) ve Ad Alanı (Namespace) Hazırlığı")
    add_p(
        "Kalıcı verilerin (stateful data) yönetilebilmesi için kümede dinamik depolama sağlayıcısının bulunması zorunludur. Minikube ortamında "
        "varsayılan olarak gelen 'standard (k8s.io/minikube-hostpath)' depolama sınıfı kontrol edilmiştir. Bu depolama sınıfı, kalıcı birim talepleri "
        "(PVC) oluşturulduğunda ana makinedeki bir dizini otomatik olarak PersistentVolume (PV) olarak bağlamaktadır. Ancak varsayılan "
        "Reclaim Policy (Geri Kazanım Politikası) değerinin 'Delete' olduğuna dikkat edilmelidir."
    )
    add_p(
        "Farklı projelerin ve sistem kaynaklarının birbirini etkilememesi için kılavuz gereği 'hafta6' adında bağımsız bir ad alanı (Namespace) "
        "oluşturulmuş ve tüm nesneler bu mantıksal sınır içerisinde konumlandırılmıştır:"
    )

    add_code_block("StorageClass ve Namespace Doğrulaması",
"""$ kubectl get storageclass
NAME                 PROVISIONER                RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
standard (default)   k8s.io/minikube-hostpath   Delete          Immediate           false                  2m

$ kubectl create namespace hafta6
namespace/hafta6 created

$ kubectl get namespace hafta6
NAME     STATUS   AGE
hafta6   Active   15s""")

    # ==================== SECTION 3 ====================
    add_h1("3. UYGULAMA MİMARİSİ VE KUBERNETES NESNELERİ")
    add_p(
        "Ders kapsamında kullanılan 'Ders Notları Kayıt Uygulaması', iki ana katmandan oluşan tipik bir mikroservis mimarisidir:"
    )
    add_bullet(" Kullanıcı isteklerini karşılayan, web formunu sunan, notları listeleyen ve REST sağlık uç noktalarını (/health/ready, /health/live) barındıran Flask tabanlı web servisi.", "Web Uygulama Katmanı:")
    add_bullet(" Ders notlarını ilişkisel tabloda (dersnotlari) kalıcı olarak saklayan, ACID güvencesine sahip PostgreSQL 16 veritabanı servisi.", "Veritabanı Katmanı:")

    add_p(
        "Aşağıdaki tabloda, bu iki katmanın Kubernetes üzerinde bildirimsel olarak yönetilmesi için tanımlanan temel nesneler ve görevleri özetlenmiştir:"
    )

    add_styled_table(
        ["Kubernetes Nesnesi", "Nesne Adı", "Türü / Stratejisi", "Görevi ve Sağladığı Fonksiyon"],
        [
            ["ConfigMap", "app-config", "Yapılandırma", "Hassas olmayan DB_HOST, DB_PORT, DB_NAME, DB_USER ve COOKIE_SECURE ayarlarını tutar."],
            ["Secret", "app-secrets", "Opaque (Gizli Bilgi)", "Veritabanı parolası (db_password) ve Flask oturum anahtarını (app_secret) salt-okunur dosyalar olarak saklar."],
            ["PersistentVolumeClaim", "db-data", "1Gi / ReadWriteOnce", "PostgreSQL için varsayılan StorageClass üzerinden kalıcı disk alanı tahsis eder."],
            ["Deployment (DB)", "db", "Recreate (1 kopya)", "PostgreSQL 16 motorunu çalıştırır, aynı anda iki Pod'un diske yazmasını engelleyen Recreate stratejisini kullanır."],
            ["Deployment (Web)", "web", "RollingUpdate (1-2 kopya)", "Web uygulamasını çalıştırır, sıfır kesintili aşamalı güncelleme (maxUnavailable: 0, maxSurge: 1) uygular."],
            ["Service (DB)", "db", "ClusterIP (Port 5432)", "Veritabanını küme içi DNS'e açar (db:5432), internete doğrudan maruz kalmasını engeller."],
            ["Service (Web)", "web", "ClusterIP (Port 8000)", "Web Pod'larına yük dengeli erişim sunar ve EndpointSlice nesneleriyle sağlıklı hedefleri yönetir."],
            ["Pod (Kontrol)", "check", "Standalone Pod", "Küme içerisinden DNS çözümlemesini ve iç servis iletişimini doğrulamak için kullanılan test Pod'u."]
        ],
        [1.5, 1.1, 1.4, 2.5]
    )

    add_h2("3.1 Güvenlik ve Gizli Bilgilerin Ayrımı (Secret vs ConfigMap)")
    add_p(
        "On İki Faktörlü Uygulama (The Twelve-Factor App) metodolojisi uyarınca, yapılandırma ve kimlik bilgileri kaynak koddan kesinlikle "
        "ayrılmalıdır. Bu ilke gereğince gizli olmayan ortam değişkenleri 'ConfigMap' nesnesinde saklanırken; veritabanı erişim şifresi ve "
        "kullanıcı oturumlarını imzalayan 'APP_SECRET' anahtarı 'Secret' nesnesi üzerinden sisteme dahil edilmiştir."
    )
    add_callout(
        "Güvenlik Uyarısı: Base64 Şifreleme Değildir",
        "Kubernetes Secret nesnelerinin YAML çıktısında (kubectl get secret -o yaml) değerler Base64 formatında kodlanmış olarak görünür. "
        "Base64 bir şifreleme (encryption) algoritması değil, yalnızca ikili veriyi metne dönüştüren bir kodlama (encoding) yöntemidir. "
        "Herhangi biri bu metni saniyeler içinde çözebilir. Bu nedenle Secret nesnelerinin içeriği asla doğrudan raporlara veya ekran "
        "görüntülerine eklenmemelidir. Çalışmamızda şifreler ortam değişkeni yerine Pod içine '/run/secrets/' dizinine salt-okunur (readOnly: true) "
        "volume olarak bağlanmış; böylece işlem dökümlerinde (process dumps) veya çevre değişkeni loglarında görünmesi engellenmiştir.",
        "WARN"
    )

    add_code_block("Secret Nesnesinin Dosyalardan Oluşturulması",
"""$ kubectl create secret generic app-secrets -n hafta6 \\
    --from-file=db_password=./secrets/db_password.txt \\
    --from-file=app_secret=./secrets/app_secret.txt
secret/app-secrets created

$ kubectl get secret app-secrets -n hafta6
NAME          TYPE     DATA   AGE
app-secrets   Opaque   2      15s""")

    # ==================== SECTION 4 ====================
    add_h1("4. KONTROLLÜ DENEYLER VE DOĞRULAMA KANITLARI")
    add_p(
        "Kılavuzda (Ek 2) tanımlanan tüm deneyler adım adım uygulanmış, terminal çıktıları ve nesne durumları anlık olarak kayıt altına alınmıştır. "
        "Her deneyin öncesi, deney esnası ve deney sonrası durumları aşağıda ayrıntılı teknik değerlendirmelerle sunulmuştur."
    )

    # Deney 1
    add_h2("4.1 Deney 1: Uygulamanın Dağıtılması ve İlk Doğrulama (Ek 2 Bölüm 7)")
    add_p(
        "Amaç: Bildirimsel YAML manifestolarının sözdizimi doğruluğunu sınamak (dry-run), nesneleri hafta6 ad alanında oluşturmak, "
        "Pod'ların READY durumuna geçtiğini teyit etmek, port yönlendirme ile dış erişim sağlamak ve ilk kalıcılık test kayıtlarını oluşturmak."
    )
    add_p(
        "Uygulanan Komutlar ve Süreç: Önce 'kubectl apply --dry-run=client -f ./k8s' ile istemci taraflı doğrulama yapılmış, ardından sırasıyla "
        "ConfigMap, Secret, PVC, DB Deployment, Servisler ve Web Deployment kümeye uygulanmıştır. Rollout kontrolleriyle her iki dağıtımın "
        "tamamlandığı izlenmiştir:"
    )

    add_code_block("Deney 1 Dağıtım Çıktıları",
"""$ kubectl apply --dry-run=client -f ./k8s
configmap/app-config configured (dry run)
persistentvolumeclaim/db-data configured (dry run)
deployment.apps/db created (dry run)
service/db created (dry run)
service/web created (dry run)
deployment.apps/web created (dry run)

$ kubectl apply -f ./k8s/01-config.yaml
$ kubectl apply -f ./k8s/02-pvc.yaml
$ kubectl apply -f ./k8s/03-db.yaml
$ kubectl apply -f ./k8s/04-services.yaml
$ kubectl apply -f ./k8s/05-web.yaml

$ kubectl rollout status deployment/db -n hafta6 --timeout=180s
deployment "db" successfully rolled out

$ kubectl rollout status deployment/web -n hafta6 --timeout=180s
deployment "web" successfully rolled out

$ kubectl get deployments,pods,services,pvc -n hafta6
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/db    1/1     1            1           12s
deployment.apps/web   1/1     1            1           11s

NAME                       READY   STATUS    RESTARTS   AGE
pod/db-77cfdc4ccc-zm7rl    1/1     Running   0          12s
pod/web-58c776859c-785d7   1/1     Running   0          11s

NAME          TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
service/db    ClusterIP   10.111.73.51   <none>        5432/TCP   11s
service/web   ClusterIP   10.109.84.91   <none>        8000/TCP   11s

NAME                            STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
persistentvolumeclaim/db-data   Bound    pvc-fff7d32f-6b0a-478c-9943-f274a6f5ed86   1Gi        RWO            standard       17s""")

    add_p(
        "Dış Erişim ve İlk Test Kayıtları: Web servisi 'ClusterIP' türünde olduğundan küme dışından doğrudan IP ile ulaşılamaz. "
        "Geliştirme ve doğrulama amacıyla geçici port yönlendirme (port-forward) başlatılmıştır:\n"
        "`kubectl port-forward -n hafta6 service/web 8080:8000 --address 127.0.0.1`\n"
        "Ardından 'http://localhost:8080' üzerinden sağlık kontrolü yapılmış ve ilk iki test kaydı (Kalıcılık A ve Kalıcılık B) oluşturulmuştur:"
    )

    add_code_block("Sağlık Sorgusu ve İlk Kayıtların Eklenmesi",
"""$ curl -s http://127.0.0.1:8080/health/ready
{"status":"ready","version":"1.1"}

$ curl -s -X POST http://127.0.0.1:8080/ -d "numara=101&baslik=Kalıcılık A&aciklama=İlk kalıcılık test kaydı"
$ curl -s -X POST http://127.0.0.1:8080/ -d "numara=102&baslik=Kalıcılık B&aciklama=İkinci kalıcılık test kaydı"

$ curl -s http://127.0.0.1:8080/ | grep -A 2 "Kalıcılık"
<td><strong>101</strong></td>
<td>Kalıcılık A</td>
<td>İlk kalıcılık test kaydı</td>
--
<td><strong>102</strong></td>
<td>Kalıcılık B</td>
<td>İkinci kalıcılık test kaydı</td>""")

    add_p(
        "Gözlemlenen Sonuç ve Değerlendirme: Hem veritabanı hem de web bileşenleri 1/1 hazır (READY) duruma geçmiş; kalıcı birim talebi (db-data) "
        "başarıyla 'Bound' statüsüne ulaşmıştır. Web uygulaması /health/ready sorgusuna 200 OK ile 'status=ready, version=1.1' yanıtı vermiş, "
        "veritabanı bağlantısının ve yazma kabiliyetinin eksiksiz çalıştığı doğrulanmıştır."
    )

    # Deney 2
    add_h2("4.2 Deney 2: Service Üzerinden Küme İçi Ağ İletişimi Doğrulaması (Ek 2 Bölüm 8)")
    add_p(
        "Amaç: Port yönlendirme bağımsız olarak, Kubernetes iç ağında DNS tabanlı servis keşfini (Service Discovery) ve "
        "EndpointSlice üzerinden yük yönlendirmesini doğrulamak."
    )
    add_p(
        "Uygulanan Komutlar ve Süreç: Aynı kümede geçici bir 'check' Pod'u ('k8s/06-check.yaml') ayağa kaldırılmış ve bu Pod içerisinden "
        "web servisine 'http://web:8000/health/ready' adresi üzerinden istek gönderilmiştir. Ayrıca web servisinin arkasındaki Pod hedeflerini "
        "tutan EndpointSlice nesnesi sorgulanmıştır:"
    )

    add_code_block("Deney 2 Küme İçi DNS ve EndpointSlice Çıktısı",
"""$ kubectl apply -f ./k8s/06-check.yaml
pod/check created
$ kubectl wait -n hafta6 --for=condition=Ready pod/check --timeout=120s
pod/check condition met

$ kubectl exec -n hafta6 check -- python -c "import urllib.request; print(urllib.request.urlopen('http://web:8000/health/ready', timeout=10).read().decode())"
{"status":"ready","version":"1.1"}

$ kubectl get endpointslices -n hafta6 -l kubernetes.io/service-name=web -o yaml
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  labels:
    kubernetes.io/service-name: web
  name: web-88twv
  namespace: hafta6
endpoints:
- addresses:
  - 10.244.0.4
  conditions:
    ready: true
    serving: true
    terminating: false
  nodeName: hafta6
  targetRef:
    kind: Pod
    name: web-58c776859c-785d7
    namespace: hafta6
    uid: a8e9f175-c9bc-4433-8692-72cd35184073
ports:
- port: 8000
  protocol: TCP""")

    add_p(
        "Gözlemlenen Sonuç ve Değerlendirme: 'check' Pod'u içerisindeki CoreDNS çözücüsü 'web' ismini 'service/web'in sanal ClusterIP adresine "
        "(10.109.84.91) başarıyla çözümlemiş ve kube-proxy bu trafiği EndpointSlice'ta 'ready: true' olarak işaretlenmiş olan 'web-58c776859c-785d7' "
        "(IP: 10.244.0.4) Pod'una iletmiştir. Böylece küme içi mikroservis iletişiminin standart Kubernetes mekanizmalarıyla sorunsuz işlediği "
        "ispatlanmıştır."
    )

    # Deney 3
    add_h2("4.3 Deney 3: Veri Kalıcılığı ve Pod Yenilenme Doğrulaması (Ek 2 Bölüm 9.1)")
    add_p(
        "Amaç: PostgreSQL veritabanı Pod'u silindiğinde veya arızalandığında, verilerin konteynerin geçici (ephemeral) katmanında değil, "
        "PersistentVolume (PV) üzerinde korunduğunu; Deployment denetleyicisinin yeni bir Pod oluşturup aynı birimi bağlayarak verileri "
        "eksiksiz geri sunduğunu kanıtlamak."
    )
    add_p(
        "Uygulanan Komutlar ve Süreç: Mevcut veritabanı Pod'unun adı ve benzersiz sistem kimliği (UID) kaydedilmiş, ardından Pod zorla silinmiştir "
        "(kubectl delete pod -n hafta6 -l app=db). Deployment'ın yeni Pod'u oluşturması beklenmiş, yeni Pod'un UID'si alınmış ve web arayüzünden "
        "kayıtların durumu kontrol edilmiştir:"
    )

    add_code_block("Deney 3 Veritabanı Pod Silinmesi ve Veri Kalıcılığı Çıktısı",
"""# 1. Silme Öncesi Durum
Eski DB Pod: db-77cfdc4ccc-zm7rl (UID: 2e0b5de3-faa6-43fe-ba12-ac6942b7c8a3)
PVC Durumu: db-data | Bound | pvc-fff7d32f-6b0a-478c-9943-f274a6f5ed86 | 1Gi | RWO

# 2. DB Pod'unun Silinmesi ve Yeniden Dağıtılması
$ kubectl delete pod -n hafta6 -l app=db
pod "db-77cfdc4ccc-zm7rl" deleted
$ kubectl rollout status deployment/db -n hafta6 --timeout=180s
deployment "db" successfully rolled out

# 3. Silme Sonrası Durum
Yeni DB Pod: db-77cfdc4ccc-5xcdx (UID: 5ded3e36-7e4d-4007-8614-ba6c4275e779)
PVC Durumu: db-data | Bound | pvc-fff7d32f-6b0a-478c-9943-f274a6f5ed86 | 1Gi | RWO

# 4. Web Arayüzünden Veri Kontrolü
$ curl -s http://127.0.0.1:8080/ | grep -A 2 "Kalıcılık"
<td><strong>101</strong></td>
<td>Kalıcılık A</td>
<td>İlk kalıcılık test kaydı</td>
--
<td><strong>102</strong></td>
<td>Kalıcılık B</td>
<td>İkinci kalıcılık test kaydı</td>""")

    add_p(
        "Gözlemlenen Sonuç ve Değerlendirme: Eski Pod (UID: 2e0b5de3...) silinmiş ve yerine tamamen yeni bir Pod (UID: 5ded3e36...) "
        "oluşturulmuştur. Ancak 'db-data' PVC nesnesi ve arkasındaki 'pvc-fff7d32f...' PV nesnesi hiç değişmeden sabit kalmıştır. "
        "Yeni veritabanı Pod'u ayağa kalktığında bu kalıcı diski '/var/lib/postgresql/data' altına bağlamış ve daha önce eklenmiş olan "
        "101 (Kalıcılık A) ve 102 (Kalıcılık B) kayıtları sıfır veri kaybıyla aynen okunmuştur."
    )

    # Deney 4
    add_h2("4.4 Deney 4: Web Pod'unun Silinmesi ve Self-Healing (Ek 2 Bölüm 9.2)")
    add_p(
        "Amaç: Durumsuz (stateless) web bileşeninin bir Pod'u çöktüğünde veya silindiğinde, Deployment/ReplicaSet kontrol döngüsünün "
        "istenen kopya sayısını (replicas: 1) korumak için otomatik olarak yeni bir Pod üretmesini (Self-Healing) gözlemlemek."
    )
    add_p(
        "Uygulanan Komutlar ve Süreç: Web Pod'unun UID'si alınmış ve 'kubectl delete pod -n hafta6 -l app=web' komutuyla silinmiştir:"
    )

    add_code_block("Deney 4 Web Pod Yenilenmesi Çıktısı",
"""Eski Web Pod: web-58c776859c-785d7 (UID: a8e9f175-c9bc-4433-8692-72cd35184073)
$ kubectl delete pod -n hafta6 -l app=web
pod "web-58c776859c-785d7" deleted
$ kubectl rollout status deployment/web -n hafta6 --timeout=180s
deployment "web" successfully rolled out

Yeni Web Pod: web-58c776859c-66fwm (UID: 72b9967c-ffad-4010-9a70-acb8b8ee54a8)
$ curl -s http://127.0.0.1:8080/health/ready
{"status":"ready","version":"1.1"}""")

    add_p(
        "Gözlemlenen Sonuç ve Değerlendirme: Web Pod'unun silinmesiyle kümedeki hazır web kopya sayısı sıfıra düşmüş; ReplicaSet denetleyicisi "
        "bu farkı tespit ederek milisaniyeler içinde 'web-58c776859c-66fwm' adında yeni bir Pod başlatmıştır. Yeni Pod yapılandırmasını "
        "ConfigMap ve Secret'tan okuyarak hazır duruma geçmiş, port yönlendirme oturumu yenilendiğinde uygulamanın kesintisiz hizmet verdiği görülmüştür."
    )

    # Deney 5
    add_h2("4.5 Deney 5: Sağlık Kontrolleri 1 - Veritabanı Kesintisi ve Readiness Probe (Ek 2 Bölüm 10.1)")
    add_p(
        "Amaç: Bağımlı bir serviste (PostgreSQL) kesinti yaşandığında, Hazır Olma Kontrolünün (Readiness Probe) ve Canlılık Kontrolünün "
        "(Liveness Probe) nasıl farklı davrandığını ve Kubernetes servis trafiğinin nasıl yönetildiğini deneysel olarak kanıtlamak."
    )
    add_p(
        "Uygulanan Komutlar ve Süreç: Veritabanı dağıtımı 'kubectl scale deployment/db -n hafta6 --replicas=0' komutuyla tamamen durdurulmuştur. "
        "Web Pod'unun ve EndpointSlice'ın durumu incelenmiş; ayrıca küme içi 'check' Pod'undan istek gönderilmiştir. Ardından db kopyası "
        "tekrar 1'e çıkarılarak toparlanma süreci izlenmiştir:"
    )

    add_code_block("Deney 5 Veritabanı Kesintisi ve Readiness Probe Çıktısı",
"""# 1. DB Kopyası 0'a İndirildi (Yapay Kesinti)
$ kubectl scale deployment/db -n hafta6 --replicas=0
deployment.apps/db scaled

# 2. Kesinti Sırasında Web Pod Durumu ve EndpointSlice
$ kubectl get pods -n hafta6
NAME                   READY   STATUS    RESTARTS   AGE
check                  1/1     Running   0          93s
web-58c776859c-66fwm   0/1     Running   0          68s

$ kubectl get endpointslices -n hafta6 -l kubernetes.io/service-name=web -o yaml | grep -A 4 "conditions:"
    conditions:
      ready: false
      serving: false
      terminating: false
    nodeName: hafta6

# 3. Canlılık (Liveness) vs Servis Trafiği (Readiness) Karşılaştırması
# İçeriden Liveness sorgusu: (Süreç ayakta, liveness bozulmadı)
$ kubectl exec -n hafta6 deployment/web -- python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/health/live').read().decode())"
{"status":"ok"}

# Check Pod'undan Servis Üzerinden İstek: (Trafik kesildi!)
$ kubectl exec -n hafta6 check -- python -c "import urllib.request; urllib.request.urlopen('http://web:8000/health/ready', timeout=5)"
Expected error during outage: <urlopen error [Errno 111] Connection refused>

# 4. DB'nin Tekrar Başlatılması ve Toparlanma
$ kubectl scale deployment/db -n hafta6 --replicas=1
deployment.apps/db successfully rolled out
pod/web-58c776859c-66fwm condition met

$ kubectl get pods -n hafta6
NAME                   READY   STATUS    RESTARTS   AGE
check                  1/1     Running   0          106s
db-77cfdc4ccc-5gfd5    1/1     Running   0          11s
web-58c776859c-66fwm   1/1     Running   0          81s

$ kubectl get endpointslices -n hafta6 -l kubernetes.io/service-name=web -o yaml | grep -A 4 "conditions:"
    conditions:
      ready: true
      serving: true
      terminating: false""")

    add_p(
        "Gözlemlenen Sonuç ve Değerlendirme: Bu deney sağlık kontrollerinin en kritik ayrımını ortaya koymuştur:\n"
        "1. Web Pod'unun konteyneri çökmemiştir (STATUS: Running), bu nedenle Liveness Probe başarılı olmaya devam etmiş ve kubelet "
        "Pod'u gereksiz yere yeniden başlatmamıştır (RESTARTS = 0).\n"
        "2. Ancak web Pod'u veritabanına erişemediği için /health/ready uç noktası başarısız olmuş (HTTP 503) ve Pod 'READY: 0/1' durumuna düşmüştür.\n"
        "3. EndpointSlice denetleyicisi, hazır olmayan bu Pod'u anında 'ready: false' olarak işaretlemiş ve Service üzerinden gelen kullanıcı "
        "trafiğini kesmiştir. Bu sayede kullanıcılar bozuk yanıtlar almak yerine trafikten izole edilmiştir.\n"
        "4. Veritabanı tekrar açıldığında Readiness Probe başarı sağlamış, hedef otomatik olarak tekrar 'ready: true' yapılmış ve trafik "
        "kullanıcı müdahalesi gerekmeksizin yeniden akmaya başlamıştır. Ardından eklenen 'Kalıcılık C' kaydı sistemin tamamen toparlandığını doğrulamıştır."
    )

    # Deney 6
    add_h2("4.6 Deney 6: Sağlık Kontrolleri 2 - Canlılık (Liveness Probe) Başarısızlığı (Ek 2 Bölüm 10.2)")
    add_p(
        "Amaç: Uygulama kilitlendiğinde veya içsel bir çıkmaza girdiğinde (deadlock), Canlılık Kontrolünün (Liveness Probe) bu durumu nasıl "
        "tespit ettiğini ve kubelet'in arızalı konteyneri yeniden başlatarak (restart) sistemi nasıl kurtardığını gözlemlemek."
    )
    add_p(
        "Uygulanan Komutlar ve Süreç: Web dağıtımında livenessProbe tanımına kontrollü bir test koşulu eklenmiştir: konteyner içinde "
        "'/tmp/live-fail' dosyası varsa kontrol 'assert not exists' ifadesiyle kasıtlı olarak başarısız olmaktadır. Pod UID'si kaydedilmiş, "
        "ardından dosya oluşturulup kubelet'in tepkisi izlenmiştir:"
    )

    add_code_block("Deney 6 Canlılık Kontrolü Başarısızlığı Çıktısı",
"""# 1. Başlangıç Durumu
Web Pod: web-58c776859c-66fwm (UID: 72b9967c-ffad-4010-9a70-acb8b8ee54a8, RESTARTS: 0)

# 2. Hata Tetikleme Dosyasının Oluşturulması
$ kubectl exec -n hafta6 web-58c776859c-66fwm -- python -c "from pathlib import Path; Path('/tmp/live-fail').touch()"

# 3. Kubelet Olayları ve Konteynerin Yeniden Başlatılması
$ kubectl describe pod web-58c776859c-66fwm -n hafta6
Events:
  Type     Reason     Age                From     Message
  ----     ------     ----               ----     -------
  Warning  Unhealthy  42s (x3 over 52s)  kubelet  Liveness probe failed: AssertionError
  Normal   Killing    42s                kubelet  Container web failed liveness probe, will be restarted
  Normal   Pulled     12s                kubelet  Container image "dersnotlari-web:1.1" already present on machine
  Normal   Created    12s                kubelet  Container created
  Normal   Started    12s                kubelet  Container started

# 4. Yeniden Başlatma Sonrası Durum
$ kubectl get pod web-58c776859c-66fwm -n hafta6
NAME                   READY   STATUS    RESTARTS      AGE
web-58c776859c-66fwm   1/1     Running   1 (11s ago)   2m37s

# 5. Pod UID Kontrolü ve Geçici Dosya Varlık Denetimi
Pod UID Değişti mi?: 72b9967c-ffad-4010-9a70-acb8b8ee54a8 (AYNI KALDI!)
$ kubectl exec -n hafta6 deployment/web -- python -c "from pathlib import Path; print('live-fail exists?:', Path('/tmp/live-fail').exists())"
live-fail exists?: False""")

    add_p(
        "Gözlemlenen Sonuç ve Değerlendirme: Liveness Probe ardışık 3 kez (failureThreshold: 3) başarısız olunca kubelet doğrudan müdahale "
        "etmiş ve 'Container web failed liveness probe, will be restarted' olayıyla konteyneri sonlandırıp yeniden başlatmıştır. "
        "Burada can alıcı gözlem şudur: Pod'un kendisi silinmemiştir; Pod UID'si (72b9967c...) tamamen aynı kalmış, yalnızca Pod içindeki "
        "web konteyneri yeniden başlatılmış ve RESTARTS değeri 0'dan 1'e yükselmiştir. Konteyner yeniden başlatıldığında geçici yazılabilir "
        "katman sıfırlandığı için '/tmp/live-fail' dosyası kendiliğinden yok olmuş ve uygulama kalıcı bir arıza döngüsüne girmeden toparlanmıştır."
    )

    # Deney 7
    add_h2("4.7 Deney 7: Kaynak Talepleri ve Elle Yatay Ölçekleme (Ek 2 Bölüm 11)")
    add_p(
        "Amaç: Konteyner kaynak yönetiminde 'requests' (garanti edilen kaynak) ve 'limits' (tavan sınır) kavramlarını doğrulamak; web bileşenini "
        "1 kopyadan 2 kopyaya çıkararak EndpointSlice üzerindeki yük dağıtımını gözlemlemek ve veritabanının neden çoğaltılmadığını açıklamak."
    )
    add_p(
        "Uygulanan Komutlar ve Süreç: Dağıtım tanımındaki kaynak sınırları ('limits: cpu 500m, memory 256Mi', 'requests: cpu 100m, memory 128Mi') "
        "kontrol edilmiş; ardından 'kubectl scale deployment/web -n hafta6 --replicas=2' çalıştırılarak 2 kopya hedeflenmiştir:"
    )

    add_code_block("Deney 7 Ölçekleme Çıktıları",
"""$ kubectl describe deployment web -n hafta6 | grep -A 4 "Limits:"
    Limits:
      cpu:     500m
      memory:  256Mi
    Requests:
      cpu:     100m
      memory:  128Mi

# 1 -> 2 Kopya Ölçekleme
$ kubectl scale deployment/web -n hafta6 --replicas=2
deployment.apps/web scaled
$ kubectl rollout status deployment/web -n hafta6 --timeout=180s
deployment "web" successfully rolled out

$ kubectl get deployment web -n hafta6
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
web    2/2     2            2           4m37s

$ kubectl get pods -n hafta6 -l app=web -o wide
NAME                   READY   STATUS    RESTARTS   AGE    IP           NODE
web-58c776859c-66fwm   1/1     Running   1          3m8s   10.244.0.7   hafta6
web-58c776859c-hsrrj   1/1     Running   0          6s     10.244.0.9   hafta6

$ kubectl get endpointslices -n hafta6 -l kubernetes.io/service-name=web -o yaml | grep -A 4 "addresses:"
  - addresses:
    - 10.244.0.7
    conditions:
      ready: true
--
  - addresses:
    - 10.244.0.9
    conditions:
      ready: true

# 2 -> 1 Kopya İndirme
$ kubectl scale deployment/web -n hafta6 --replicas=1
deployment.apps/web scaled
$ kubectl get pods -n hafta6 -l app=web
NAME                   READY   STATUS        RESTARTS   AGE
web-58c776859c-66fwm   1/1     Running       1          3m8s
web-58c776859c-hsrrj   1/1     Terminating   0          6s""")

    add_p(
        "Gözlemlenen Sonuç ve Değerlendirme: Web kopya sayısı 2'ye çıkarıldığında Kubernetes Scheduler, kümedeki kaynak kapasitesini kontrol etmiş "
        "(toplam 200m CPU ve 256Mi RAM talebi) ve ikinci Pod'u ('web-...-hsrrj') düğüme başarıyla yerleştirmiştir. EndpointSlice nesnesi "
        "otomatik güncellenerek her iki Pod IP'sini (10.244.0.7 ve 10.244.0.9) 'ready: true' olarak listelemiş; böylece gelen istekler round-robin "
        "mantığıyla iki Pod arasında paylaştırılmıştır. Kopya sayısı tekrar 1'e indirildiğinde ikinci Pod kontrollü biçimde (Terminating) kaldırılmıştır."
    )
    add_callout(
        "PostgreSQL Neden Aynı Şekilde Çoğaltılmaz?",
        "Web bileşeni durumsuz (stateless) olduğu için kopya sayısı serbestçe artırılabilir; her Pod aynı veritabanına bağlanır ve gelen isteği "
        "bağımsızca işler. Buna karşın PostgreSQL ilişkisel ve durumsal (stateful) bir sistemdir. Kılavuzdaki kalıcı depolama (ReadWriteOnce) "
        "tek bir dosya sistemini bağlar. Birden fazla PostgreSQL Pod'u aynı veri dizinine (PGDATA) eşzamanlı yazmaya kalkışırsa 'split-brain' "
        "(bölünmüş beyin) durumu oluşur, işlem kilitleri bozulur ve veritabanı dosyaları geri dönülemez biçimde bozulur (data corruption). "
        "Veritabanını çoğaltmak için basit 'scale' komutu yetersizdir; birincil-ikincil (primary-replica) replikasyon protokolleri, "
        "Write-Ahead Logging (WAL) akışı ve StatefulSet gibi özelleşmiş orkestrasyon mimarileri gereklidir.",
        "WARN"
    )

    # Deney 8
    add_h2("4.8 Deney 8: Kademeli Güncelleme (Rolling Update) ve Geri Dönüş (Rollout Undo) (Ek 2 Bölüm 12-13)")
    add_p(
        "Amaç: Uygulamanın yeni sürümünün (1.2) sıfır kesinti stratejisiyle (maxUnavailable: 0, maxSurge: 1) nasıl dağıtıldığını gözlemlemek, "
        "yeni sürüm üzerinde veritabanına yeni kayıt eklemek, ardından 'rollout undo' ile önceki sürüme (1.1) geri dönüldüğünde hem eski hem yeni "
        "kayıtların korunduğunu kanıtlamak."
    )
    add_p(
        "Uygulanan Komutlar ve Süreç: Web imajı 'dersnotlari-web:1.2' olarak güncellenmiş ve aşamalı geçiş izlenmiştir. Sürüm 1.2 hazır olunca "
        "'1.2 Sürüm Kaydı' başlıklı yeni bir not eklenmiştir. Ardından 'kubectl rollout undo deployment/web -n hafta6' komutu verilerek "
        "revizyon 1.1'e geri dönülmüş ve veritabanı kayıtları listelenmiştir:"
    )

    add_code_block("Deney 8 Rolling Update ve Rollout Undo Çıktıları",
"""# 1. Sürüm 1.2'ye Güncelleme
$ kubectl set image deployment/web web=dersnotlari-web:1.2 -n hafta6
deployment.apps/web image updated
$ kubectl rollout status deployment/web -n hafta6 --timeout=180s
Waiting for deployment "web" rollout to finish: 0 out of 1 new replicas have been updated...
Waiting for deployment "web" rollout to finish: 1 old replicas are pending termination...
deployment "web" successfully rolled out

$ kubectl get deployment web -n hafta6 -o jsonpath='{.spec.template.spec.containers[0].image}'
dersnotlari-web:1.2

# 2. Sürüm 1.2'de Sağlık ve Yeni Kayıt Ekleme
$ kubectl exec -n hafta6 check -- python -c "import urllib.request; print(urllib.request.urlopen('http://web:8000/health/ready').read().decode())"
{"status":"ready","version":"1.2"}

# 1.2 sürümünde yeni kayıt (No: 104) eklenmesi:
<td>Kalıcılık A</td>
<td>Kalıcılık B</td>
<td>Kalıcılık C</td>
<td>1.2 Sürüm Kaydı</td>

# 3. Önceki Sürüme (1.1) Geri Dönüş (Rollout Undo)
$ kubectl rollout undo deployment/web -n hafta6
deployment.apps/web rolled back
$ kubectl rollout status deployment/web -n hafta6 --timeout=180s
deployment "web" successfully rolled out

$ kubectl get deployment web -n hafta6 -o jsonpath='{.spec.template.spec.containers[0].image}'
dersnotlari-web:1.1

# 4. Geri Dönüş Sonrası Sağlık ve Veritabanı Bütünlüğü Kontrolü
$ kubectl exec -n hafta6 check -- python -c "import urllib.request; print(urllib.request.urlopen('http://web:8000/health/ready').read().decode())"
{"status":"ready","version":"1.1"}

$ kubectl exec -n hafta6 check -- python -c "import urllib.request; print(urllib.request.urlopen('http://web:8000/').read().decode())" | grep "<td>"
<td><strong>101</strong></td> <td>Kalıcılık A</td>
<td><strong>102</strong></td> <td>Kalıcılık B</td>
<td><strong>103</strong></td> <td>Kalıcılık C</td>
<td><strong>104</strong></td> <td>1.2 Sürüm Kaydı</td>""")

    add_p(
        "Gözlemlenen Sonuç ve Değerlendirme: RollingUpdate stratejisi 'maxUnavailable: 0' kuralına sadık kalarak, yeni sürüm 1.2 Pod'u tamamen "
        "başlatılıp hazır olma testini (readiness probe) geçmeden eski 1.1 Pod'unu sonlandırmamıştır. Böylece kullanıcılara kesintisiz hizmet "
        "sunulmuştur. Geri dönüş ('rollout undo') yapıldığında ise imaj tekrar 'dersnotlari-web:1.1'e geçmiş ve /health/ready 'version: 1.1' "
        "döndürmüştür. En kritik sonuç şudur: Uygulama sürümünün 1.1'e dönmesi, 1.2 sürümündeyken veritabanına eklenen '1.2 Sürüm Kaydı'nı "
        "kesinlikle silmemiştir! Çünkü Kubernetes dağıtım sürümleri Pod şablonunu (imaj, çevre değişkeni vb.) kapsar; veritabanındaki "
        "kalıcı verileri geriye sarmaz."
    )

    # Deney 9
    add_h2("4.9 Deney 9: Çalışmanın Sonlandırılması ve Depolama Yönetimi (Ek 2 Bölüm 15-16)")
    add_p(
        "Amaç: Uygulama iş yükleri kaldırıldığında kalıcı depolamanın (PVC ve PV) durumunu denetlemek, 'Delete' ve 'Retain' geri kazanım "
        "politikalarının farkını ve kalıcı depolama ile veri yedekleme arasındaki ayrımı ortaya koymak."
    )
    add_p(
        "Uygulanan Komutlar ve Süreç: Dağıtımlar, servisler, kontrol Pod'u, ConfigMap ve Secret nesneleri 'kubectl delete' ile kaldırılmış, "
        "ancak 'db-data' PVC nesnesi bilinçli olarak korunmuştur:"
    )

    add_code_block("Deney 9 Kaynak Temizliği ve PVC Koruma Çıktısı",
"""$ kubectl delete deployment web db -n hafta6
$ kubectl delete service web db -n hafta6
$ kubectl delete pod check -n hafta6
$ kubectl delete configmap app-config -n hafta6
$ kubectl delete secret app-secrets -n hafta6

$ kubectl get deployments,pods,services,configmaps,secrets -n hafta6
NAME                         DATA   AGE
configmap/kube-root-ca.crt   1      6m50s

$ kubectl get pvc db-data -n hafta6 -o wide
NAME      STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE    VOLUMEMODE
db-data   Bound    pvc-fff7d32f-6b0a-478c-9943-f274a6f5ed86   1Gi        RWO            standard       6m5s   Filesystem

$ kubectl get pv pvc-fff7d32f-6b0a-478c-9943-f274a6f5ed86
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM            STORAGECLASS   AGE
pvc-fff7d32f-6b0a-478c-9943-f274a6f5ed86   1Gi        RWO            Delete           Bound    hafta6/db-data   standard       6m5s""")

    add_p(
        "Gözlemlenen Sonuç ve Değerlendirme: Uygulamanın tüm aktif iş yükleri sonlandırılmış olmasına rağmen, 'db-data' PVC'si ve diskteki "
        "fiziksel PV nesnesi 'Bound' durumunu korumuştur. Yapılandırma ve veritabanı Deployment'ı tekrar uygulandığında sistem aynı PVC'yi "
        "kullanarak eski verilere anında erişebilmektedir. Reclaim Policy 'Delete' olduğundan, eğer 'kubectl delete pvc db-data' komutu "
        "verilseydi, Kubernetes otomatik olarak alttaki PV'yi ve fiziksel depolama alanını da silecekti. 'Retain' politikasında ise PVC silinse dahi "
        "PV 'Released' durumuna geçer ve veriler disk üzerinde manuel müdahaleye kadar korunur."
    )

    # ==================== SECTION 5 ====================
    add_h1("5. BULUT ORTAMINA GEÇİŞ VE BÜTÜNLEŞİK DEĞERLENDİRME (EK 3 KAPSAMI)")
    add_p(
        "Yerel kümede (Minikube / Docker Desktop) doğrulanan bir uygulamanın büyük bulut sağlayıcılarının (AWS EKS, Microsoft Azure AKS, "
        "Google Cloud GKE) yönetilen Kubernetes ortamlarına taşınması, mimari ve operasyonel açıdan belirli uyarlamalar gerektirir. "
        "Kılavuzun Ek 3 bölümünde ele alınan bu gereksinimler aşağıda karşılaştırmalı olarak analiz edilmiştir:"
    )

    add_styled_table(
        ["Mimari / Operasyonel Alan", "Yerel Kubernetes Ortamı (Minikube)", "Yönetilen Bulut Kubernetes (EKS / AKS / GKE)"],
        [
            ["Kontrol Düzlemi (Control Plane)", "Geliştiricinin yerel makinesinde tek VM/konteyner olarak çalışır, yüksek erişilebilirlik (HA) yoktur.", "Bulut sağlayıcı tarafından çoklu kullanılabilirlik alanında (Multi-AZ) SLA garantisiyle yönetilir."],
            ["İmaj Dağıtımı (Registry)", "Yerel Docker daemon veya minikube image build ile yerel düğümlere yüklenir.", "AWS ECR, Azure ACR veya GCP Artifact Registry gibi özel depolara gönderilir; IAM veya imagePullSecrets gerekir."],
            ["Dış Trafik Erişimi", "ClusterIP servisleri dışa kapalıdır; geçici 'kubectl port-forward' ile test edilir.", "Service type: LoadBalancer (AWS NLB, Azure LB) veya Cloud Ingress Controller (ALB, NGINX) ile gerçek IP sağlanır."],
            ["Kalıcı Depolama (Storage)", "Yerel ana makine dizini (hostpath) kullanılır; düğüm arızasında veri kaybı riski vardır.", "Bulut blok depolama sınıfları (AWS EBS gp3, Azure Disk, GCP Persistent Disk) veya paylaşımlı NFS (EFS) kullanılır."],
            ["Güvenlik ve Kimlik", "Basit kubeconfig ve yerel servis hesapları kullanılır.", "Bulut IAM rolleriyle entegre Pod Kimliği (AWS IRSA, Azure Workload Identity, GCP Workload Identity) kullanılır."],
            ["Maliyet Modeli", "Donanım maliyeti hariç tamamen ücretsizdir.", "Yönetilen küme saati, çalışan EC2/VM düğümleri, yük dengeleyiciler ve ayrılan diskler için kullandıkça öde faturalandırması yapılır."]
        ],
        [1.6, 2.4, 2.5]
    )

    add_h2("5.1 Paylaşımlı Sorumluluk Modeli ve Maliyet Yönetimi")
    add_p(
        "Yönetilen bir Kubernetes hizmetinde (EKS/AKS/GKE) kontrol düzleminin sağlayıcı tarafından işletilmesi, uygulamanın tüm sorumluluğunun "
        "sağlayıcıya geçtiği anlamına gelmez. Bulut 'Paylaşımlı Sorumluluk Modeli'ne (Shared Responsibility Model) göre:"
    )
    add_bullet(" Kontrol düzleminin (API Server, etcd vb.) yüksek erişilebilirliği, çekirdek yamaları, veri merkezi güvenliği ve fiziksel donanım sağlayıcının sorumluluğundadır.", "Sağlayıcının Sorumluluğu:")
    add_bullet(" Uygulama kodunun güvenliği, doğru yapılandırma (ConfigMap/Secret), kaynak sınırlarının (requests/limits) belirlenmesi, sağlık denetimleri (probes), Pod güvenlik standartları, veri tabanı yedekleme stratejisi ve küme içi ağ politikaları tamamen müşterinin (öğrencinin/mühendisin) sorumluluğundadır.", "Müşterinin Sorumluluğu:")

    add_callout(
        "Maliyet Tuzağı: Deployment Silmek Maliyeti Bitirmez",
        "Bulut denemeleri tamamlandığında 'kubectl delete deployment web db' komutunu çalıştırmak bulut maliyetlerini sonlandırmaz! "
        "Çünkü Deployment silindiğinde yalnızca Pod'lar kaldırılır. Arkada tahsis edilen Bulut Diskleri (AWS EBS / Azure Disk PersistentVolume), "
        "Statik IP adresleri, Düğüm Havuzundaki sanal sunucular (EC2 düğümleri) ve özellikle 'LoadBalancer' servisinin açtığı harici Yük Dengeleyici "
        "hizmeti arka planda çalışmaya ve saatlik ücret üretmeye devam eder. Tüm harcamaları sonlandırmak için ilişkili PVC'lerin, Service nesnelerinin "
        "ve nihayetinde kümenin kendisinin ('eksctl delete cluster' / 'az aks delete') tamamen imha edilmesi gerekmektedir.",
        "WARN"
    )

    # ==================== SECTION 6 ====================
    add_h1("6. KAVRAMSAL AÇIKLAMALAR VE ÇALIŞMA SORULARI")
    add_p(
        "Ders notunun Bölüm 7.3 ve Kılavuzun Ek 2 Bölüm 17 başlıklarında yer alan altı temel kavramsal soru, gerçekleştirilen kontrollü deneylerin "
        "sonuçları ve Kubernetes mimarisi temelinde kapsamlı bir biçimde yanıtlanmıştır:"
    )

    add_h2("Soru 1: Web uygulamasına erişim ile web bileşeninin PostgreSQL’e erişimi nasıl sağlanır?")
    add_p(
        "Yanıt: Kubernetes ortamında Pod'lar geçici (ephemeral) varlıklardır; her yeniden başlatmada farklı bir dinamik IP adresi alırlar. "
        "Bu nedenle bileşenler birbirine doğrudan Pod IP'leri üzerinden bağlanamaz. İletişim iki farklı 'Service' nesnesi ve Kubernetes "
        "iç ağ mekanizmalarıyla çözülmüştür:"
    )
    add_bullet(" Web bileşeni, veritabanına '04-services.yaml' dosyasında tanımlanan 'service/db' nesnesi üzerinden erişir. Bu servis 'ClusterIP' türündedir ve küme içinde sabit bir sanal IP (10.111.73.51) ile 'db' adında bir DNS kaydı üretir. Web konteynerine ConfigMap üzerinden 'DB_HOST=db' ve 'DB_PORT=5432' verilmiştir. Web Pod'u istek gönderdiğinde CoreDNS bu ismi sanal IP'ye, kube-proxy ise bu IP'yi arkadaki PostgreSQL Pod'unun (10.244.0.3) 5432 portuna iletir. Veritabanı doğrudan internete açılmamış, yalnızca küme içi güvenli ağda tutulmuştur.", "Web Bileşeninin Veritabanına Erişimi:")
    add_bullet(" Kullanıcıların web arayüzüne erişimi üretim ortamında 'LoadBalancer' veya 'Ingress Controller' ile sağlanırken, bu yerel laboratuvar çalışmasında 'service/web' (ClusterIP) kullanılmıştır. Geliştiricinin yerel makinesinden bu servise ulaşabilmesi için 'kubectl port-forward -n hafta6 service/web 8080:8000' komutuyla bir tünel açılmıştır. Bu tünel, yerel makinenin 127.0.0.1:8080 portuna gelen istekleri küme içindeki 'service/web' üzerinden EndpointSlice'ta 'ready: true' olan web Pod'unun 8000 portuna yönlendirmiştir.", "Kullanıcıların Web Uygulamasına Erişimi:")

    add_h2("Soru 2: Silinen web Pod’unun yerine neden yeni Pod oluşturulur? Konteyner yeniden başlatılması ile Pod yeniden oluşturulması arasındaki fark nedir?")
    add_p(
        "Yanıt: Web Pod'u 'Deployment' nesnesi ve onun arka planda yönettiği 'ReplicaSet' denetleyicisi tarafından idare edilmektedir. "
        "Dağıtım tanımında 'spec.replicas: 1' beyan edilmiştir. Kubernetes kontrol döngüsü (reconciliation loop), kümedeki mevcut Pod sayısını "
        "sürekli gözlemler. Bir web Pod'u silindiğinde aktif kopya sayısı 0'a düşer. ReplicaSet istenen durum (1) ile gerçek durum (0) arasındaki "
        "farkı kapatmak için derhal yeni bir Pod planlar (Self-Healing)."
    )
    add_p(
        "Konteynerin Yeniden Başlatılması ile Pod'un Yeniden Oluşturulması Arasındaki Farklar:"
    )
    add_styled_table(
        ["Karşılaştırma Kriteri", "Konteynerin Yeniden Başlatılması (Container Restart)", "Pod'un Yeniden Oluşturulması (Pod Re-creation)"],
        [
            ["Tetikleyen Mekanizma", "Kubelet (Liveness Probe başarısızlığı veya sürecin çökmesi).", "ReplicaSet / Deployment denetleyicisi (Pod silinmesi veya düğüm kaybı)."],
            ["Pod Kimliği (UID) ve IP", "Pod UID'si ve Pod IP adresi DEĞİŞMEZ, tamamen aynı kalır.", "Eski Pod tamamen yok edilir; YENİ bir UID ve YENİ bir IP adresi atanır."],
            ["Konteyner Yaşam Döngüsü", "Pod kabuğu yerinde kalır; yalnızca içindeki konteyner süreci yeniden başlatılır.", "Tüm konteynerler sıfırdan oluşturulur, imaj yeniden çekilebilir."],
            ["Dosya Sistemi Etkisi", "Konteynerin yazılabilir katmanı sıfırlanır (örn. /tmp/live-fail yok olur).", "Pod düzeyindeki boşluklar (emptyDir) ve geçici katmanlar tamamen silinir."],
            ["Gösterge Belirtisi", "kubectl get pod çıktısında RESTARTS sayacı 1 artar.", "RESTARTS 0 olur, Pod adı ve UID'si değişir, AGE süresi sıfırlanır."]
        ],
        [1.6, 2.4, 2.5]
    )

    add_h2("Soru 3: Kayıtlar nerede saklanır? PostgreSQL Pod’u yeniden oluşturulduğunda neden korunur?")
    add_p(
        "Yanıt: Konteynerlerin yerel dosya sistemi geçicidir (ephemeral layer). Bir konteyner silindiğinde bu katmandaki tüm veriler kaybolur. "
        "Ancak PostgreSQL dağıtımımızda veriler konteynerin içine değil; Kubernetes'in 'PersistentVolumeClaim (db-data)' nesnesi aracılığıyla "
        "bağlanan harici bir 'PersistentVolume' (PV) üzerine yazılmaktadır."
    )
    add_p(
        "Çalışma dosyamızda (03-db.yaml) '/var/lib/postgresql/data' dizini 'data' adlı birime, bu birim de 'db-data' PVC'sine bağlanmıştır. "
        "Ayrıca 'PGDATA' değişkeni '/var/lib/postgresql/data/pgdata' yapılarak veritabanı dosyalarının bu kalıcı alt dizinde tutulması sağlanmıştır. "
        "PostgreSQL Pod'u silindiğinde Pod'un kendisi ölür; fakat bağımsız bir Kubernetes nesnesi olan 'db-data' PVC ve diskteki PV varlığını "
        "sürdürür. Yeni db Pod'u ayağa kalktığında Deployment aynı PVC'yi yeni Pod'a bağlar. PostgreSQL başlatma betiği PGDATA dizininde "
        "mevcut veritabanı kümelerini (cluster data) bulur, yeni bir kurulum yapmaz ve mevcut veritabanını doğrudan kullanıma açar. "
        "Bu sayede Kalıcılık A ve B kayıtları sıfır kayıpla korunmuştur."
    )

    add_h2("Soru 4: Hazır olma kontrolünün başarısızlığı ile canlılık kontrolünün başarısızlığı uygulamayı nasıl etkiler?")
    add_p(
        "Yanıt: Kubernetes mimarisinde Hazır Olma Kontrolü (Readiness Probe) ile Canlılık Kontrolü (Liveness Probe) tamamen farklı amaçlara hizmet eder ve başarısızlıklarında zıt tepkiler üretir:"
    )
    add_bullet(" Konteynerin kullanıcı isteklerini kabul etmeye hazır olup olmadığını denetler (örneğin veritabanı bağlantısı sağlıklı mı, önbellekler yüklendi mi?). Başarısız Olduğunda: Kubelet konteyneri ASLA öldürmez veya yeniden başlatmaz! Bunun yerine Pod'un durumunu 'READY: 0/1' yapar ve EndpointSlice/Service denetleyicisine haber verir. Servis, bu Pod'u trafik yönlendirme havuzundan çıkarır ('ready: false'). Kullanıcılar hata almaz, trafik varsa diğer hazır Pod'lara akar. Sorun düzeldiğinde (örn. veritabanı geri geldiğinde) Pod otomatik olarak tekrar havuza alınır.", "Hazır Olma Kontrolü (Readiness Probe):")
    add_bullet(" Konteyner sürecinin hayatta olup olmadığını, çıkmaza (deadlock) girip girmediğini denetler. Başarısız Olduğunda: Kubelet, uygulamanın kendini kurtaramayacağına hükmeder ve konteyneri zorla sonlandırarak (SIGKILL) YENİDEN BAŞLATIR (restart). Deney 6'da görüldüğü üzere RESTARTS sayısı artar. Eğer veritabanı kesintisinde liveness probe veritabanını denetleyecek şekilde yanlış yapılandırılsaydı, veritabanı kapalı kaldığı sürece web konteyneri sonsuz bir yeniden başlatma döngüsüne (CrashLoopBackOff) girer ve gereksiz kaynak tüketirdi.", "Canlılık Kontrolü (Liveness Probe):")

    add_h2("Soru 5: Web kopya sayısı değiştiğinde hangi bileşenler değişir? PostgreSQL neden aynı şekilde çoğaltılmaz?")
    add_p(
        "Yanıt: Web kopya sayısı 1'den 2'ye çıkarıldığında kümede şu bileşenler değişir:\n"
        "1. Deployment denetleyicisi ReplicaSet'in hedef kopya sayısını 2 yapar.\n"
        "2. Kubernetes Scheduler, ikinci web Pod'u için kaynak kontrolü yapar (100m CPU, 128Mi RAM) ve Pod'u uygun düğüme atar.\n"
        "3. Kubelet ikinci web konteynerini başlatır; başlangıç ve hazır olma kontrolleri tamamlandığında Pod 'Running 1/1' olur.\n"
        "4. En kritik değişiklik: 'EndpointSlice' nesnesine ikinci Pod'un IP adresi eklenir ve 'ready: true' yapılır. Kube-proxy yönlendirme "
        "tablolarını güncelleyerek gelen HTTP isteklerini bu iki Pod arasında paylaştırmaya başlar."
    )
    add_p(
        "PostgreSQL'in Neden Aynı Şekilde Çoğaltılamayacağı: Web servisi tamamen durumsuzdur (stateless); oturum bilgisi tutmaz ve gelen isteği "
        "veritabanından okuyup döner. Bu nedenle kopya sayısı yatayda rahatça artırılabilir. Ancak PostgreSQL ilişkisel ve durumsal (stateful) "
        "bir veritabanıdır. Kılavuzdaki kalıcı depolama 'ReadWriteOnce' modundadır; yani aynı anda yalnızca tek bir düğüm tarafından bağlanabilir. "
        "Eğer PostgreSQL Deployment kopyası 2 yapılırsa, iki farklı Pod aynı veri dizini (PGDATA) üzerinde eşzamanlı işlem kilitleri (row locks, "
        "table locks) almaya ve veri dosyalarını değiştirmeye çalışır. Bu durum ACID garantisini bozar, yarış durumlarına (race condition) yol açar "
        "ve veritabanı tablolarının fiziksel olarak bozulmasına (data corruption) neden olur. Veritabanını ölçeklemek için Deployment değil, "
        "birincil-ikincil (master-replica) replikasyon protokolleri çalıştıran 'StatefulSet' mimarileri veya bulut veritabanı servisleri (DBaaS) gereklidir."
    )

    add_h2("Soru 6: Yeni sürüme geçiş ve önceki sürüme dönüş nasıl doğrulanır? Önceki uygulama sürümüne dönmek neden veritabanını da önceki hâline getirmez?")
    add_p(
        "Yanıt: Yeni sürüme geçiş 'kubectl set image deployment/web web=dersnotlari-web:1.2' komutuyla tetiklenir. Doğrulama adımları:\n"
        "1. 'kubectl rollout status' komutuyla aşamalı güncellemenin (RollingUpdate) tamamlandığı izlenir.\n"
        "2. 'kubectl get deployment web -o jsonpath={...image}' ile çalışan aktif imaj etiketinin 'dersnotlari-web:1.2' olduğu doğrulanır.\n"
        "3. Web uygulamasının '/health/ready' uç noktasından 'version: 1.2' yanıtı alınır ve arayüzde 'Sürüm: 1.2' başlığı görülür.\n"
        "Önceki sürüme dönüş ise 'kubectl rollout undo deployment/web' komutuyla gerçekleştirilir; aktif imajın tekrar 'dersnotlari-web:1.1' olduğu "
        "ve /health/ready'nin 'version: 1.1' döndürdüğü doğrulanır."
    )
    add_p(
        "Geri Dönüşün Veritabanını Neden Geri Getirmediği: Kubernetes 'rollout undo' komutu, yalnızca Deployment manifestosundaki "
        "Pod Şablonunu (Pod Template - imaj sürümü, ortam değişkenleri, etiketler vb.) önceki revizyona geri çeker. Veritabanı ve kalıcı birimler "
        "(PV/PVC) Deployment yaşam döngüsünden tamamen bağımsız nesnelerdir. Uygulama sürümü 1.2 iken kullanıcıların kaydettiği veriler, "
        "fiziksel olarak PostgreSQL'in disk tablolarına yazılmıştır. Kubernetes'in veritabanı işlemlerini geriye alma (rollback database transactions) "
        "veya disk bloklarını geçmişe sarma gibi bir yetkisi ve mekanizması yoktur. Uygulama kodunu eski sürüme almak, veritabanını da eski haline "
        "getirmez. Veritabanı durumunu geri almak için periyodik veritabanı yedeklerinin (pg_dump, snapshot) veya geriye dönük veritabanı şema "
        "migrasyonlarının (database migration rollbacks) kullanılması şarttır."
    )

    # ==================== SECTION 7 ====================
    add_h1("7. ÇALIŞMA KODLARI VE MANİFEST DOSYALARI")
    add_p(
        "Çalışma kapsamında hazırlanan, yerel Kubernetes kümesinde test edilip doğrulanan tüm kaynak kodlar ve bildirimsel YAML manifestoları "
        "aşağıda eksiksiz olarak belgelenmiştir:"
    )

    add_h2("7.1 Flask Web Uygulaması Kaynak Kodu (app.py)")
    with open("/home/arch/Dersler/26-27-Guz/Bulut-Bilisim/Odevler/app.py") as f:
        app_code = f.read()
    add_code_block("app.py", app_code)

    add_h2("7.2 Web Arayüzü HTML Şablonu (templates/index.html)")
    with open("/home/arch/Dersler/26-27-Guz/Bulut-Bilisim/Odevler/templates/index.html") as f:
        html_code = f.read()
    add_code_block("templates/index.html", html_code)

    add_h2("7.3 Docker Yapılandırması (Dockerfile ve .dockerignore)")
    with open("/home/arch/Dersler/26-27-Guz/Bulut-Bilisim/Odevler/Dockerfile") as f:
        dockerfile_code = f.read()
    with open("/home/arch/Dersler/26-27-Guz/Bulut-Bilisim/Odevler/.dockerignore") as f:
        dockerignore_code = f.read()
    add_code_block("Dockerfile", dockerfile_code)
    add_code_block(".dockerignore", dockerignore_code)

    add_h2("7.4 Kubernetes Manifestoları (k8s Klasörü)")
    for fname in ["01-config.yaml", "02-pvc.yaml", "03-db.yaml", "04-services.yaml", "05-web.yaml", "06-check.yaml"]:
        fpath = os.path.join("/home/arch/Dersler/26-27-Guz/Bulut-Bilisim/Odevler/k8s", fname)
        with open(fpath) as f:
            yaml_code = f.read()
        add_code_block(fname, yaml_code)

    # ==================== SECTION 8 ====================
    add_h1("8. KAYNAKÇA")
    refs = [
        "[1] National Institute of Standards and Technology (NIST), 'The NIST Definition of Cloud Computing', Special Publication 800-145, Sept. 2011.",
        "[2] Kubernetes Documentation, 'Kubernetes Concepts and Architecture', https://kubernetes.io/docs/concepts/ (Erişim: Kasım 2026).",
        "[3] Docker Documentation, 'Docker Desktop Kubernetes Environment', https://docs.docker.com/desktop/use-desktop/kubernetes/ (Erişim: Kasım 2026).",
        "[4] Minikube Documentation, 'Minikube Handbook and Driver Architecture', https://minikube.sigs.k8s.io/docs/ (Erişim: Kasım 2026).",
        "[5] Kubernetes Documentation, 'Configure Liveness, Readiness and Startup Probes', https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/.",
        "[6] Kubernetes Documentation, 'Persistent Volumes and Storage Classes', https://kubernetes.io/docs/concepts/storage/persistent-volumes/.",
        "[7] Kubernetes Documentation, 'Services, Load Balancing, and Networking', https://kubernetes.io/docs/concepts/services-networking/service/.",
        "[8] Kubernetes Documentation, 'Managing Resources for Containers', https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/.",
        "[9] Kubernetes Documentation, 'Deployments and Rolling Updates', https://kubernetes.io/docs/concepts/workloads/controllers/deployment/.",
        "[10] Cloud Native Computing Foundation (CNCF), 'Cloud Native Landscape and Container Orchestration Patterns', 2026."
    ]
    for r in refs:
        add_p(r, space_after=4)

    # Save document
    out_path = "/home/arch/Dersler/26-27-Guz/Bulut-Bilisim/Odevler/16008122022_Arda_Kumartaslioglu_Bulut_Bilisim_Raporu.docx"
    doc.save(out_path)
    print(f"Report generated successfully at: {out_path}")

if __name__ == "__main__":
    create_report()
