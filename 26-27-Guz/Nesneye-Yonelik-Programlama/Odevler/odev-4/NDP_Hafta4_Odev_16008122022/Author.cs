using System;

namespace LibraryAutomation
{
    public class Author
    {
        private string _name;
        private string _country;

        // Ad boş veya sadece boşluklardan oluşamaz
        public string Name
        {
            get => _name;
            set
            {
                if (string.IsNullOrWhiteSpace(value))
                    throw new ArgumentException("Yazar adı boş veya sadece boşluklardan oluşamaz!");
                _name = value.Trim();
            }
        }

        public string Country
        {
            get => _country;
            set => _country = string.IsNullOrWhiteSpace(value) ? "Bilinmiyor" : value.Trim();
        }

        // 1. Kurucu (Kısa Kurucu): this(...) kullanarak diğer kurucuyu çağırır ve varsayılan ülke atar
        public Author(string name) : this(name, "Türkiye")
        {
        }

        // 2. Kurucu (Ana Kurucu)
        public Author(string name, string country)
        {
            Name = name;       // Property üzerinden doğrulama yapılır
            Country = country;
        }

        public override string ToString()
        {
            return $"{Name} ({Country})";
        }
    }
}
