namespace uyg2
{
    internal class Program
    {
        static void Main(string[] args)
        {
            int derece = 259;
            string durum = derece switch
            {
                <= 0 => "soğuk",
                >0 and <15 => "ılık", 
                >=15 and <30 =>"sıcak",
                >= 30 =>"çok sıcak"
            };
            Console.WriteLine(durum);
            int i = 0; 
            while (i<5)
            {
              
                Console.WriteLine(i);
                ++i;  // yan etkisi olan operatör
                //if (i == 3) continue;
                Console.WriteLine("deneme");
            }
            Console.WriteLine(i);
            do
            {
                Console.WriteLine("ben do while içindeyim" + i );
                if (i==3) break;
                i--;

            } while (i >0); 

            for (int y = 100;y<=10;y+=1)
            {
                Console.WriteLine($"y değeri = {y}");
            }

            for (int x = 1; x<=10;x++)
                for (int y =1;y<=10;y+=1)
                {
                    Console.WriteLine($" {x} * {y} "+ x * y);
                }
            Console.WriteLine("-----------------");
            int[] dizi = { 0, 1, 2, 3 }; //array
            foreach(int d in dizi)
                Console.WriteLine(d);
            foreach (var item in dizi) Console.WriteLine(item.ToString());





        }
    }
}
