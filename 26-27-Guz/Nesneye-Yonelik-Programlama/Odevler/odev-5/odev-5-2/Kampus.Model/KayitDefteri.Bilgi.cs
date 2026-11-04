namespace Kampus.Model
{
    public partial class KayitDefteri
    {
        public string Bilgi()
        {
            return $"Adet: {Adet}";
        }

        public string Bilgi(string baslik)
        {
            return $"{baslik}: {Adet}";
        }
    }
}
