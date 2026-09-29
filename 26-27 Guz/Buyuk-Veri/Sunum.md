# Büyük Veri İşleme Çerçevelerinin Karşılaştırmalı Analizi
**Makale Adı:** *A Comparative Analysis of Big Data Frameworks: An Adoption Perspective*  
**Yazarlar:** Madiha Khalid, Muhammad Murtaza Yousaf (Applied Sciences, 2021)  
**Sunum Süresi:** ~10 Dakika (11 Sayfa, Sayfa başına ~50-60 saniye)

---

## 1. Sayfa: Giriş ve Araştırmanın Amacı

1. Dijital dönüşüm, sosyal medya, web uygulamaları ve IoT cihazları nedeniyle üretilen veri miktarı katlanarak artmaktadır.
2. Geleneksel veritabanları ve ilişkisel sistemler, bu devasa veri hacmi ve veri hızı karşısında yetersiz kalmaktadır.
3. Bu darboğazı aşmak için açık kaynak dünyasında çok sayıda dağıtık büyük veri işleme çerçevesi (framework) geliştirilmiştir.
4. Bu akademik makale; en popüler beş büyük veri çerçevesini kapsamlı, tarafsız ve sistematik bir yaklaşımla karşılaştırmaktadır.
5. Çalışmanın temel amacı, yazılım mimarlarına ve araştırmacılara projeleri için en doğru teknolojiyi seçmelerinde rehberlik etmektir.
6. Literatürdeki parçalı ve dağınık kıyaslamaların aksine, bu çalışma tüm çerçeveleri tutarlı bir çerçeve altında toplamıştır.
7. 10 dakikalık bu sunumda; sistemlerin mimarilerini, performanslarını, hata toleranslarını ve hangi senaryoda hangisinin seçilmesi gerektiğini inceleyeceğiz.

> **Konuşmacı Notu (00:00 - 01:00):** Girişte dinleyicilere veri patlamasından bahsedin ve şirketlerin/geliştiricilerin neden tek bir araç yerine farklı büyük veri araçlarına ihtiyaç duyduğunu vurgulayın.

---

## 2. Sayfa: Büyük Veri Çerçevelerinin Dört Temel Gereksinimi

1. Dağıtık bir büyük veri çerçevesinin başarısı, veri yükünü arka planda nasıl organize ettiğine bağlıdır.
2. Makale, bir büyük veri çerçevesinin taşıması gereken özellikleri dört ana boyutta tanımlamaktadır.
3. Birincisi **Mimari Gereksinimler**dir; verinin düğümlere nasıl dağıtılacağını, depolanacağını ve kümenin nasıl yönetileceğini belirler.
4. İkincisi **Veri İşleme Modeli**dir; sistemin veriyi yığın (batch) halinde mi yoksa gerçek zamanlı anlık akış (stream) olarak mı ele alacağını tanımlar.
5. Üçüncüsü **Çizelgeleme (Scheduling)** mekanizmasıdır; görevlerin mevcut işlemci çekirdeklerine ve sunuculara en verimli şekilde atanmasını sağlar.
6. Dördüncüsü **Hata Toleransı (Fault Tolerance)** sistemidir; binlerce sunucudan oluşan kümelerde donanım arızalarında veri kaybı olmadan çalışmayı sürdürmeyi garanti eder.
7. Bu dört temel sütun, sonraki sayfalarda inceleyeceğimiz tüm çerçevelerin çekirdek tasarımını oluşturmaktadır.

> **Konuşmacı Notu (01:00 - 02:00):** Her büyük veri sisteminin bu 4 temel problemi çözmek zorunda olduğunu dinleyicilere aktarın.

---

## 3. Sayfa: İncelenen Beş Temel Çerçeve

