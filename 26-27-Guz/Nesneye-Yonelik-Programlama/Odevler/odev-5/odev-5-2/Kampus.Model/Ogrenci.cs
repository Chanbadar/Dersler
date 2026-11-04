using System;

namespace Kampus.Model
{
    public sealed class Ogrenci : Kisi
    {
        public static int OlusturulanSayisi { get; private set; } = 0;
        public int Numara { get; }

        private int puan;
        public int Puan
        {
            get => puan;
            set => puan = value < 0 ? 0 : value;
        }

        public int Bakiye { get; private set; } = 0;

        public Ogrenci(string ad, int numara) : base(ad)
        {
            if (numara <= 0)
            {
                throw new ArgumentOutOfRangeException(nameof(numara), "Numara pozitif olmalıdır.");
            }
            Numara = numara;
            OlusturulanSayisi++;
        }

        public bool Yukle(int tutar)
        {
            if (tutar <= 0) return false;
            Bakiye += tutar;
            return true;
        }

        public bool Harca(int tutar)
        {
            if (tutar <= 0 || Bakiye < tutar) return false;
            Bakiye -= tutar;
            return true;
        }
    }
}
