# London Project API

---

## 🇷🇺 Русский

### Описание

REST API для сайта ресторана "London Project".  
Реализованы: меню (категории + блюда), новости, форма обратной связи, страница "О нас", авторизация по JWT.

### Технологии

- Django 5+
- Django REST Framework
- JWT (SimpleJWT)
- drf-spectacular (Swagger/ReDoc)
- PostgreSQL (dev — SQLite)
- Docker

### Быстрый старт

```bash
# 1. Клонировать репозиторий
git clone <repo-url>
cd london_project

# 2. Создать виртуальное окружение и установить зависимости
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
pip install -r requirements.txt

# 3. Настроить .env
cp .env.example .env

# 4. Миграции и запуск
python manage.py migrate
python manage.py runserver
```

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

### Деплой (Railway)

Проект полностью настроен для деплоя на [Railway](https://railway.app/):
1. Создайте проект и добавьте базу данных **PostgreSQL**.
2. Подключите ваш GitHub репозиторий.
3. В настройках сервиса (Variables) добавьте следующие переменные:
   - `SECRET_KEY` (ваша секретная строка)
   - `DEBUG=False`
   - `ALLOWED_HOSTS=*`
   - `CSRF_TRUSTED_ORIGINS=https://<your-app-domain>.railway.app`
   - `DATABASE_URL` (строка подключения к базе данных, выдается Railway)
4. Railway автоматически соберет образ из `Dockerfile`, применит статику через `whitenoise` и запустит сервер с помощью Gunicorn.

### Структура проекта

```
london_project/
├── config/       # Настройки Django (settings, urls, wsgi, asgi)
├── accounts/     # Пользователи и JWT (register/login/refresh)
├── menu/         # Категории и блюда
├── news/         # Новости
├── contact/      # Контакты (форма обратной связи)
├── about/        # О нас
├── manage.py
└── requirements.txt
```

---

## 🇺🇿 O'zbekcha

### Tavsif

"London Project" restorani sayti uchun REST API.  
Amalga oshirilgan: menyu (kategoriyalar + taomlar), yangiliklar, aloqa formasi, "Biz haqimizda" sahifasi, JWT orqali autentifikatsiya.

### Texnologiyalar

- Django 5+
- Django REST Framework
- JWT (SimpleJWT)
- drf-spectacular (Swagger/ReDoc)
- PostgreSQL (dev — SQLite)
- Docker

### Tez boshlash

```bash
# 1. Repositoriyani klonlash
git clone <repo-url>
cd london_project

# 2. Virtual muhit yaratish va kutubxonalarni o'rnatish
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
pip install -r requirements.txt

# 3. .env sozlamalari
cp .env.example .env

# 4. Migratsiyalar va ishga tushirish
python manage.py migrate
python manage.py runserver
```

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

### Deploy (Railway)

Loyiha [Railway](https://railway.app/) ga yuklash uchun to'liq moslashtirilgan:
1. Loyiha yarating va **PostgreSQL** ma'lumotlar bazasini qo'shing.
2. GitHub repositoriyni ulang.
3. Xizmat sozlamalarida (Variables) quyidagi o'zgaruvchilarni qo'shing:
   - `SECRET_KEY` (maxfiy kalit)
   - `DEBUG=False`
   - `ALLOWED_HOSTS=*`
   - `CSRF_TRUSTED_ORIGINS=https://<your-app-domain>.railway.app`
   - `DATABASE_URL` (Railway beradigan bazaga ulanish havolasi)
4. Railway avtomatik ravishda `Dockerfile` orqali build qiladi, `whitenoise` yordamida statik fayllarni yig'adi va Gunicorn orqali serverni ishga tushiradi.

### Loyiha tuzilishi

```
london_project/
├── config/       # Django sozlamalari (settings, urls, wsgi, asgi)
├── accounts/     # Foydalanuvchilar va JWT (register/login/refresh)
├── menu/         # Kategoriyalar va taomlar
├── news/         # Yangiliklar
├── contact/      # Aloqa (feedback formasi)
├── about/        # Biz haqimizda
├── manage.py
└── requirements.txt
```

---

## Лицензия / Litsenziya

MIT
