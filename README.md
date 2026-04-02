# Mikroservis Mimarisi ile API Gateway Uygulamasi

**Ders:** Yazilim Gelistirme Laboratuvari-II  
**Universite:** Kocaeli Universitesi, Teknoloji Fakultesi, Bilisim Sistemleri Muhendisligi  
**Takim Uyeleri:** Gizemnur Arslan (231307024), Umut Sahin (231307091)  
**Tarih:** 5 Nisan 2026

---

## 1. Giris

### Problemin Tanimi

Modern yazilim sistemlerinde monolitik mimariler, olceklenebilirlik, bagimsiz deploy edilebilirlik ve hata izolasyonu konularinda ciddi kisitlamalar ortaya koymaktadir. Bu proje, bu sorunlara cozum olarak mikroservis mimarisini benimsemekte ve tum dis istekleri merkezi bir Dispatcher (API Gateway) uzerinden yoneten, guvenli ve olceklenebilir bir uygulama sunmaktadir.

### Amac

Bu projenin temel amaci; bagimsiz calisabilen mikroservisler gelistirmek, bu servisleri tek bir giris noktasindan yoneten bir Dispatcher tasarlamak, TDD (Test-Driven Development) disipliniyle kod kalitesini artirmak ve Docker ile tum mimarinin tek komutla ayaga kalkmasini saglamaktir.

---

## 2. Sistem Tasarimi

### Richardson Olgunluk Modeli (RMM)

Richardson Olgunluk Modeli, REST API'lerin ne kadar olgun oldugunu olcen bir modeldir. Bu projede **Seviye 2** uygulanmistir.

- **Seviye 0:** Tek URL, tek metot
- **Seviye 1:** Kaynaklar URI uzerinden tanimlanir
- **Seviye 2 (Bu Proje):** HTTP metotlari dogru kullanilir (GET, POST, PUT, DELETE) ve dogru HTTP durum kodlari dondurulur
- **Seviye 3:** HATEOAS (Hypertext as the Engine of Application State)

Bu projede tum kaynaklar URI uzerinden tanimlanmis, islemler uygun HTTP metotlari ile gerceklestirilmis ve hatali durumlarda 401, 403, 404, 500 gibi dogru HTTP durum kodlari kullanilmistir.

### Mikroservis Mimarisi
```mermaid
graph TD
    Client["React Frontend (3001)"]
    Dispatcher["Dispatcher Service (8003)"]
    Auth["Auth Service (8000)"]
    Product["Product Service (8001)"]
    Order["Order Service (8002)"]
    MongoDB_Auth[("auth_db")]
    MongoDB_Product[("product_db")]
    MongoDB_Order[("order_db")]
    MongoDB_Dispatcher[("dispatcher_db")]
    Prometheus["Prometheus (9090)"]
    Grafana["Grafana (3000)"]

    Client --> Dispatcher
    Dispatcher --> Auth
    Dispatcher --> Product
    Dispatcher --> Order
    Auth --> MongoDB_Auth
    Product --> MongoDB_Product
    Order --> MongoDB_Order
    Dispatcher --> MongoDB_Dispatcher
    Prometheus --> Auth
    Prometheus --> Product
    Prometheus --> Order
    Prometheus --> Dispatcher
    Grafana --> Prometheus
```

### Sinif Yapilari

#### Auth Service
```mermaid
classDiagram
    class RegisterRequest {
        +EmailStr email
        +str password
        +str full_name
        +str role
    }
    class RegisterResponse {
        +str message
        +str user_id
        +EmailStr email
        +str role
    }
    class LoginRequest {
        +EmailStr email
        +str password
    }
    class LoginResponse {
        +str message
        +str access_token
        +str token_type
    }
    class VerifyResponse {
        +bool valid
        +str user_id
        +EmailStr email
        +str role
    }
```

#### Order Service
```mermaid
classDiagram
    class OrderItemRequest {
        +str product_id
        +int quantity
    }
    class OrderCreateRequest {
        +str user_id
        +List items
    }
    class OrderItemResponse {
        +str product_id
        +str product_name
        +float unit_price
        +int quantity
        +float line_total
    }
    class OrderResponse {
        +str id
        +str user_id
        +List items
        +float total_price
        +str status
    }
```

#### Product Service
```mermaid
classDiagram
    class ProductResponse {
        +str id
        +str name
        +str description
        +float price
        +int stock
        +str category
        +bool is_active
    }
    class ProductCreateRequest {
        +str name
        +str description
        +float price
        +int stock
        +str category
        +bool is_active
    }
```

### Sequence Diyagramlari

#### Login Akisi
```mermaid
sequenceDiagram
    participant C as React Client
    participant D as Dispatcher
    participant A as Auth Service
    participant DB as auth_db

    C->>D: POST /auth/login
    D->>A: POST /auth/login
    A->>DB: Kullanici sorgula
    DB-->>A: Kullanici bilgisi
    A-->>D: JWT Token
    D-->>C: access_token
```