1. Araştırma kapsamında açık kaynak ekosisteminin en öne çıkan beş büyük veri çerçevesi seçilmiştir.
2. **Apache Hadoop:** MapReduce hesaplama modeli ve HDFS depolama katmanıyla büyük veri çağını başlatan en olgun ve öncü çerçevedir.
3. **Apache Spark:** Bellek içi (in-memory) veri işleme kabiliyetiyle Hadoop'a göre 100 kata kadar hız vadeden genel amaçlı lider çerçevedir.
4. **Apache Storm:** Twitter tarafından desteklenen, olayları anlık olarak tek tek işleyen ve son derece düşük gecikme sunan bir akış motorudur.
5. **Apache Samza:** LinkedIn tarafından geliştirilen, özellikle Apache Kafka mesajlaşma platformuyla mükemmel uyumlu çalışan durum bilgili bir akış çerçevesidir.
6. **Apache Flink:** Hem akış hem yığın veriyi "yerel akış" (native streaming) mantığıyla işleyebilen yeni nesil, yüksek performanslı hibrit bir sistemdir.
7. Bu sistemlerin hiçbiri "her işi en iyi yapan tek sistem" değildir; her birinin kendine özgü güçlü yanları vardır.

> **Konuşmacı Notu (02:00 - 03:00):** 5 aracı kısaca tanıtın. Hadoop'un dede, Spark'ın bellek kralı, Storm'un düşük gecikmeli haberci, Samza'nın Kafka dostu, Flink'in ise yeni nesil hibrit güç olduğunu belirtin.

---

## 4. Sayfa: Karşılaştırma Metodolojisi: 7 Öznitelik Vektörü

1. Makalenin literatüre en büyük özgün katkısı, çerçeveleri "7 Öznitelik Vektörü" (Feature Vectors) adı verilen mantıksal gruplarla sınıflandırmasıdır.
2. **Genel Özellikler:** Projeyi destekleyen kurumsal şirketler, sistemin olgunluk seviyesi ve desteklenen programlama dillerini inceler.
3. **Mimari Bileşenler:** Küme mimarisi, kaynak yöneticisi (YARN, Mesos vb.), depolama türü ve güvenlik protokollerini değerlendirir.
4. **Veri İşleme & Performans:** İşleme modunu (yığın/akış), gecikme (latency), işlem hacmi (throughput) ve bellek kullanımını kıyaslar.
5. **Hata Toleransı:** Düğüm çökmelerinin nasıl tespit edildiğini, verinin nasıl kurtarıldığını ve yüksek erişilebilirlik yöntemlerini inceler.
6. **Makine Öğrenmesi Desteği:** Sistemlerin yerel yapay zeka kütüphanelerini ve üçüncü parti araçlarla (H2O, SAMOA) uyumunu kapsar.
7. **Akış İşleme Yetenekleri:** Veri işleme garantilerini (at-least-once, exactly-once) ve durum yönetimini (state management) ayrıntılandırır.

> **Konuşmacı Notu (03:00 - 03:50):** Makalenin bilimsel değerinin bu 7 vektörden geldiğini, rasgele bir kıyaslama yerine mühendislik kriterleri sunulduğunu söyleyin.

---

## 5. Sayfa: Mimari Yapı ve Kaynak Yönetimi

1. Hadoop, Spark, Storm ve Flink temelde **Master-Slave (Yönetici-İşçi)** küme mimarisine dayanmaktadır.
2. Buna karşın Apache Samza, sistem genelinde merkezi bir yönetici düğüm barındırmaz ve Kafka tabanlı **Publish-Subscribe (Yayınla-Abone Ol)** mimarisiyle çalışır.
3. Kaynak yönetimi alanında Hadoop YARN ve Apache Mesos, neredeyse tüm çerçeveler tarafından standart olarak desteklenmektedir.
4. Dağıtık veri depolama katmanında HDFS (Hadoop Distributed File System), ekosistemin omurgası ve ortak paydası konumundadır.
5. Güvenlik tarafında Hadoop, Storm ve Flink endüstri standardı olan **Kerberos** kimlik doğrulama protokolünü kullanır.
6. Spark, şifre tabanlı paylaşımlı gizli anahtarlar ve Erişim Kontrol Listeleri (ACL) ile güvenlik sağlar; Samza ise dahili bir güvenlik katmanı barındırmaz.
7. Bu mimari yapı, çerçevelerin bulut ve kurum içi (on-premise) sunucularda ne kadar esnek konuşlandırılabileceğini belirler.

