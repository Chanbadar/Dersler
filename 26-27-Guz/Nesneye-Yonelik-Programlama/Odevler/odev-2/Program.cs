// See https://aka.ms/new-console-template for more information
//A-1
/*int x = 8;
Console.WriteLine(x> 5 && x < 10);
*/
//A-2
/*
for (int i=1;i<=5;i++)
{
	if(i==3) continue;
	Console.Write(i);
}
*/
//A-3
/*
int n=2;
do
{
	Console.Write(n);
	n--;
}while (n>0);
*/
//B --Cevap ikinci satira > isareti gelmeli, en son satira break; konmali yoksa sonsuz donguye girer
/*int puan = 70;
if(puan>=60)
	Console.WriteLine("Gecti");
int i=1;
while(i<=5)
{
	Console.WriteLine(i); break;
}
*/
//C
int aracSayisi;
Console.Write("Arac sayisini girin (1-20):");
bool aracSayisiKontrol= int.TryParse(Console.ReadLine(), out aracSayisi);
decimal gunlukGelir = 0;
int otomobilSayisi = 0;

for (int i=1; i<=aracSayisi;i++)
{
	Console.Write("Plaka giriniz: ");
	string plaka = Console.ReadLine();
	
	Console.Write("Arac turunu giriniz (O-Otomobil, M-Motosiklet, K-Kamyonet): ");
    	string AracTur = Console.ReadLine();
	
	int ParkSuresi;
	Console.Write("Park suresini giriniz (Saat): ");
	bool SureCheck = int.TryParse(Console.ReadLine(),out ParkSuresi);
	bool gecerliAralikMi = SureCheck && ParkSuresi >= 1 && ParkSuresi <= 24;
	while (!gecerliAralikMi)
	{
		Console.Write("Hatali giris Lutfen 1 ile 24 arasinda bir saat degeri giriniz: ");
        	SureCheck = int.TryParse(Console.ReadLine(), out ParkSuresi);
        	gecerliAralikMi = SureCheck && ParkSuresi >= 1 && ParkSuresi <= 24;
	}
	decimal saatlikUcret = AracTur switch
	{
    		"M"          => 15TL,
    		"O"            => 25TL,
    		"K"		 => 40TL
	};



}



