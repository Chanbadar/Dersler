using System;
using System.Collections.Generic;
using System.Linq;

namespace LibraryAutomation
{
    public class Library
    {
        // readonly: Listenin kendisine yeni bir referans atanmasını engeller, eleman ekleme/çıkarmaya engel değildir
        private readonly List<Book> _books;

        public Library()
        {
            _books = new List<Book>();
        }

        // Hesaplanan (Computed) Property: İç listedeki toplam kitap sayısı
        public int TotalBooks => _books.Count;

        // Hesaplanan (Computed) Property: Ödünç verilebilir (kütüphanede olan) kitap sayısı
        public int AvailableBooks => _books.Count(b => !b.IsBorrowed);

        // Kitap Ekleme (Yinelenen ISBN engellenir)
        public bool AddBook(Book book)
        {
            if (book == null)
                throw new ArgumentNullException(nameof(book));

            // Aynı ISBN'ye sahip kitap katalogda var mı?
            if (GetBookByIsbn(book.Isbn) != null)
            {
                return false; // Mükerrer kayıt engellendi
            }

            _books.Add(book);
            return true;
        }

        // ISBN ile Kitap Arama (Bulunamazsa null döner)
        public Book GetBookByIsbn(string isbn)
        {
            if (string.IsNullOrWhiteSpace(isbn))
                return null;

            return _books.FirstOrDefault(b => b.Isbn.Equals(isbn.Trim(), StringComparison.OrdinalIgnoreCase));
        }

        // Kitap Ödünç Verme İşlemi
        public (bool IsSuccess, string Message) BorrowBook(string isbn)
        {
            Book book = GetBookByIsbn(isbn);
            if (book == null)
            {
                return (false, "İşlem Başarısız: Bu ISBN numarasına sahip kitap kütüphanede bulunamadı!");
            }

            if (book.Borrow())
            {
                return (true, $"'{book.Title}' başlıklı kitap başarıyla ödünç alındı.");
            }
            else
            {
                return (false, $"İşlem Başarısız: '{book.Title}' kitabı zaten ödünç verilmiş durumda!");
            }
        }

        // Kitap İade Etme İşlemi
        public (bool IsSuccess, string Message) ReturnBook(string isbn)
        {
            Book book = GetBookByIsbn(isbn);
            if (book == null)
            {
                return (false, "İşlem Başarısız: Bu ISBN numarasına sahip kitap kütüphanede bulunamadı!");
            }

            if (book.ReturnBook())
            {
                return (true, $"'{book.Title}' başlıklı kitap başarıyla iade edildi.");
            }
            else
            {
                return (false, $"İşlem Başarısız: '{book.Title}' kitabı zaten kütüphanede görünüyor (ödünç alınmamış)!");
            }
        }

        // Tüm kitapları konsola listeler
        public void ListAllBooks()
        {
            if (_books.Count == 0)
            {
                Console.WriteLine("\nKütüphanede henüz kayıtlı kitap bulunmamaktadır.");
                return;
            }

            Console.WriteLine("\n================ KÜTÜPHANE KATALOĞU ================");
            foreach (var book in _books)
            {
                Console.WriteLine(book.ToString());
            }
            Console.WriteLine("====================================================");
        }
    }
}
