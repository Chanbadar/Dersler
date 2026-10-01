using System.ComponentModel.Design;

namespace hafta2
{
    internal class Program
    {
        static void Main(string[] args)
        {
            bool ok = int.TryParse(Console.ReadLine(), out int yas); 
            if (yas>=18 && ok)
            {
                Console.WriteLine("Yaş geçerli ve 18 den büyük");

            }
            if(yas<18)
            {
                Console.WriteLine("yas 18den küçük");
            }
 
            else
            {
                Console.WriteLine("hatalı giriş");
            }
            IExtenderListService 
  
        }
    }
}
