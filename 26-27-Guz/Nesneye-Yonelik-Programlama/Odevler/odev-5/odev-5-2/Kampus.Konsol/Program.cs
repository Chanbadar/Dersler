using System;
using Kampus.Model; // D1: Model kütüphanesi namespace'i

namespace Kampus.Konsol
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

            // Bölüm C Ana Testi
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

            // Bölüm D Ek Test Kodu
            Console.WriteLine(defter.Bilgi());
            Console.WriteLine(defter.Bilgi("Kampus"));

            Puan x = new Puan(35);
            Puan y = new Puan(15);
            Puan toplam = x + y;

            Console.WriteLine($"{x.Deger}/{y.Deger}/{toplam.Deger}");
            Console.WriteLine(ReferenceEquals(x, toplam));
        }
    }
}
