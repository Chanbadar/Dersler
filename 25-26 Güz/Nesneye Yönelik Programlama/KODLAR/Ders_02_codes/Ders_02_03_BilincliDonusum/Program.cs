using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Ders_02_03_BilincliDonusum
{
    class Program
    {
        static void Main(string[] args)
        {
            int a = 25;
            byte b = (byte)a;
            Console.WriteLine(b);

            object x = "merhaba";
            string y = (string)x;
            Console.WriteLine(x);
            Console.WriteLine(y);

            object m = 500;
            int n = (int)m;
            Console.WriteLine(m);
            Console.WriteLine(n);            

            //object k = '5';
            //int l = (int)k; //hatalı
            //Console.WriteLine(k);
            //Console.WriteLine(l);

            int c = 555500;
            string d = c.ToString();
            Console.WriteLine(d);

            int c1 = 555500;
            string d1 = Convert.ToString(c1); //Convert nesnesi üzerinden dönüşüm
            Console.WriteLine(d1);
            Console.ReadKey();
        }
    }
}
