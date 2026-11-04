namespace Kampus.Model
{
    public class Puan
    {
        public int Deger { get; }

        public Puan(int deger)
        {
            Deger = deger;
        }

        public static Puan operator +(Puan a, Puan b)
        {
            return new Puan(a.Deger + b.Deger);
        }
    }
}
