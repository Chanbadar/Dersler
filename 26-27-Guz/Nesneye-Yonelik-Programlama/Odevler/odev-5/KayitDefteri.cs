using System;
using System.Collections.Generic;

namespace Kampus.Model
{
    public class KayitDefteri
    {
        private readonly List<Ogrenci> ogrenciler = new List<Ogrenci>();

        public int Adet => ogrenciler.Count;

        public bool Ekle(Ogrenci aday)
        {
            if (aday == null)
            {
                throw new ArgumentNullException(nameof(aday), "Eklenecek öğrenci null olamaz.");
            }

            foreach (var ogrenci in ogrenciler)
            {
                if (ogrenci.Numara == aday.Numara)
                {
                    return false; // Aynı öğrenci numarası var, eklenmedi
                }
            }

            ogrenciler.Add(aday);
            return true;
        }

        public Ogrenci this[int i]
        {
            get => ogrenciler[i];
        }
    }
}