#### Urun Listeleme Akisi
```mermaid
sequenceDiagram
    participant C as React Client
    participant D as Dispatcher
    participant A as Auth Service
    participant P as Product Service

    C->>D: GET /products (Bearer token)
    D->>A: POST /auth/verify
    A-->>D: Kullanici bilgisi
    D->>P: GET /products
    P-->>D: Urun listesi
    D-->>C: user + products
```

#### Siparis Olusturma Akisi
```mermaid
sequenceDiagram
    participant C as React Client
    participant D as Dispatcher
    participant A as Auth Service
    participant P as Product Service
    participant O as Order Service

    C->>D: POST /orders (Bearer token)
    D->>A: POST /auth/verify
    A-->>D: Kullanici bilgisi
    D->>O: POST /orders (user_id eklenir)
    O->>P: GET /products (stok kontrol)
    P-->>O: Urun bilgisi
    O->>P: PATCH /products/{id}/stock
    O-->>D: Siparis bilgisi
    D-->>C: Siparis sonucu
```

---

## 3. Proje Yapisi ve Moduller

```
WebApplication1/
├── docker-compose.yml
├── prometheus.yml
├── locustfile.py
├── auth-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── routes.py
│   ├── models.py
│   └── database.py
├── product-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── routes.py
│   ├── models.py
│   └── database.py
├── order-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── routes.py
│   ├── models.py
│   └── database.py
├── dispatcher/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── database.py
│   ├── auth_client.py
│   ├── product_client.py
│   ├── order_client.py
│   └── test_dispatcher.py
└── frontend/
    └── src/
        └── components/
            ├── Login.js
            ├── Register.js
            ├── Dashboard.js
            ├── Products.js
            ├── Orders.js
            ├── CreateOrder.js
            ├── AddProduct.js
            ├── Logs.js
            └── Monitoring.js
```

### Servisler

| Servis | Port | Veritabani | Aciklama |
|---|---|---|---|
| Auth Service | 8000 | auth_db | Kullanici kayit, giris, token dogrulama |
| Product Service | 8001 | product_db | Urun listeleme, ekleme, stok guncelleme |
| Order Service | 8002 | order_db | Siparis olusturma ve listeleme |
| Dispatcher | 8003 | dispatcher_db | API Gateway, yetkilendirme, log tutma |
| MongoDB | 27017 | - | NoSQL veritabani |
| Prometheus | 9090 | - | Metrik toplama |
| Grafana | 3000 | - | Trafik gorsellestirme |

### Network Izolasyonu

Projede iki ayri Docker networku tanimlanmistir. Sadece Dispatcher ve Grafana dis dunyaya acikken diger tum servisler yalnizca ic agda calismaktadir.

```mermaid
graph TD
    Internet["Dis Dunya"]
    Dispatcher["Dispatcher (8003)"]
    Grafana["Grafana (3000)"]
    Auth["Auth Service"]
    Product["Product Service"]
    Order["Order Service"]
    MongoDB["MongoDB"]
    Prometheus["Prometheus"]

    Internet -->|public-net| Dispatcher
    Internet -->|public-net| Grafana
    Dispatcher -->|private-net| Auth
    Dispatcher -->|private-net| Product
    Dispatcher -->|private-net| Order
    Auth -->|private-net| MongoDB
    Product -->|private-net| MongoDB
    Order -->|private-net| MongoDB
    Prometheus -->|private-net| Auth
    Prometheus -->|private-net| Product
    Prometheus -->|private-net| Order
    Prometheus -->|private-net| Dispatcher
```

---

## 4. Kurulum ve Calistirma

### Gereksinimler
- Docker Desktop
- Node.js

### Calistirma

```bash
# Servisleri baslat
docker compose up --build

# React arayuzunu baslat (ayri terminalde)
cd frontend
npm start

# Yuk testi (ayri terminalde)
locust -f locustfile.py
```

---

## 5. Uygulama Ekran Goruntuleri ve Test Sonuclari

### React Arayuzu

**Urunler Sayfasi** — Admin rolüyle giris yapildiktan sonra urun listesi goruntulenmektedir.

![Urunler](docs/WhatsApp%20Image%202026-04-02%20at%2015.07.20.jpeg)

**Urun Ekle Sayfasi** — Yalnizca admin rolundeki kullanicilar urun ekleyebilmektedir.

![Urun Ekle](docs/WhatsApp%20Image%202026-04-02%20at%2015.07.20%20(1).jpeg)

**Trafik Loglari** — Dispatcher uzerinden gecen tum istekler zaman, method, path, kullanici ve HTTP status bilgileriyle loglanmaktadir.

![Trafik Loglari](docs/WhatsApp%20Image%202026-04-02%20at%2015.06.04.jpeg)

### API Dokumantasyonu

