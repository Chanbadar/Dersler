using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Ders_02_05_Soru
{
    class Program
    {
        static void Main(string[] args)
        {
            int toplam = 0;
            int ek = 100000000; //integer'ın en büyük değeri
            int eb = 0;
            for (int i = 0; i < 10; i++)
            {
                Console.Write((i+1)+". pozitif sayıyı girin: ");
                string sayi_s = Console.ReadLine();
                int sayi =  Convert.ToInt32(sayi_s);
                toplam += sayi;
                if (ek > sayi)
                    ek = sayi;
                if (eb < sayi)
                    eb = sayi;
            }

            double ort = (double)toplam / 10;

            Console.WriteLine("Toplam: " + toplam);
            Console.WriteLine("Ortalama: " + ort);
            Console.WriteLine("En büyük: " + eb);
            Console.WriteLine("En küçük: " + ek);
            
            Console.ReadKey();
        }
    }
}
