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
using System;

class Program
{
	static void Main()
	{
		// 1. Araç sayısını 1-20 arasında TryParse ile doğrulayarak alma
		int aracSayisi;
		Console.Write("Araç sayısını giriniz (1-20): ");
		bool aracSayisiKontrol = int.TryParse(Console.ReadLine(), out aracSayisi) && aracSayisi >= 1 && aracSayisi <= 20;

		while (!aracSayisiKontrol)
		{
			Console.Write("Hatalı giriş! Lütfen 1 ile 20 arasında bir araç sayısı giriniz: ");
			aracSayisiKontrol = int.TryParse(Console.ReadLine(), out aracSayisi) && aracSayisi >= 1 && aracSayisi <= 20;
		}

		// İstatistik değişkenleri
		decimal toplamGelir = 0;
		int motosikletSayisi = 0;
		int otomobilSayisi = 0;
		int kamyonetSayisi = 0;

		decimal enYuksekUcret = 0;
		string enYuksekUcretPlaka = "";

		// 2. Her araç için bilgileri döngüde alma
		for (int i = 1; i <= aracSayisi; i++)
		{
			Console.WriteLine($"\n--- {i}. Araç Bilgileri ---");
			Console.Write("Plaka giriniz: ");
			string plaka = Console.ReadLine();

			// 3. Araç türü doğrulaması (M, O, K)
			Console.Write("Araç türünü giriniz (M-Motosiklet, O-Otomobil, K-Kamyonet): ");
			string aracTur = Console.ReadLine()?.Trim().ToUpper();

			while (aracTur != "M" && aracTur != "O" && aracTur != "K")
			{
				Console.Write("Geçersiz araç türü! Lütfen sadece 'M', 'O' veya 'K' giriniz: ");
				aracTur = Console.ReadLine()?.Trim().ToUpper();
			}

			// Tür sayılarını güncelleme
			switch (aracTur)
			{
				case "M": motosikletSayisi++; break;
				case "O": otomobilSayisi++; break;
				case "K": kamyonetSayisi++; break;
			}

			// 4. Park süresi doğrulaması (1-24 saat)
			int parkSuresi;
			Console.Write("Park süresini giriniz (Saat): ");
			bool sureCheck = int.TryParse(Console.ReadLine(), out parkSuresi);
			bool gecerliAralikMi = sureCheck && parkSuresi >= 1 && parkSuresi <= 24;

			while (!gecerliAralikMi)
			{
				Console.Write("Hatalı giriş! Lütfen 1 ile 24 arasında bir saat değeri giriniz: ");
				sureCheck = int.TryParse(Console.ReadLine(), out parkSuresi);
				gecerliAralikMi = sureCheck && parkSuresi >= 1 && parkSuresi <= 24;
			}

			// 5. Saatlik ücretleri switch expression ile belirleme
			decimal saatlikUcret = aracTur switch
			{
				"M" => 15m,
				"O" => 25m,
				"K" => 40m,
				_   => 0m
			};

			// Toplam ücret hesabı
			decimal toplamUcret = saatlikUcret * parkSuresi;

			// 6. 8 saat ve üzerindeki sürelere %10 indirim
			if (parkSuresi >= 8)
			{
				toplamUcret *= 0.90m; // %10 indirim
			}

			// 7. Hesaplanan ücreti yazdırma
			Console.WriteLine($"Hesaplanan Ücret ({plaka}): {toplamUcret:C2}");

			// Gün sonu toplamı
			toplamGelir += toplamUcret;

			// 9. En yüksek ücreti ve plakayı güncelleme
			if (toplamUcret > enYuksekUcret)
			{
				enYuksekUcret = toplamUcret;
				enYuksekUcretPlaka = plaka;
			}
		}

		// 8. Gün sonu özeti
		Console.WriteLine("\n====================================");
		Console.WriteLine("          GÜN SONU ÖZETİ            ");
		Console.WriteLine("====================================");
		Console.WriteLine($"Motosiklet Sayısı : {motosikletSayisi}");
		Console.WriteLine($"Otomobil Sayısı   : {otomobilSayisi}");
		Console.WriteLine($"Kamyonet Sayısı   : {kamyonetSayisi}");
		Console.WriteLine($"Toplam Gelir      : {toplamGelir:C2}");
		if (aracSayisi > 0)
		{
			Console.WriteLine($"En Yüksek Ücret   : {enYuksekUcret:C2} (Plaka: {enYuksekUcretPlaka})");
		}
		Console.WriteLine("====================================");
	}
}