**Dispatcher Swagger UI** — Dispatcher servisi 8003 portundan dis dunyaya aciktir ve FastAPI otomatik dokumantasyonu sunmaktadir.

![Dispatcher Swagger](docs/WhatsApp%20Image%202026-04-02%20at%2013.38.59.jpeg)

**Auth Service (Erisim Engellendi)** — Auth servisi yalnizca ic agda (private-net) calistigindan dogrudan erisim mumkun degildir. Bu, network izolasyonunun calismakta oldugunu kanitlamaktadir.

![Auth Service Erisim Engellendi](docs/WhatsApp%20Image%202026-04-02%20at%2013.38.58.jpeg)

### Grafana Izleme

**HTTP Requests Total** — Prometheus metrikleri Grafana uzerinden gercek zamanli olarak izlenmektedir. Yuk testi sirasinda tum servislerin trafigi gorsellestirilmistir.

![Grafana Dashboard](docs/WhatsApp%20Image%202026-04-02%20at%2015.05.02.jpeg)

### TDD - Dispatcher Testleri

Dispatcher servisi TDD (Red-Green-Refactor) yaklasimi ile gelistirilmistir. Test dosyasinin zaman damgasi fonksiyonel koddan oncedir.

```bash
cd dispatcher
pytest test_dispatcher.py
```

### Yuk Testi Sonuclari

Locust ile farkli kullanici seviyelerinde yuk testi gerceklestirilmistir. Tum testlerde hata orani **%0** olarak gerceklesmistir.

**10 Kullanici — RPS: 4.88**

![Locust 10 Kullanici](docs/WhatsApp%20Image%202026-04-02%20at%2013.39.01.jpeg)

**50 Kullanici — RPS: 18.5**

![Locust 50 Kullanici](docs/WhatsApp%20Image%202026-04-02%20at%2013.39.00.jpeg)

**100 Kullanici — RPS: 26.1**

![Locust 100 Kullanici](docs/WhatsApp%20Image%202026-04-02%20at%2013.38.59%20(1).jpeg)

**200 Kullanici — RPS: 93.7**

![Locust 200 Kullanici](docs/WhatsApp%20Image%202026-04-02%20at%2013.55.53.jpeg)

**500 Kullanici — RPS: 51.4**

![Locust 500 Kullanici](docs/WhatsApp%20Image%202026-04-02%20at%2013.56.54.jpeg)

#### Yuk Testi Ozet Tablosu

| Kullanici | RPS | Hata Orani | Ort. Yanis Suresi |
|---|---|---|---|
| 10 | 4.88 | %0 | 120 ms |
| 50 | 18.5 | %0 | 129 ms |
| 100 | 26.1 | %0 | 644 ms |
| 200 | 93.7 | %0 | 173 ms |
| 500 | 51.4 | %0 | 682 ms |

#### Yorum

10 ve 50 kullanici seviyesinde sistem stabil calismis, yanis sureleri dusuk kalmistir. 100 kullanicida RPS artmaya devam etmis ancak yanis suresi 644ms'ye yukselmeye baslamistir. Tum testlerde hata orani %0 olarak gerceklesmistir.

---

## 6. Sonuc ve Tartisma

### Basarilar

- Mikroservis mimarisi basariyla gerceklendi, her servis bagimsiz olarak calisabilmektedir.
- Dispatcher uzerinden merkezi yetkilendirme saglanmis, ic servisler dis dunyaya kapali tutulmustur.
- TDD yaklasimi ile dispatcher servisi gelistirilmis, tum testler basariyla gecmektedir.
- Docker Compose ile tum mimari tek komutla ayaga kalkmaktadir.
- Prometheus ve Grafana ile gercek zamanli trafik izleme saglanmistir.
- Admin/kullanici rol ayrimli React arayuzu gelistirilmistir.

### Sinirliliklar

- Stok guncelleme islemleri atomik degildir, cok yuksek es zamanli isteklerde tutarsizlik olusabilir.
- Servisler arasi iletisimde retry mekanizmasi bulunmamaktadir.
- JWT token suresi doldugundan otomatik yenileme (refresh token) yoktur.

### Olasi Gelistirmeler

- Redis ile token blacklist ve cache mekanizmasi eklenebilir.
- Servisler arasi iletisimde message queue (RabbitMQ/Kafka) kullanilabilir.
- Kubernetes ile orkestrasyon saglanabilir.
- HTTPS ve SSL sertifikasi eklenebilir.

---

## Teknolojiler

- **FastAPI** - Python web framework
- **MongoDB** - NoSQL veritabani
- **Docker & Docker Compose** - Konteynerizasyon
- **Prometheus** - Metrik toplama
- **Grafana** - Gorsellestirme
- **Locust** - Yuk testi
- **React** - Frontend arayuzu
- **JWT** - Kimlik dogrulama
- **Pytest** - TDD test framework