> **Konuşmacı Notu (03:50 - 04:40):** Samza'nın merkezi master'ı olmaması ve Kafka'ya dayanması en önemli ayırt edici mimari farktır.

---

## 6. Sayfa: Veri İşleme Modelleri ve Performans Kıyaslaması

1. Hadoop, disk tabanlı MapReduce modeliyle yalnızca yığın (batch) veri işler; ara sonuçları sürekli diske yazdığı için yüksek gecikmeye sahiptir.
2. Apache Spark, verileri RAM üzerinde saklayan RDD soyutlaması sayesinde yinelemeli hesaplamalarda Hadoop'tan 100 kat daha hızlıdır.
3. Spark akış verilerini milisaniyelik küçük parçalara bölerek **mikro-yığın (micro-batch)** yöntemiyle işler; bu nedenle saf gerçek zamanlı değildir.
4. Apache Storm ve Flink ise gelen her veriyi anında işleyen **yerel akış (native streaming)** motorlarıdır.
5. Gecikme (latency) yarışında Storm, Samza ve Flink milisaniye altı seviyelere inerek kesin bir üstünlük sağlar.
6. İşlem hacmi (throughput) tarafında ise Spark ve Flink, saniyede milyonlarca veriyi işleyebilme kapasiteleriyle öne çıkar.
7. Mühendislikte temel kural: Çok düşük gecikme istendiğinde Storm/Flink, yüksek veri çıktısı istendiğinde Spark/Flink tercih edilir.

> **Konuşmacı Notu (04:40 - 05:40):** Spark'ın mikro-yığın (micro-batch) mantığı ile Flink ve Storm'un gerçek zamanlı (native streaming) farkını vurgulayın.

---

## 7. Sayfa: Hata Toleransı ve Güvenilirlik Mekanizmaları

1. Yüzlerce düğümden oluşan dağıtık büyük veri kümelerinde donanım arızaları bir istisna değil, günlük bir gerçektir.
2. Tüm çerçeveler, çalışan düğümlerin sağlık durumunu kontrol etmek için periyodik **Heartbeat (Kalp Atışı)** sinyallerinden faydalanır.
3. Hadoop, veriyi HDFS üzerinde varsayılan olarak 3 farklı sunucuya kopyalayarak (data replication) donanım arızalarını tolere eder.
4. Spark, bellekteki verinin hangi adımlarla üretildiğini kaydeden **RDD Lineage (Soy Ağacı)** grafiği sayesinde kaybolan veriyi anında yeniden hesaplar.
5. Storm, üretilen her veri demetini (tuple) bellekten izler ve zaman aşımı durumunda kaynağa geri bildirimde bulunur.
6. Flink, sistem çalışırken hafif dağıtık anlık görüntüler (**Distributed Snapshots / Checkpoints**) alarak en düşük performans kaybıyla sistemi kurtarır.
7. Yüksek erişilebilirlik (High Availability) için tüm sistemler yedekli ana düğümler ve Apache ZooKeeper koordinasyonundan yararlanır.

> **Konuşmacı Notu (05:40 - 06:40):** Spark'ın RDD Lineage yönteminin veri kopyalamak yerine "nasıl üretildiğini hatırlama" felsefesi olduğunu ve Flink'in checkpointing mekanizmasını anlatın.

---

## 8. Sayfa: Akış İşleme Özellikleri ve Veri Garantileri

