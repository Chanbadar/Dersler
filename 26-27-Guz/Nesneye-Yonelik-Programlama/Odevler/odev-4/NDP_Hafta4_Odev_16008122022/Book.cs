using System;

namespace LibraryAutomation
{
    public class Book
    {
        // Statik Nesne Sayacı: Oluşturulan toplam Book nesnesi sayısını tutar
        private static int _createdCount = 0;
        public static int CreatedCount => _createdCount;

        private string _title;

        // ISBN kurucu sırasında atanır, dışarıdan sadece okunabilir (init/readonly mantığı)
        public string Isbn { get; }
        
        public Author Author { get; }

        public string Title
        {
            get => _title;
            private set
            {
                if (string.IsNullOrWhiteSpace(value))
                    throw new ArgumentException("Kitap başlığı boş veya sadece boşluklardan oluşamaz!");
                _title = value.Trim(); // Başındaki/sondaki boşlukları temizler
            }
        }

        // Ödünç durumu dışarıdan doğrudan değiştirilemez
        public bool IsBorrowed { get; private set; }

        public Book(string isbn, string title, Author author)
        {
            if (string.IsNullOrWhiteSpace(isbn))
                throw new ArgumentException("ISBN numarası boş olamaz!");

            Isbn = isbn.Trim();
            Title = title;
            Author = author ?? throw new ArgumentNullException(nameof(author), "Yazar nesnesi null olamaz!");
            IsBorrowed = false;

            // Başarılı bir şekilde nesne oluşturulduğunda static sayacı bir artırır
            _createdCount++;
        }

        // Ödünç alma metodu
        public bool Borrow()
        {
            if (IsBorrowed)
            {
                return false; // Zaten ödünç verilmiş
            }
            IsBorrowed = true;
            return true;
        }

        // İade etme metodu
        public bool ReturnBook()
        {
            if (!IsBorrowed)
            {
                return false; // Zaten kütüphanede, ödünç alınmamış
            }
            IsBorrowed = false;
            return true;
        }

        public override string ToString()
        {
            string status = IsBorrowed ? "Ödünç Verildi" : "Kütüphanede (Mevcut)";
            return $"[ISBN: {Isbn}] - Başlık: {Title} | Yazar: {Author.Name} | Durum: {status}";
        }
    }
}
