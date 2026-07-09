# London Project API

---

## Русский

### Описание

REST API + Django Templates для сайта ресторана "London Grill House".  
Реализованы: меню (категории + блюда), новости, форма обратной связи, страница "О нас", авторизация (JWT + session).

### Технологии

- Django 6+
- Django REST Framework
- JWT (SimpleJWT) + Django Session Auth
- Django Templates (серверный рендеринг)
- drf-spectacular (Swagger/ReDoc)
- PostgreSQL (dev — SQLite)
- Docker

### Быстрый старт

```bash
git clone <repo-url>
cd exam_project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

### Страницы сайта

| URL | Описание |
|---|---|
| `/pages/` | Главная страница |
| `/pages/menu/` | Меню (все блюда) |
| `/pages/menu/<id>/` | Меню (по категории) |
| `/pages/news/` | Новости |
| `/pages/news/<id>/` | Детали новости |
| `/pages/about/` | О нас |
| `/pages/contact/` | Контакты (форма) |
| `/login/` | Вход |
| `/register/` | Регистрация |
| `/logout/` | Выход |

### API Endpoints

| Метод | URL | Описание |
|---|---|---|
| POST | `/api/auth/register/` | Регистрация |
| POST | `/api/auth/login/` | Получить JWT |
| POST | `/api/auth/refresh/` | Обновить JWT |
| GET/POST | `/api/menu/categories/` | Список/создание категорий |
| GET/PUT/DELETE | `/api/menu/categories/{id}/` | Детально категорию |
| GET/POST | `/api/menu/dishes/` | Список/создание блюд |
| GET/PUT/DELETE | `/api/menu/dishes/{id}/` | Детально блюдо |
| GET/POST | `/api/news/` | Список/создание новостей |
| GET/PUT/DELETE | `/api/news/{id}/` | Детально новость |
| GET/POST | `/api/contact/` | Отправить/список сообщений |
| GET/PUT | `/api/about/` | Получить/обновить "О нас" |
| GET | `/api/schema/` | OpenAPI schema |
| GET | `/api/docs/` | Swagger UI |
| GET | `/api/redoc/` | ReDoc UI |

### Структура проекта

```
exam_project/
├── config/           # Настройки Django (settings, urls, page_views)
├── accounts/         # Пользователи, JWT, регистрация
├── menu/             # Категории и блюда
├── news/             # Новости
├── contact/          # Контакты (форма обратной связи)
├── about/            # О нас
├── templates/        # Django шаблоны
│   ├── base.html     # Базовый шаблон (header, footer)
│   └── pages/        # Страницы сайта
├── static/           # Статические файлы (CSS, JS)
├── manage.py
└── requirements.txt
```

---

## O'zbekcha

### Tavsif

"London Grill House" restorani sayti uchun REST API + Django Templates.  
Amalga oshirilgan: menyu (kategoriyalar + taomlar), yangiliklar, aloqa formasi, "Biz haqimizda" sahifasi, JWT + session autentifikatsiya.

### Texnologiyalar

- Django 6+
- Django REST Framework
- JWT (SimpleJWT) + Django Session Auth
- Django Templates (server-side rendering)
- drf-spectacular (Swagger/ReDoc)
- PostgreSQL (dev — SQLite)
- Docker

### Tez boshlash

```bash
git clone <repo-url>
cd exam_project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

### Sahifalar

| URL | Tavsif |
|---|---|
| `/pages/` | Bosh sahifa |
| `/pages/menu/` | Menyu (barcha taomlar) |
| `/pages/menu/<id>/` | Menyu (kategoriya bo'yicha) |
| `/pages/news/` | Yangiliklar |
| `/pages/news/<id>/` | Yangilik detali |
| `/pages/about/` | Biz haqimizda |
| `/pages/contact/` | Aloqa (forma) |
| `/login/` | Kirish |
| `/register/` | Ro'yxatdan o'tish |
| `/logout/` | Chiqish |

### API Manzillari

| Metod | URL | Tavsif |
|---|---|---|
| POST | `/api/auth/register/` | Ro'yxatdan o'tish |
| POST | `/api/auth/login/` | JWT olish |
| POST | `/api/auth/refresh/` | JWT yangilash |
| GET/POST | `/api/menu/categories/` | Kategoriyalar ro'yxati/yaratish |
| GET/PUT/DELETE | `/api/menu/categories/{id}/` | Kategoriya detali |
| GET/POST | `/api/menu/dishes/` | Taomlar ro'yxati/yaratish |
| GET/PUT/DELETE | `/api/menu/dishes/{id}/` | Taom detali |
| GET/POST | `/api/news/` | Yangiliklar ro'yxati/yaratish |
| GET/PUT/DELETE | `/api/news/{id}/` | Yangilik detali |
| GET/POST | `/api/contact/` | Xabar yuborish/ro'yxat |
| GET/PUT | `/api/about/` | "Biz haqimizda" olish/yangilash |
| GET | `/api/schema/` | OpenAPI sxemasi |
| GET | `/api/docs/` | Swagger UI |
| GET | `/api/redoc/` | ReDoc UI |

### Loyiha tuzilishi

```
exam_project/
├── config/           # Django sozlamalari (settings, urls, page_views)
├── accounts/         # Foydalanuvchilar, JWT, ro'yxatdan o'tish
├── menu/             # Kategoriyalar va taomlar
├── news/             # Yangiliklar
├── contact/          # Aloqa (feedback formasi)
├── about/            # Biz haqimizda
├── templates/        # Django shablonlar
│   ├── base.html     # Asosiy shablon (header, footer)
│   └── pages/        # Sayt sahifalari
├── static/           # Statik fayllar (CSS, JS)
├── manage.py
└── requirements.txt
```

---

## Лицензия / Litsenziya

MIT