1. Gerçek zamanlı veri akışında en kritik kavramlar; veri işleme garantileri ve durum yönetimidir (state management).
2. Apache Storm ve Samza varsayılan olarak **At-least-once (En az bir kez)** garantisi sunar; bu da çökme anında bazı verilerin mükerrer işlenmesine yol açabilir.
3. Apache Spark ve Apache Flink ise finans ve e-ticaret gibi hassas alanlar için **Exactly-once (Tam olarak bir kez)** işleme garantisi verir.
4. Durum yönetimi tarafında Flink ve Samza, önceki verilerin özetini yerel veritabanlarında (RocksDB) tutabilen gelişmiş durumlu operatörlere sahiptir.
5. Flink'in devrimsel yaklaşımı, batch veriyi "sınırlandırılmış bir akış (bounded stream)", gerçek zamanlı veriyi ise "sınırsız bir akış" olarak modellemesidir.
6. Samza, Kafka tamponlarını kullanarak veri akışında tıkanma yaşanmasını önleyen **Backpressure (Geri Basınç)** problemini doğal olarak çözer.
7. Akış projelerinde veri kaybına mı yoksa mükerrer veri riskine mi tolerans gösterileceği sistem seçimini belirler.

> **Konuşmacı Notu (06:40 - 07:40):** Finansal işlemlerde "Exactly-once" garantisinin şart olduğunu, bu yüzden Flink ve Spark'ın kritik işlerde vazgeçilmez olduğunu belirtin.

---

## 9. Sayfa: Makine Öğrenmesi Desteği ve Ekosistemler

1. Büyük veri çerçevelerinin günümüzdeki en önemli kullanım alanlarından biri büyük veri üzerinde yapay zeka modelleri eğitmektir.
2. Apache Spark, bünyesinde yer alan zengin **MLlib** kütüphanesi sayesinde dağıtık makine öğrenmesinde açık ara sektör standardıdır.
3. Spark MLlib; sınıflandırma, regresyon, kümeleme, boyut indirgeme ve öneri sistemleri gibi geniş bir algoritma havuzuna sahiptir.
4. Apache Flink, benzer şekilde yerel makine öğrenmesi araçları sunan **FlinkML** kütüphanesine sahiptir ancak topluluk desteği Spark kadar geniş değildir.
5. Hadoop doğrudan küme üzerinde çalışabilen Apache Mahout, Oryx ve Weka gibi harici araç paketleri üzerinden yapay zekayı destekler.
6. Storm ve Samza'nın yerel bir ML kütüphanesi yoktur; akış verisi üzerinde öğrenme için SAMOA platformuyla entegre çalışırlar.
7. Derin öğrenme (Deep Learning) gerektiren projelerde ise H2O platformu ile entegre olabilen çerçeveler (Spark, Hadoop, Storm) öne çıkmaktadır.

> **Konuşmacı Notu (07:40 - 08:30):** Makine öğrenmesi ve yapay zeka odaklı bir sunumda Spark'ın tartışmasız liderliğini ve MLlib kütüphanesini vurgulayın.

---

## 10. Sayfa: Karar Matrisi ve Çerçeve Seçim Rehberi

1. Makalenin en değerli ve uygulanabilir çıktısı, hangi senaryoda hangi çerçevenin seçilmesi gerektiğini gösteren karar matrisidir.
2. **Hadoop Tercih Edilmeli:** Zaman kısıtı olmayan, petabaytlarca devasa verilerin gece yığınları halinde işleneceği durumlarda en kararlı ve ekonomik seçenektir.
3. **Spark Tercih Edilmeli:** Yüksek işlem hacmi aranan, yinelenen algoritmaların, makine öğrenmesinin ve mikro-akışların bir arada kullanılacağı projelerde idealdir.
4. **Storm Tercih Edilmeli:** Milisaniyeler mertebesinde aşırı düşük gecikmenin şart olduğu ve "en az bir kez" garantisinin yeterli görüldüğü saf akışlarda seçilmelidir.
5. **Samza Tercih Edilmeli:** Farklı mühendislik ekiplerinin aynı Kafka veri akışlarına farklı işlem aşamalarında erişmesi gereken büyük kurumsal boru hatlarında uygundur.
6. **Flink Tercih Edilmeli:** Hem aşırı düşük gecikme hem de kesinlikle "tam olarak bir kez" garantisi aranan, son teknoloji akış ve hibrit analitik projelerinde rakipsizdir.
7. Özetle; veri türü, gecikme toleransı ve mevcut kurumsal altyapı analiz edilmeden doğru bir teknoloji seçimi yapılamaz.

