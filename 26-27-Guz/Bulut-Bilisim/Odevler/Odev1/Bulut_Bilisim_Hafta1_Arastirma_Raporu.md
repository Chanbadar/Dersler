# BULUT BİLİŞİM DERSİ
## HAFTA 1 ARAŞTIRMA ÖDEVİ RAPORU: BİR İŞ YÜKÜ İÇİN BULUT ÇÖZÜMÜ SEÇİMİ

---

### 1. Kapak Bilgileri
* **Dersin Adı:** Bulut Bilişim
* **Ödevin Adı:** Hafta 1 Araştırma Ödevi: Bir İş Yükü İçin Bulut Çözümü Seçimi
* **Seçilen İş Yükü:** Üniversite Ders Kayıt ve Bilgi Yönetim Sistemi
* **Öğrencinin Adı ve Soyadı:** [Öğrenci Adı Soyadı]
* **Öğrenci Numarası:** [Öğrenci Numarası]
* **Teslim Tarihi:** Ekim 2026

---

### 2. Seçilen İş Yükünün Tanıtılması
Bu çalışmada iş yükü olarak **"Üniversite Ders Kayıt ve Bilgi Yönetim Sistemi"** seçilmiştir. Sistem; yaklaşık 30.000 aktif öğrencinin, 1.500 akademik danışmanın ve idari personelin dönem başlarında ders seçimi, kontenjan takibi, önkoşul kontrolü ve danışman onay süreçlerini yürüttüğü kurumsal bir web platformudur [1].

