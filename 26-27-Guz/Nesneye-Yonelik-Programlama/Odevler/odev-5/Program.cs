using System;
using Kampus.Model;

namespace Kampus.App
{
    internal class Program
    {
        static void Main(string[] args)
        {
            // Kimlik Başlığı
            Console.WriteLine("==================================================");
            Console.WriteLine("AD SOYAD : Arda Kumartaşlıoğlu");
            Console.WriteLine("ÖĞR. NO  : 16008122022");
            Console.WriteLine("==================================================\n");

            Console.WriteLine("--- C Sabit Test Sonuçları ---");

            Ogrenci a = new Ogrenci("Deniz", 301) { Puan = -5 };
            Ogrenci b = new Ogrenci("Selin", 302) { Puan = 78 };
            Ogrenci tekrar = new Ogrenci("Mert", 301);

            KayitDefteri defter = new KayitDefteri();

            Console.WriteLine(defter.Ekle(a));
            Console.WriteLine(defter.Ekle(b));
            Console.WriteLine(defter.Ekle(tekrar));
            Console.WriteLine($"{Ogrenci.OlusturulanSayisi}/{defter.Adet}");
            Console.WriteLine(a.Yukle(120));
            Console.WriteLine(a.Harca(35));
            Console.WriteLine(a.Harca(100));
            Console.WriteLine(a.Yukle(-10));
            Console.WriteLine($"{a.Bakiye}/{a.Puan}");
            Console.WriteLine(defter[0].Ad);

            Func<Ogrenci, bool> sec = o => o.Numara > 301;
            for (int i = 0; i < defter.Adet; i++)
            {
                if (sec(defter[i]))
                {
                    Console.WriteLine(defter[i].Ad);
                }
            }

            // Ek Test Senaryoları (Ek 1 için)
            Console.WriteLine("\n--- Ek Test Senaryoları (T2, T3, T4) ---");
            
            // T2: Boş ad ve sıfır numara denetimi
            try
            {
                Ogrenci bosAd = new Ogrenci("   ", 305);
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"[T2 - Boş Ad Hata Yakalandı]: {ex.Message}");
            }

            try
            {
                Ogrenci sifirNo = new Ogrenci("Ahmet", 0);
            }
            catch (ArgumentOutOfRangeException ex)
            {
                Console.WriteLine($"[T2 - Sıfır Numara Hata Yakalandı]: {ex.Message}");
            }

            // T3: Sıfır/Negatif Harcama ve Bakiyenin Korunması
            bool harcamaSifir = a.Harca(0);
            bool harcamaNegatif = a.Harca(-20);
            Console.WriteLine($"[T3 - Sıfır Harcama Sonucu]: {harcamaSifir}, Güncel Bakiye: {a.Bakiye}");
            Console.WriteLine($"[T3 - Negatif Harcama Sonucu]: {harcamaNegatif}, Güncel Bakiye: {a.Bakiye}");

            // T4: Seçme Sınırının Değiştirilmesi
            Func<Ogrenci, bool> secAlternatif = o => o.Puan > 50;
            Console.WriteLine("[T4 - Puanı 50'den Büyük Öğrenciler]:");
            for (int i = 0; i < defter.Adet; i++)
            {
                if (secAlternatif(defter[i]))
                {
                    Console.WriteLine($"- {defter[i].Ad} (Puan: {defter[i].Puan})");
                }
            }
        }
    }
}