> **Konuşmacı Notu (08:30 - 09:20):** Bu sayfa sunumun doruk noktasıdır. Dinleyicilere bu 5 maddelik karar kuralını net bir şekilde aktarın.

---

## 11. Sayfa: Sonuç ve Genel Değerlendirme

1. Bu makale, literatürdeki dağınık bilgileri 7 öznitelik vektörü altında toplayarak tutarlı bir karşılaştırma standardı oluşturmuştur.
2. Hadoop, olgunluğu ve HDFS depolama altyapısıyla büyük veri ekosisteminin temeli olmayı sürdürmektedir.
3. Spark, olağanüstü hızı ve zengin ekosistemi (SQL, MLlib, GraphX) ile genel amaçlı büyük veri analitiğinde hakimiyetini korumaktadır.
4. Storm ve Samza belirli akış senaryolarında değerini kanıtlarken, Flink modern akış odaklı mimarisiyle geleceğin standardı haline gelmektedir.
5. Büyük veri çerçevesi seçimi bir "en iyi araç" arayışı değil, gecikme, işlem hacmi, karmaşıklık ve donanım maliyetleri arasındaki bir denge (trade-off) yönetimidir.
6. Makalenin sunduğu bu sistematik değerlendirme, kurumlara plansız yatırımların önüne geçecek net bir yol haritası sunmaktadır.
7. Dinlediğiniz ve vaktinizi ayırdığınız için teşekkür ederim; varsa sorularınızı yanıtlamaktan memnuniyet duyarım.

> **Konuşmacı Notu (09:20 - 10:00):** Dinleyicilere teşekkür edip soru-cevap aşamasına geçin.

---

### Hızlı Özet Tablosu (Sunum Sırasında Ekran Arkasında veya Soru-Cevapta Başvurmak İçin)

| Özellik / Çerçeve | Apache Hadoop | Apache Spark | Apache Storm | Apache Samza | Apache Flink |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **İşleme Modeli** | Yalnızca Yığın (Batch) | Yığın & Mikro-Yığın | Saf Akış (Native Stream) | Saf Akış (Native Stream) | Hibrit (Yerel Akış & Yığın) |
| **Gecikme (Latency)** | Yüksek (Dakikalar/Saatler) | Düşük (Saniyeler) | Çok Düşük (Milisaniyeler) | Çok Düşük (Milisaniyeler) | Çok Düşük (Milisaniyeler) |
| **İşlem Hacmi (Throughput)** | Yüksek | Çok Yüksek | Orta | Yüksek | Çok Yüksek |
| **Bellek İçi İşleme** | Hayır (Disk tabanlı) | Evet (RAM tabanlı) | Evet | Evet | Evet |
| **Akış Garantisi** | Yok | Exactly-Once | At-Least-Once | At-Least-Once | Exactly-Once |
| **Yerel ML Kütüphanesi** | Harici (Mahout) | MLlib (Çok Zengin) | Yok (SAMOA) | Yok (SAMOA) | FlinkML |
| **Mimari Model** | Master-Slave | Master-Slave | Master-Slave | Publish-Subscribe (Kafka) | Master-Slave |
| **Olgunluk Seviyesi** | Çok Yüksek | Yüksek | Yüksek | Orta | Orta / Gelişiyor |