Sistem; kimlik bilgileri (T.C. kimlik no, parola karmaları), akademik kayıtlar (transkript, not ortalamaları) ile müfredat ve kontenjan verilerini işler. Sistemin yük profili son derece dengesizdir. Yılın yaklaşık 50 haftasında yalnızca düşük yoğunluklu not ve belge görüntüleme sorguları yapılırken, güz ve bahar yarıyılı kayıt sabahlarında (özellikle 09:00'da) on binlerce öğrencinin eşzamanlı istek göndermesiyle ekstrem bir talep patlaması (spike) yaşanır. Bu kritik saatlerdeki kesintiler öğrenci mağduriyetine, kontenjan dağılımında adaletsizliğe ve kurumsal itibar kaybına yol açar. Ayrıca işlenen veriler 6698 sayılı KVKK ve YÖK düzenlemeleri kapsamında yüksek hassasiyetli kişisel verilerdir.

---

### 3. İş Yükünün Temel Gereksinimleri
Sistemin mimari ve teknik gereksinimleri şunlardır:
1. **Yüksek Eşzamanlılık ve Düşük Gecikme:** Kayıt anında saniyede binlerce isteği kilitlenme olmaksızın karşılayabilme kapasitesi.
2. **ACID Veri Tutarlılığı:** Kotalı derslerde kontenjan aşımını (overbooking) ve yarış durumlarını (race condition) engelleyen ilişkisel bütünlük.
3. **Bellek İçi Önbellekleme:** Müfredat ve ders katalogları gibi statik verilerin birincil veritabanını tüketmemesi için hızlı önbellek katmanı.
4. **Veri Güvenliği ve Gizliliği:** Kişisel verilerin aktarımda (TLS 1.3) ve depolamada (AES-256) şifrelenmesi, yetkilerin rol tabanlı erişim kontrolü (RBAC) ile sınırlandırılması.
5. **Dinamik Ölçeklenebilirlik:** Sakin dönemlerde asgari kaynak tüketip kayıt günlerinde otomatik olarak genişleyebilen elastik altyapı.

---

### 4. NIST Temel Özelliklerinin İş Yükündeki Karşılıkları
NIST SP 800-145 belgesinde tanımlanan beş temel niteliğin seçilen iş yükündeki somut karşılıkları şunlardır [1]:
* **On-demand self-service (İsteğe bağlı self servis):** Üniversite BT ekibinin kayıt haftasından önce sağlayıcı personeline ihtiyaç duymadan, konsol veya API üzerinden yeni uygulama düğümleri ve veritabanı okuma kopyaları tahsis edebilmesidir.
* **Broad network access (Geniş ağ erişimi):** Öğrencilerin ve akademisyenlerin kampüs ağından, ev internetinden veya mobil cihazlardan standart web protokolleriyle sisteme kesintisiz erişebilmesidir.
* **Resource pooling (Kaynak havuzlama):** Sağlayıcının çok kiracılı fiziksel sunucu havuzunu dinamik paylaştırarak, üniversitenin kayıt sabahı ihtiyaç duyduğu yüksek işlem gücünü ortak altyapıdan sağlamasıdır.
* **Rapid elasticity (Hızlı esneklik):** Kayıt sabahı 09:00'da artan yük karşısında uygulama sunucularının otomatik olarak 3'ten 30 örneğe fırlaması, kayıt haftası bitiminde tekrar 3 örneğe inebilmesidir [5].
* **Measured service (Ölçülebilir hizmet):** Tüketilen vCPU saati, RAM ve ağ trafiğinin ölçülerek faturalandırılması; üniversitenin tatil aylarında atıl sunucu parası ödemeyip yalnızca tükettiği kaynak kadar ödeme yapmasıdır.

---

### 5. Hizmet Modeli Seçimi ve Gerekçesi
Bulut hizmet modelleri kuruma farklı denetim ve yönetim sorumlulukları sunar [1], [2]:
* **IaaS:** Donanım yönetimini kaldırsa da işletim sistemi yamaları, güvenlik güncellemeleri ve küme yönetimi üniversitenin sınırlı BT personeline ağır bakım yükü bindirir.
* **SaaS:** Hazır bir yazılım sunsa da üniversitenin özelleşmiş müfredat kurallarına, çakışma algoritmalarına ve yerel entegrasyonlarına uyum sağlayamaz; yüksek sağlayıcı bağımlılığı üretir.

**Seçilen Model: PaaS (Yönetilen Konteyner / Platform) ve DBaaS (Hizmet Olarak Veritabanı)**  
Uygulama katmanı için PaaS/CaaS, veritabanı için DBaaS ve bellek içi önbellekleme mimarisi seçilmiştir.  
*Gerekçe:* Üniversite yazılım ekibi işletim sistemi ve sunucu bakımıyla vakit kaybetmeden doğrudan ders kayıt iş mantığına odaklanabilir. PaaS katmanı gelen istek yoğunluğuna göre konteynerleri milisaniyeler içinde yatayda ölçeklerken, DBaaS modeli otomatik yedekleme, çoklu kullanılabilirlik alanı (Multi-AZ) ve anlık salt-okunur kopya (read-replica) desteğiyle veri bütünlüğünü ve kesintisizliği garanti altına alır.

---

### 6. Dağıtım Modeli Seçimi ve Gerekçesi
Dağıtım modelleri veri hassasiyeti, mevzuat ve esneklik ölçütleriyle değerlendirilmiştir [1], [3]:
* **Genel Bulut:** Üstün esneklik sunar; ancak KVKK ve YÖK düzenlemeleri gereği kalıcı akademik sicil verilerinin yurt dışı veri merkezlerinde barındırılması yasal kısıtlamalara tabidir.
* **Özel Bulut:** Veri egemenliği sağlar; ancak yılda sadece birkaç gün yaşanacak tepe yük için yüzlerce sunucu satın alıp yıl boyu atıl bekletmek kamu kaynakları açısından verimsizdir.

**Seçilen Dağıtım Modeli: Hibrit Bulut (Hybrid Cloud)**  
*Gerekçe:* Bu iş yükü için en optimum çözüm hibrit buluttur. Kalıcı transkript, kimlik ve resmi sicil verileri üniversitenin kurum içi (on-premises) özel veri merkezinde tutulur. Kayıt haftasında yoğun trafiği göğüsleyen web arayüzleri, statik içerikler ve kayıt kuyrukları genel bulutun elastik ortamında çalıştırılır. İki ortam şifreli özel ağ tüneliyle (IPsec VPN / Direct Connect) bağlanır. Böylece hem veri egemenliği ve mevzuat uyumu sağlanır hem de genel bulutun sınırsız esnekliğinden yararlanılarak sistem çökmesi önlenir.

---

### 7. Ekonomik Değerlendirme
Önerilen mimari kurum içi altyapıyla ekonomik olarak karşılaştırıldığında şu sonuçlar öne çıkar [2], [4]:
* **CapEx ve OpEx Dengesi:** Geleneksel modelde tepe yükü karşılayacak donanım için yüksek sermaye harcaması (CapEx) gerekirken; bulut çözümü bu yatırımı ortadan kaldırarak kullandıkça ödenen operasyonel gidere (OpEx) dönüştürür.
* **Atıl Kapasite Riskinin Bertarafı:** Yılın %95'inde düşük çalışan bir sistemde tepe yüke göre sunucu satın almak devasa bir atıl kapasite israfıdır. Bulutun esnekliği bu israfı önler.
* **Maliyet Yanılgısı ve Riskler:** "Bulut her zaman daha ucuzdur" kabulü yanlıştır. Kayıt dönemi sonrasında ölçeklenen kaynaklar küçültülmezse (scale-in unutulursa), veri transferi (egress) izlenmezse ve gereksiz test ortamları açık bırakılırsa maliyet kurum içini aşabilir. FinOps bütçe alarmları ve otomatik kapanma kuralları zorunludur.

---

### 8. Paylaşılan Sorumlulukların Değerlendirilmesi
Önerilen PaaS ve DBaaS hibrit mimarisinde sorumluluklar sağlayıcı ve üniversite arasında şöyle paylaşılır [2], [3]:

| Sorumluluk Alanı | Bulut Sağlayıcısının Sorumluluğu | Üniversitenin (Müşterinin) Sorumluluğu |
| :--- | :--- | :--- |
| **Fiziksel Altyapı** | Veri merkezi güvenliği, sunucu donanımı, güç ve soğutma. | Sorumluluğu yoktur. |
| **İşletim Sistemi** | Sunucu işletim sisteminin kurulumu, çekirdek yamaları ve güvenliği. | Doğrudan erişimi yoktur; sorumlu değildir (PaaS avantajı). |
| **Uygulama** | Çalışma ortamı (runtime) kararlılığı ve temel platform desteği. | Ders kayıt yazılım kodu, iş kuralları ve uygulama güvenlik açıkları. |
| **Kullanıcı Hesapları & Erişim** | IAM kimlik altyapısının sürekliliği. | Öğrenci ve danışman yetkileri, roller ve çok faktörlü doğrulama (MFA). |
| **Veriler** | Depolama medyasının donanımsal dayanıklılığı ve replikasyonu. | Veri sınıflandırması, KVKK uyumu, şifreleme anahtarları ve bütünlük. |
| **Güvenlik Yapılandırmaları**| Sanal ağ ve hipervizör izolasyonu. | Güvenlik grupları, port kuralları ve Web Uygulama Güvenlik Duvarı (WAF). |
| **Yedekleme ve Güncelleme** | Otomatik snapshot ve Multi-AZ replikasyon altyapısı. | Yedekleme politikaları (RPO/RTO), felaket kurtarma ve yazılım sürümleri. |

*IaaS - PaaS Farkı:* IaaS kullanılsaydı sanal makinelerin işletim sistemi yamaları ve çekirdek güvenliği üniversiteye ait olacaktı. PaaS modelinde bu yük sağlayıcıya devredilmiş; üniversite sadece uygulama ve veriye odaklanmıştır.

---

### 9. Kontrol Düzlemi ve Veri Düzlemi Örnekleri
Sistem işlemleri iki temel düzleme ayrılır [2], [4]:
* **Kontrol Düzlemi (Control Plane) Örnekleri:**
  1. Bilgi işlem yöneticisinin kayıt sabahı öncesinde yönetim konsolundan PaaS konteyner kümesinin asgari örneğini 3'ten 25'e çıkarması ve otomatik ölçeklendirme kuralını güncellemesi.
  2. Veritabanı yöneticisinin kayıt dönemi öncesinde DBaaS üzerinde yeni bir salt-okunur kopya (read-replica) tahsis etmesi veya IAM üzerinden danışmanlara onay yetkisi tanımlaması.
* **Veri Düzlemi (Data Plane) Örnekleri:**
  1. Bir öğrencinin web tarayıcısı üzerinden bir dersin güncel kontenjan durumunu ekranda sorgulaması (SELECT veritabanı okuma işlemi).
  2. Bir öğrencinin "Dersi Ekle" butonuna tıklamasıyla kontenjan sayacının bir azaltılıp dersin öğrenci sepetine işlenmesi (INSERT/UPDATE veritabanı yazma işlemi).

---

### 10. AWS, Microsoft Azure ve Google Cloud Hizmet Karşılıkları
Sistem gereksinimlerinin üç büyük bulut sağlayıcısındaki karşılıkları Tablo 1'de listelenmiştir [2], [3], [4]:

**Tablo 1. Seçilen iş yükü için sağlayıcı bağımsız gereksinimlerin AWS, Microsoft Azure ve Google Cloud karşılıkları**

| Gereksinim / Hizmet Kategorisi | AWS Karşılığı | Microsoft Azure Karşılığı | Google Cloud Karşılığı | Sistemdeki Kullanım Amacı |
| :--- | :--- | :--- | :--- | :--- |
| **1. Yönetilen Konteyner / Platform (PaaS/CaaS)** | AWS Elastic Beanstalk / App Runner | Azure App Service / Container Apps | Google Cloud Run / App Engine | Kayıt web arayüzünün ve API servislerinin otomatik ölçeklenerek çalıştırılması. |
| **2. Yönetilen İlişkisel Veritabanı (DBaaS)** | Amazon RDS for PostgreSQL / Aurora | Azure Database for PostgreSQL | Google Cloud SQL for PostgreSQL | Öğrenci, ders ve kontenjan kayıtlarının ACID güvencesiyle saklanması. |
| **3. Yönetilen Bellek İçi Önbellek (In-Memory Cache)** | Amazon ElastiCache (Redis) | Azure Cache for Redis | Google Cloud Memorystore (Redis) | Sık sorgulanan ders listeleri, kota sayaçları ve oturumların hızlandırılması. |
| **4. Nesne Depolama (Object Storage)** | Amazon Simple Storage Service (S3) | Azure Blob Storage | Google Cloud Storage | Ders izlenceleri (syllabus), transkript PDF'leri ve statik web varlıklarının saklanması. |

*Hizmetlerin Eş Değerliği Üzerine Not:* Tablodaki ürünler aynı ihtiyacı karşılasa da bire bir eş değer kabul edilmemelidir. Konteynerlerin sıfıra ölçeklenme davranışı (scale-to-zero), veritabanı replikasyon gecikmeleri, Türkiye'ye olan ağ gecikmesi (latency), SLA taahhütleri ve fiyatlandırma modelleri farklıdır. Seçim ürün adına göre değil, teknik gereksinimlere göre yapılmalıdır.

---

### 11. Sonuç ve Öneri
Teknik, ekonomik ve yönetsel analizlerin özeti şöyledir:
* **Seçilen Hizmet Modelleri:** PaaS (Uygulama), DBaaS (Veritabanı), Bellek İçi Önbellek ve Nesne Depolama.
* **Seçilen Dağıtım Modeli:** Hibrit Bulut (Hybrid Cloud).
* **En Önemli İki Yarar:**
  1. *Kesintisiz Esneklik:* Kayıt sabahlarındaki aşırı trafik dalgalanmalarında otomatik genişleyerek sistem çökmesini ve öğrenci mağduriyetini önlemesi.
  2. *Atıl Kapasite Maliyetinin Sıfırlanması:* Yılın %95'lik sakin döneminde gereksiz sunucu yatırımı ve bakım maliyetlerinden tasarruf sağlaması.
* **En Önemli İki Risk ve Sınırlılık:**
  1. *FinOps ve Maliyet Riski:* Kayıt sonrasında kaynakların küçültülmemesi veya kontrolsüz veri transferi sonucu yüksek fatura oluşması riski.
  2. *Hibrit Ağ ve Mevzuat Karmaşıklığı:* Kurum içi altyapı ile genel bulut arasındaki şifreli ağın yönetimi ve KVKK uyum süreçlerinin getirdiği yönetsel zorluklar.
* **Kurum Bu İş Yükünü Buluta Taşımalı mıdır?**  
  **Kesin Karar: Evet, taşımalıdır.**  
  *Teknik Gerekçe:* Yıl içine dengesiz dağılan döngüsel tepe yükler geleneksel donanım mimarileriyle verimli yönetilemez.  
  *Ekonomik Gerekçe:* Yılda sadece 10 gün çalışacak sunucuların 5 yıllık amortisman ve bakım maliyetini peşin ödemek kamu kaynaklarını israf etmektir.  
  *Yönetsel Gerekçe:* Hibrit mimari sayesinde hassas veriler kurum içinde korunurken, BT ekibi donanım ve işletim sistemi yamaları yerine eğitim yazılımlarının geliştirilmesine odaklanabilecektir.

---

### 12. Kaynakça
[1] Mell, P., & Grance, T. (2011). *The NIST Definition of Cloud Computing* (Special Publication 800-145). National Institute of Standards and Technology (NIST), U.S. Department of Commerce. https://doi.org/10.6028/NIST.SP.800-145  
[2] Amazon Web Services. (2024). *Shared Responsibility Model and Cloud Architecture Center*. AWS Documentation. https://aws.amazon.com/compliance/shared-responsibility-model/  
[3] Microsoft Learn. (2024). *Shared Responsibility in the Cloud & Azure Architecture Center*. Microsoft Technical Documentation. https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility  
[4] Google Cloud. (2024). *Google Cloud Architecture Framework: Security, Scalability, and System Design*. Google Cloud Documentation. https://cloud.google.com/architecture/framework  
[5] Armbrust, M., Fox, A., Griffith, R., Joseph, A. D., Katz, R., Konwinski, A., Lee, G., Patterson, D., Rabkin, A., Stoica, I., & Zaharia, M. (2010). *A View of Cloud Computing*. Communications of the ACM, 53(4), 50-58. https://doi.org/10.1145/1721654.1721672
