# YAZLAB-II Mikroservis Projesi

Bu proje, FastAPI, MongoDB, Docker ve Grafana kullanılarak geliştirilmiş bir mikroservis mimarisi uygulamasıdır.

## Mimari
````mermaid
graph TD
    Client["React Frontend"]
    Dispatcher["Dispatcher Service (8003)"]
    Auth["Auth Service (8000)"]
    Product["Product Service (8001)"]
    Order["Order Service (8002)"]
    MongoDB[("MongoDB")]
    Prometheus["Prometheus (9090)"]
    Grafana["Grafana (3000)"]

    Client --> Dispatcher
    Dispatcher --> Auth
    Dispatcher --> Product
    Dispatcher --> Order
    Auth --> MongoDB
    Product --> MongoDB
    Order --> MongoDB
    Prometheus --> Auth
    Prometheus --> Product
    Prometheus --> Order
    Prometheus --> Dispatcher
    Grafana --> Prometheus
````

## Servisler

| Servis | Port | Açıklama |
|---|---|---|
| Auth Service | 8000 | Kullanıcı kayıt, giriş ve token doğrulama |
| Product Service | 8001 | Ürün listeleme ve ekleme |
| Order Service | 8002 | Sipariş oluşturma ve listeleme |
| Dispatcher | 8003 | API Gateway, tüm istekleri yönlendirir |
| MongoDB | 27017 | Veritabanı |
| Prometheus | 9090 | Metrik toplama |
| Grafana | 3000 | Trafik görselleştirme |

## Kurulum

### Gereksinimler
- Docker Desktop
- Node.js (React arayüzü için)

### Çalıştırma
````bash
# Servisleri başlat
docker compose up --build

# React arayüzünü başlat (ayrı terminalde)
cd frontend
npm start
````

## API Akışı
````mermaid
sequenceDiagram
    participant C as React Client
    participant D as Dispatcher
    participant A as Auth Service
    participant P as Product Service
    participant O as Order Service

    C->>D: POST /auth/login
    D->>A: Token dogrula
    A-->>D: Token gecerli
    D-->>C: Access token

    C->>D: GET /products (Bearer token)
    D->>A: Token dogrula
    A-->>D: Kullanici bilgisi
    D->>P: GET /products
    P-->>D: Urun listesi
    D-->>C: Urunler

    C->>D: POST /orders (Bearer token)
    D->>A: Token dogrula
    D->>O: Siparis olustur
    O-->>D: Siparis bilgisi
    D-->>C: Siparis sonucu
````

## Yuk Testi

Locust ile yuk testi yapmak icin:
````bash
locust -f locustfile.py
````

Tarayicidan `http://localhost:8089` adresine giderek test parametrelerini ayarlayabilirsiniz.

## Teknolojiler

- **FastAPI** — Python web framework
- **MongoDB** — NoSQL veritabani
- **Docker & Docker Compose** — Konteynerizasyon
- **Prometheus** — Metrik toplama
- **Grafana** — Gorsellestirme
- **Locust** — Yuk testi
- **React** — Frontend arayuzu
````
````