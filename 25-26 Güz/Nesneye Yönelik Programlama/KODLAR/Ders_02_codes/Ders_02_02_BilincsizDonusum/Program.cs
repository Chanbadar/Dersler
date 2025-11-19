using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Ders_02_02_BilincsizDonusum
{
    class Program
    {
        static void Main(string[] args)
        {
            int a = 1200;
            byte b = 255;
            int temp = a + b;
            Console.WriteLine(temp);

            char x = 'A';
            int y = x;
            Console.WriteLine(x);
            Console.WriteLine(y);
            Console.ReadKey();
        }
    }
}
