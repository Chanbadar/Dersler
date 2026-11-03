using System;
using System.Collections.Generic;
using System.Collections;

using System.Linq;
using System.Text;

namespace Ders_02_06_Dizi
{
    class Program
    {
        static void Main(string[] args)
        {
            ArrayList arlis = new ArrayList();
            arlis.Add(100);
            arlis.Add(10);
            arlis.Add(1000); 
            foreach (var item in arlis)
                Console.WriteLine(item);
            arlis.Sort(0,3,null);
            foreach (var item in arlis)
                Console.WriteLine(item);
            arlis.Reverse();
            foreach (var item in arlis)
                Console.WriteLine(item);

            int[] dizi = {5,6,78,67,5,6,7,8,1,15,76,87,98,9,32,4};
            int toplam = dizi[0];
            int ek = dizi[0]; //integer'ın en büyük değeri
            int eb = dizi[0];
            //for (int i = 1; i < dizi.Length; i++) //dizi.Length dizi boyutu veren özellik
            //{
            //    toplam += dizi[i];
            //    if (ek > dizi[i])
            //        ek = dizi[i];
            //    if (eb < dizi[i])
            //        eb = dizi[i];
            //}

            //for bölümünü foreach döngüsüne dönüştürme
            bool basla = false;
            foreach (int item in dizi)
            {
                if (basla) //if (basla == true) aynı kapıya çıkar //1. eleman dikkate alınmadı
                {
                    toplam += item;
                    if (ek > item)
                        ek = item;
                    if (eb < item)
                        eb = item;
                }
                else
                    basla = true;
            }
            Console.WriteLine("-----------------------------------------");
            Array.Sort(dizi);
         
            foreach (int item in dizi)
                Console.WriteLine(item);


            double ort = (double)toplam / 10;

            Console.WriteLine("Toplam: " + toplam);
            Console.WriteLine("Ortalama: " + ort);
            Console.WriteLine("En büyük: " + eb);
            Console.WriteLine("En küçük: " + ek);

            Console.ReadKey();
        }
    }
}
