## YAZLAB-II PROJESİ
# Projenin Mimarisi


mikroservis-proje/
│
├── dispatcher/
│   ├── app/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── auth-service/
│   ├── app/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── product-service/
│   ├── app/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── order-service/
│   ├── app/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── infra/
│   ├── grafana/
│   ├── prometheus/
│   └── locust/
│
├── docker-compose.yml
└── README.md







WebApplication1/
├── docker-compose.yml          
├── auth-service
│   ├── Dockerfile              
│   ├── requirements.txt        
│   └── database.py             
├── product-service
│   ├── Dockerfil
│   ├── requirements.tx
│   └── database.py             
├── order-service
│   ├── Dockerfil
│   ├── requirements.tx
│   ├── database.py             
│   └── routes.py               
└── dispatcher
    ├── Dockerfil
    ├── requirements.tx
    ├── auth_client.py          
    ├── product_client.py       
    └── order_client.py         