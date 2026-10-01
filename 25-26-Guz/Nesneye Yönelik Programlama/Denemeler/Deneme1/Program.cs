using System;
public class Araba
{
	public string Renk;
	public int MaxHiz;
	public void Calistir()
	{
		Console.WriteLine("Araba motoru çalıştı ve ses çıkarıyor.");
	}
}
public class Program
{
	public static void Main()
	{
		Araba araba=new Araba();
		araba.Renk= "Kırmızı";
		araba.MaxHiz=100;
		araba.Calistir();
	}
}
