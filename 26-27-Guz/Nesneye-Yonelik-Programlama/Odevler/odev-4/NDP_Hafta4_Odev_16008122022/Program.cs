using System;

namespace LibraryAutomation
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Library library = new Library();

            // C3 Başlangıç Kataloğu (En az 3 kitap ve 2 yazar)
            Author author1 = new Author("Fyodor Dostoyevski", "Rusya");
            Author author2 = new Author("Mustafa Kemal Atatürk"); // Kısa kurucu kullanımı (Varsayılan: Türkiye)

            library.AddBook(new Book("9789750719387", "Suç ve Ceza", author1));
            library.AddBook(new Book("9789750719394", "Budala", author1));
            library.AddBook(new Book("9789753438407", "Nutuk", author2));

            bool exit = false;

            while (!exit)
            {
                Console.WriteLine("\n=== KÜTÜPHANE OTOMASYON SİSTEMİ ===");
                Console.WriteLine("1. Kitapları Listele");
                Console.WriteLine("2. ISBN ile Kitap Ara");
                Console.WriteLine("3. Kitap Ödünç Al");
                Console.WriteLine("4. Kitap İade Et");
                Console.WriteLine("5. Yeni Kitap Ekle");
                Console.WriteLine("6. Toplam / Ödünç Verilebilir Kitap Sayılarını Göster");
                Console.WriteLine("7. Çıkış");
                Console.Write("Seçiminiz (1-7): ");

                string input = Console.ReadLine();

                switch (input)
                {
                    case "1":
                        library.ListAllBooks();
                        break;

                    case "2":
                        Console.Write("Aranacak ISBN Numarası: ");
                        string searchIsbn = Console.ReadLine();
                        Book foundBook = library.GetBookByIsbn(searchIsbn);
                        if (foundBook != null)
                        {
                            Console.WriteLine($"\n[Kitap Bulundu]\n{foundBook}");
                        }
                        else
                        {
                            Console.WriteLine("\n[!] Hata: Belirtilen ISBN numarasına ait kitap bulunamadı!");
                        }
                        break;

                    case "3":
                        Console.Write("Ödünç Alınacak Kitabın ISBN Numarası: ");
                        string borrowIsbn = Console.ReadLine();
                        var borrowResult = library.BorrowBook(borrowIsbn);
                        Console.WriteLine($"\n{borrowResult.Message}");
                        break;

                    case "4":
                        Console.Write("İade Edilecek Kitabın ISBN Numarası: ");
                        string returnIsbn = Console.ReadLine();
                        var returnResult = library.ReturnBook(returnIsbn);
                        Console.WriteLine($"\n{returnResult.Message}");
                        break;

                    case "5":
                        AddNewBookUI(library);
                        break;

                    case "6":
                        Console.WriteLine($"\n--- KÜTÜPHANE İSTATİSTİKLERİ ---");
                        Console.WriteLine($"Katalogdaki Toplam Kitap Sayısı (Library.TotalBooks): {library.TotalBooks}");
                        Console.WriteLine($"Ödünç Verilebilir Kitap Sayısı (Library.AvailableBooks): {library.AvailableBooks}");
                        Console.WriteLine($"Sistemde Toplam Üretilen Book Nesnesi (Book.CreatedCount): {Book.CreatedCount}");
                        break;

                    case "7":
                        exit = true;
                        Console.WriteLine("\nSistemden çıkılıyor... İyi günler!");
                        break;

                    default:
                        Console.WriteLine("\n[!] Geçersiz seçim! Lütfen 1-7 arasında bir değer giriniz.");
                        break;
                }
            }
        }

        private static void AddNewBookUI(Library library)
        {
            try
            {
                Console.WriteLine("\n--- YENİ KİTAP EKLEME ---");
                Console.Write("ISBN Numarası: ");
                string isbn = Console.ReadLine();

                Console.Write("Kitap Başlığı: ");
                string title = Console.ReadLine();

                Console.Write("Yazar Adı: ");
                string authorName = Console.ReadLine();

                Console.Write("Yazar Ülkesi (Boş bırakılabilir): ");
                string authorCountry = Console.ReadLine();

                Author author = string.IsNullOrWhiteSpace(authorCountry) 
                    ? new Author(authorName) 
                    : new Author(authorName, authorCountry);

                Book newBook = new Book(isbn, title, author);

                bool success = library.AddBook(newBook);
                if (success)
                {
                    Console.WriteLine("\n[✓] Kitap başarıyla kütüphane kataloğuna eklendi.");
                }
                else
                {
                    Console.WriteLine("\n[!] Hata: Bu ISBN numarasına sahip bir kitap katalogda zaten mevcut!");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\n[!] Kitap Ekleme Hatası: {ex.Message}");
            }
        }
    }
}
