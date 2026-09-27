/*
//ilk cikti
Console.WriteLine("HelloWorld!");

//Asama-3 icin ciktilar
Console.Write("Adiniz: ");

string ad = Console.ReadLine() ?? "";

Console.Write("Yasiniz: ");

bool yasGecerli = int.TryParse(Console.ReadLine(), out int yas);

Console.WriteLine($"Merhaba, {ad}!"); 

Console.WriteLine($"Yas bilgisi gecerli mi? {yasGecerli}"); 

Console.WriteLine($"Girilen yas: {yas}");
*/
//Asama-4 icin ciktilar
Console.Write("Adiniz ve Soyadiniz: ");

string Ad = Console.ReadLine() ?? "";

Console.Write("Ogrenci No: ");

string No = Console.ReadLine() ?? "";

Console.Write("Bolum: ");

string Bolum = Console.ReadLine() ?? "";

Console.Write("Yasiniz: ");

bool YasGecerli = int.TryParse(Console.ReadLine(), out int Yas);

Console.Write("Mezuniyet Yiliniz: ");

bool YilGecerli = int.TryParse(Console.ReadLine(), out int Yil);

Console.WriteLine("==========================Ogrenci Tanitim Karti==============");

Console.WriteLine($"Ad Soyad: {Ad}");

Console.WriteLine($"Ogrenci No: {No}");

Console.WriteLine($"Bolum: {Bolum}");

Console.WriteLine($"Yas: {Yas}");

Console.WriteLine($"Mezuniyet Yili: {Yil}");

Console.WriteLine($"Yas gecerli: {YasGecerli}");

Console.WriteLine($"Yil gecerli: {YilGecerli}");
