using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Ders_02_04_ReadLine
{
    class Program
    {
        static void Main(string[] args)
        {
            string str = Console.ReadLine();
            Console.WriteLine(str);

            Console.Write("Birinci sayıyı girin: ");
            string sayi1 = Console.ReadLine();
            Console.Write("İkinci sayıyı girin: ");
            string sayi2 = Console.ReadLine();
            int toplam = Convert.ToInt32(sayi1) + Convert.ToInt32(sayi2); //bilinçli dönüşüm işlemi
            Console.WriteLine("Toplam: " + toplam);
            Console.WriteLine(sayi1 + sayi2);//string birleştirme işlemi yapar
            Console.ReadKey();
        }
    }
}
