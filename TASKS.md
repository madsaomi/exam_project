# London Project API — Задачи для команды / Jamoa uchun vazifalar

---

## 🇷🇺 Русский раздел

---

## ✅ Что уже сделано

### Скелет проекта
- Базовая структура Django-проекта (`london_project/`)
- `config/settings.py` — настройки DRF, JWT, drf-spectacular, пагинация, фильтры
- `config/urls.py` — все роуты подключены
- `config/wsgi.py`, `config/asgi.py`

### App `accounts` — Пользователи и JWT
- Модель `CustomUser` (наследует `AbstractUser`)
- `RegisterSerializer`, `UserSerializer`
- `RegisterView` (POST — регистрация)
- endpoints: `/api/auth/register/`, `/api/auth/login/`, `/api/auth/refresh/`
- `IsAdminOrReadOnly` — кастомный permission
- Админка для пользователей

### App `menu` — Категории и блюда
- Модели: `Category` (name, description, order), `Dish` (category FK, name, description, price, image, is_available, order)
- `CategoryViewSet`, `DishViewSet` — полный CRUD
- endpoints: `/api/menu/categories/`, `/api/menu/dishes/`
- Права: `IsAdminOrReadOnly`
- Админка

### App `news` — Новости
- Модель `NewsArticle` (title, content, image, created_at, updated_at, is_published)
- `NewsArticleViewSet` — полный CRUD
- endpoint: `/api/news/`
- Права: `IsAdminOrReadOnly`
- Админка

### App `contact` — Контакты
- Модель `ContactMessage` (name, email, message, created_at, is_read)
- `ContactMessageListCreateView` (POST — любой, GET — только админ)
- endpoint: `/api/contact/`
- Админка

### App `about` — О нас
- Модель `AboutContent` (title, content, updated_at) — singleton
- `AboutContentRetrieveUpdateView` (GET — все, PUT — админ)
- endpoint: `/api/about/`
- Админка

### Инфраструктура
- `requirements.txt` со всеми зависимостями
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- OpenAPI Schema: `/api/schema/`
- `.gitignore`
- `README.md` (русский + узбекский)
- Миграции созданы и накатаны, `python manage.py check` проходит без ошибок

---

## ❗ Что осталось сделать — подробно по каждой задаче

---

### 🟥 Задача 1: CORS

**Кому:** Backend-разработчик #1
**Файлы:** `requirements.txt`, `config/settings.py`

**Что конкретно нужно сделать:**

1. Открыть `requirements.txt`, добавить строку: `django-cors-headers`
2. Установить: `pip install django-cors-headers`
3. В `config/settings.py`:
   - Добавить `'corsheaders'` в `INSTALLED_APPS` (самым первым, перед `django.contrib.admin`)
   - Добавить `'corsheaders.middleware.CorsMiddleware'` в `MIDDLEWARE` (самым первым, в самый верх списка)
4. В конец `settings.py` добавить настройки CORS. Для разработки можно так:
   ```python
   CORS_ALLOW_ALL_ORIGINS = True
   ```
   Для продакшена — строгий список:
   ```python
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
       "http://127.0.0.1:3000",
       "https://yourdomain.com",
   ]
   ```
5. Проверить: запустить сервер и убедиться, что фронтенд с другого порта может делать запросы

**Признак готовности:** фронтенд-разработчик может делать fetch-запросы к API без ошибки CORS в консоли браузера.

---

### 🟥 Задача 2: .env файлы

**Кому:** Backend-разработчик #1
**Файлы:** `.env`, `.env.example`

**Что конкретно нужно сделать:**

1. Создать файл `.env.example` в корне проекта (`london_project/.env.example`) с таким содержимым:
   ```env
   SECRET_KEY=change-me-to-random-string
   DEBUG=True
   ALLOWED_HOSTS=*

   DB_ENGINE=django.db.backends.sqlite3
   DB_NAME=db.sqlite3

   # Для PostgreSQL (раскомментировать когда будет Docker):
   # DB_ENGINE=django.db.backends.postgresql
   # DB_NAME=london_db
   # DB_USER=postgres
   # DB_PASSWORD=postgres
   # DB_HOST=db
   # DB_PORT=5432
   ```
2. Создать файл `.env` (скопировать из `.env.example`) — для локальной разработки
3. Убедиться, что в `.gitignore` есть строчка `.env` (она уже есть)
4. Сгенерировать `SECRET_KEY`. Можно через Python:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Скопировать результат в `.env`

**Признак готовности:** проект запускается без указания SECRET_KEY в коде, все настройки читаются из `.env`.

---

### 🟥 Задача 3: Docker

**Кому:** DevOps
**Файлы:** `Dockerfile`, `docker-compose.yml`, `.dockerignore`

**Что конкретно нужно сделать:**

**Dockerfile:**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**docker-compose.yml (два сервиса — web + db):**
```yaml
version: '3.9'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - .env
    volumes:
      - .:/app
      - static_volume:/app/static
      - media_volume:/app/media
    command: >
      sh -c "python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"

  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data
    env_file:
      - .env
    environment:
      - POSTGRES_DB=london_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    ports:
      - "5432:5432"

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

**.dockerignore:**
```gitignore
__pycache__
*.pyc
*.pyo
.env
.git
.gitignore
venv
.venv
*.sqlite3
```

**Дополнительно:** в `.env.example` раскомментировать PostgreSQL-переменные и добавить пояснение, что для Docker нужно использовать их.

**Признак готовности:** `docker compose up --build` поднимает проект, `python manage.py migrate` выполняется в контейнере, API доступно на `http://localhost:8000`.

---

### 🟧 Задача 4: Расширить CustomUser

**Кому:** Backend-разработчик #2
**Файлы:** `accounts/models.py`

**Что конкретно нужно сделать:**

1. Открыть `accounts/models.py`. Сейчас там:
   ```python
   class CustomUser(AbstractUser):
       pass
   ```

2. Добавить поля:
   ```python
   class CustomUser(AbstractUser):
       phone = models.CharField(
           max_length=20,
           blank=True,
           verbose_name='Телефон'
       )
       avatar = models.ImageField(
           upload_to='avatars/',
           blank=True,
           null=True,
           verbose_name='Аватар'
       )

       class Meta:
           verbose_name = 'Пользователь'
           verbose_name_plural = 'Пользователи'
   ```

3. Обновить сериализатор `accounts/serializers.py`:
   - В `RegisterSerializer` добавить поля `phone`, `avatar` в `Meta.fields`
   - В `UserSerializer` добавить `phone`, `avatar` в `Meta.fields`

4. Сделать миграции:
   ```bash
   python manage.py makemigrations accounts
   python manage.py migrate
   ```

**Признак готовности:** при регистрации можно передать `phone` и `avatar`, они сохраняются в БД.

---

### 🟧 Задача 5: DetailView для Contact

**Кому:** Backend-разработчик #2
**Файлы:** `contact/views.py`, `contact/urls.py`

**Что конкретно нужно сделать:**

1. Открыть `contact/views.py`, добавить новый класс:
   ```python
   class ContactMessageRetrieveView(generics.RetrieveAPIView):
       queryset = ContactMessage.objects.all()
       serializer_class = ContactMessageSerializer
       permission_classes = (permissions.IsAdminUser,)
   ```

2. Открыть `contact/urls.py`, добавить путь:
   ```python
   path('<int:pk>/', ContactMessageRetrieveView.as_view(), name='contact-detail'),
   ```

3. Также можно добавить `RetrieveUpdateDestroyAPIView` вместо просто `RetrieveAPIView`, если нужно, чтобы админ мог удалять сообщения или менять `is_read`. Решение за разработчиком.

**Признак готовности:**
- `GET /api/contact/1/` возвращает JSON сообщения (для админа)
- `GET /api/contact/1/` возвращает 401/403 для анонима
- `GET /api/contact/1/` возвращает 404 для несуществующего ID

---

### 🟧 Задача 6: Фильтры

**Кому:** Backend-разработчик #2
**Файлы:** `menu/views.py`, `news/views.py`, `contact/views.py`

**Что конкретно нужно сделать:**

**menu/views.py** — добавить в `DishViewSet`:
```python
filterset_fields = ('category', 'is_available')
search_fields = ('name', 'description')
ordering_fields = ('name', 'price', 'order')
```

**news/views.py** — добавить в `NewsArticleViewSet`:
```python
filterset_fields = ('is_published',)
search_fields = ('title', 'content')
ordering_fields = ('created_at', 'title')
```

**contact/views.py** — в `ContactMessageListCreateView` добавить:
```python
filterset_fields = ('is_read',)
search_fields = ('name', 'email', 'message')
ordering_fields = ('created_at',)
```

**Важно:** нужно импортировать `filterset_fields` — он работает из коробки, т.к. в `settings.py` уже подключен `DjangoFilterBackend`.

**Признак готовности:** в Swagger UI (`/api/docs/`) у каждого endpoint'а появились поля для фильтрации, поиска и сортировки. Можно сделать:
- `GET /api/menu/dishes/?category=1&search=суп&ordering=price`
- `GET /api/news/?is_published=true&search=акция`

---

### 🟧 Задача 7: Валидация уникальности блюда

**Кому:** Backend-разработчик #2
**Файлы:** `menu/models.py` или `menu/serializers.py`

**Вариант 1 (через модель — рекомендуется):**

В `menu/models.py` добавить в класс `Dish.Meta`:
```python
class Meta:
    verbose_name_plural = 'dishes'
    ordering = ('order', 'name')
    constraints = [
        models.UniqueConstraint(
            fields=['category', 'name'],
            name='unique_dish_in_category'
        )
    ]
```

Сделать миграции: `python manage.py makemigrations menu && python manage.py migrate`

**Вариант 2 (через сериализатор):**

В `menu/serializers.py` переопределить метод `validate` в `DishSerializer`:
```python
def validate(self, data):
    category = data.get('category')
    name = data.get('name')
    if category and name:
        qs = Dish.objects.filter(category=category, name=name)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                'Блюдо с таким названием уже существует в этой категории'
            )
    return data
```

**Признак готовности:** при попытке создать два блюда с одинаковым названием в одной категории — ошибка 400 с текстом.

---

### 🟩 Задача 8: Тесты accounts

**Кому:** Backend-разработчик #3
**Файлы:** `accounts/tests.py` (создать новый файл)

**Что конкретно нужно сделать:**

Создать файл `accounts/tests.py` с тест-классами:

**TestRegistration:**
- `test_register_success` — POST `/api/auth/register/` с username, email, password → 201
- `test_register_no_password` — POST без password → 400
- `test_register_duplicate_username` — дважды один username → 400

**TestLogin:**
- `test_login_success` — POST `/api/auth/login/` с верными credentials → 200 + токены
- `test_login_wrong_password` — POST с неверным паролем → 401

**TestRefresh:**
- `test_refresh_success` — POST `/api/auth/refresh/` с refresh токеном → 200
- `test_refresh_invalid` — POST с левым токеном → 401

**TestPermissions:**
- `test_anon_cannot_access_admin` — проверить, что аноним не может сделать POST/PUT/DELETE на защищённые endpoints

**Пример теста:**
```python
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class TestRegistration(APITestCase):
    def test_register_success(self):
        url = reverse('auth-register')
        data = {'username': 'testuser', 'email': 'test@test.com', 'password': 'testpass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
```

**Признак готовности:** `python manage.py test accounts` — все тесты проходят.

---

### 🟩 Задача 9: Тесты menu

**Кому:** Backend-разработчик #3
**Файлы:** `menu/tests.py` (создать новый файл)

**Что конкретно нужно сделать:**

**TestCategoryModel:**
- `test_str` — `str(category)` возвращает название
- `test_ordering` — категории сортируются по order, name

**TestCategoryAPI:**
- `test_list_categories_anon` — GET `/api/menu/categories/` → 200 (аноним может читать)
- `test_create_category_anon` — POST → 401 (аноним не может создать)
- `test_create_category_admin` — POST с админом → 201
- `test_create_category_user` — POST с обычным юзером → 403
- `test_detail_category` — GET `/{id}/` → 200
- `test_update_category_admin` — PUT с админом → 200
- `test_delete_category_admin` — DELETE с админом → 204

**TestDishAPI:**
- `test_list_dishes` — GET → 200
- `test_create_dish_admin` — POST с админом → 201
- `test_filter_by_category` — `GET ?category=1` → только блюда этой категории
- `test_search_by_name` — `GET ?search=суп` → находит по названию

**Признак готовности:** `python manage.py test menu` — все тесты проходят.

---

### 🟩 Задача 10: Тесты news

**Кому:** Backend-разработчик #3
**Файлы:** `news/tests.py` (создать новый файл)

**Что конкретно нужно сделать:**

**TestNewsArticleModel:**
- `test_str` — str возвращает title
- `test_ordering` — сортировка по created_at DESC

**TestNewsArticleAPI:**
- `test_list_news_anon` — GET → 200
- `test_create_news_anon` — POST → 401
- `test_create_news_admin` — POST → 201
- `test_detail_news_anon` — GET `/{id}/` → 200
- `test_update_news_admin` — PUT → 200
- `test_delete_news_admin` — DELETE → 204
- `test_filter_published` — `?is_published=true` → только опубликованные
- `test_search_title` — `?search=заголовок` → находит

**Признак готовности:** `python manage.py test news` — все тесты проходят.

---

### 🟩 Задача 11: Тесты contact

**Кому:** Backend-разработчик #3
**Файлы:** `contact/tests.py` (создать новый файл)

**Что конкретно нужно сделать:**

**TestContactMessageModel:**
- `test_str` — str возвращает "Имя - дата"

**TestContactMessageAPI:**
- `test_send_message_anon` — POST (любой может отправить) → 201
- `test_send_message_no_email` — POST без email → 400
- `test_list_messages_anon` — GET (аноним не может смотреть список) → 401
- `test_list_messages_admin` — GET с админом → 200
- `test_list_messages_user` — GET с обычным юзером → 403
- `test_filter_by_is_read` — `?is_read=false` (админ) → только непрочитанные

**Признак готовности:** `python manage.py test contact` — все тесты проходят.

---

### 🟩 Задача 12: Тесты about

**Кому:** Backend-разработчик #3
**Файлы:** `about/tests.py` (создать новый файл)

**Что конкретно нужно сделать:**

**TestAboutContentAPI:**
- `test_get_about_anon` — GET → 200 (аноним может читать)
- `test_update_about_anon` — PUT → 401 (аноним не может менять)
- `test_update_about_admin` — PUT с админом → 200
- `test_get_about_returns_content` — GET возвращает title и content
- `test_singleton_auto_create` — при первом GET создаётся запись по умолчанию

**Признак готовности:** `python manage.py test about` — все тесты проходят.

---

### 🟦 Задача 13: Gunicorn

**Кому:** DevOps
**Файлы:** `requirements.txt`

**Что конкретно нужно сделать:**

1. Открыть `requirements.txt`
2. Добавить строку: `gunicorn`
3. Установить: `pip install gunicorn`
4. Проверить: `gunicorn config.wsgi:application --bind 0.0.0.0:8000` — сервер стартует

---

### 🟦 Задача 14: Nginx конфиг

**Кому:** DevOps
**Файлы:** создать `deploy/nginx.conf`

**Что конкретно нужно сделать:**

Создать папку `deploy/`, внутри файл `nginx.conf`:
```nginx
upstream backend {
    server web:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    client_max_body_size 20M;

    location /static/ {
        alias /app/static/;
    }

    location /media/ {
        alias /app/media/;
    }

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Признак готовности:** `nginx -t -c deploy/nginx.conf` — конфиг валиден.

---

### 🟦 Задача 15: CI/CD (GitHub Actions)

**Кому:** DevOps
**Файлы:** создать `.github/workflows/ci.yml`

**Что конкретно нужно сделать:**

Создать `.github/workflows/ci.yml`:
```yaml
name: CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: london_db
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run migrations
      run: python manage.py migrate
      env:
        DB_ENGINE: django.db.backends.postgresql
        DB_NAME: london_db
        DB_USER: postgres
        DB_PASSWORD: postgres
        DB_HOST: localhost
        DB_PORT: 5432
        SECRET_KEY: test-secret-key
    
    - name: Run tests
      run: python manage.py test
      env:
        DB_ENGINE: django.db.backends.postgresql
        DB_NAME: london_db
        DB_USER: postgres
        DB_PASSWORD: postgres
        DB_HOST: localhost
        DB_PORT: 5432
        SECRET_KEY: test-secret-key
```

**Признак готовности:** после пуша в GitHub в разделе Actions запускается pipeline и проходит успешно.

---

### 🟪 Задача 16–22: Frontend (если есть команда)

**Кому:** Frontend-разработчики

**Точное ТЗ по страницам:**

**1. Авторизация (2 endpoints):**
- Страница регистрации: поля username, email, password, кнопка "Зарегистрироваться"
- Страница логина: поля username, password, кнопка "Войти"
- После логина сохранять access_token и refresh_token (localStorage или cookies)
- При 401 автоматически делать refresh
- Кнопка "Выйти" (очистить токены)

**2. Страница "Меню":**
- GET `/api/menu/categories/` — список категорий
- GET `/api/menu/dishes/` — список блюд (можно отфильтровать по `?category=ID`)
- Отобразить: название, цену, описание, картинку, доступность
- Для админов: кнопки "Добавить", "Редактировать", "Удалить"

**3. Страница "Новости":**
- GET `/api/news/` — список новостей
- GET `/api/news/{id}/` — детальная страница новости
- Отобразить: заголовок, дату, контент, картинку
- Для админов: CRUD

**4. Страница "О нас":**
- GET `/api/about/` — получить контент
- Отобразить: title, content
- Для админа: возможность редактировать (PUT)

**5. Страница "Контакты":**
- Форма: name, email, message + кнопка "Отправить"
- POST `/api/contact/`
- После отправки — уведомление об успехе
- Для админа: отдельная страница со списком сообщений (GET) и просмотром деталей

**6. Админ-панель (для staff-пользователей):**
- Управление категориями меню
- Управление блюдами (с загрузкой картинки)
- Управление новостями (с загрузкой картинки)
- Просмотр сообщений из контактов

**Признак готовности:** все страницы работают, авторизация проходит полный цикл (login → request → refresh → logout).

---

## 📅 Итого по срокам

| Неделя | Кто | Что делает |
|---|---|---|
| 1 | Backend #1 | CORS + .env |
| 1 | Backend #2 | CustomUser + Contact DetailView |
| 1 | DevOps | Docker |
| 2 | Backend #2 | Фильтры + валидация |
| 2 | Backend #3 | Тесты (все 5 apps) |
| 2 | DevOps | Gunicorn + Nginx |
| 3 | DevOps | CI/CD |
| 3 | Frontend | Все страницы |

---

> Вопросы — в чат команды. Каждую выполненную задачу отмечать готово в этом файле.

---
#https://www.figma.com/design/nxbT73EVpP2spkWwjLO2E3/%F0%9F%8D%94London?node-id=0-1&p=f&t=yaigVQ7AyK18DXRI-0
#figma link
---

## 🇺🇿 O'zbekcha bo'lim

---

## ✅ Nima qilingan

### Loyiha skleti
- Django loyihasi asosiy tuzilishi (`london_project/`)
- `config/settings.py` — DRF, JWT, drf-spectacular, paginatsiya, filtrlash sozlamalari
- `config/urls.py` — barcha yo'nalishlar ulangan
- `config/wsgi.py`, `config/asgi.py`

### `accounts` ilovasi — Foydalanuvchilar va JWT
- `CustomUser` modeli (AbstractUser dan meros olgan)
- `RegisterSerializer`, `UserSerializer`
- `RegisterView` (POST — ro'yxatdan o'tish)
- Yo'nalishlar: `/api/auth/register/`, `/api/auth/login/`, `/api/auth/refresh/`
- `IsAdminOrReadOnly` — maxsus ruxsat klassi
- Admin panel

### `menu` ilovasi — Kategoriyalar va taomlar
- `Category` modeli (name, description, order)
- `Dish` modeli (category FK, name, description, price, image, is_available, order)
- `CategoryViewSet`, `DishViewSet` — to'liq CRUD
- Yo'nalishlar: `/api/menu/categories/`, `/api/menu/dishes/`
- Ruxsat: `IsAdminOrReadOnly`
- Admin panel

### `news` ilovasi — Yangiliklar
- `NewsArticle` modeli (title, content, image, created_at, updated_at, is_published)
- `NewsArticleViewSet` — to'liq CRUD
- Yo'nalish: `/api/news/`
- Ruxsat: `IsAdminOrReadOnly`
- Admin panel

### `contact` ilovasi — Aloqa
- `ContactMessage` modeli (name, email, message, created_at, is_read)
- `ContactMessageListCreateView` (POST — hamma, GET — faqat admin)
- Yo'nalish: `/api/contact/`
- Admin panel

### `about` ilovasi — Biz haqimizda
- `AboutContent` modeli (title, content, updated_at) — singleton
- `AboutContentRetrieveUpdateView` (GET — hamma, PUT — admin)
- Yo'nalish: `/api/about/`
- Admin panel

### Infratuzilma
- `requirements.txt` barcha kutubxonalar bilan
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- OpenAPI Schema: `/api/schema/`
- `.gitignore`
- `README.md` (Rus va O'zbek tillarida)
- Migratsiyalar yaratilgan va bajarilgan, `python manage.py check` xatosiz

---

## ❗ Nima qilish kerak — batafsil

---

### 🟥 1-topshiriq: CORS sozlamalari

**Kimga:** Backend dasturchi #1
**Fayllar:** `requirements.txt`, `config/settings.py`

**Aniq nima qilish kerak:**

1. `requirements.txt` faylini oching, qo'shing: `django-cors-headers`
2. O'rnating: `pip install django-cors-headers`
3. `config/settings.py` da:
   - `INSTALLED_APPS` ga `'corsheaders'` ni eng birinchi qilib qo'shing (hatto `django.contrib.admin` dan oldin)
   - `MIDDLEWARE` ga `'corsheaders.middleware.CorsMiddleware'` ni eng birinchi qilib qo'shing (ro'yxatning eng tepasiga)
4. `settings.py` oxiriga qo'shing:
   ```python
   CORS_ALLOW_ALL_ORIGINS = True   # faqat development uchun
   ```
5. Tekshirish: serverni ishga tushiring, frontend boshqa portdan so'rov yubora olsin

**Tayyorlik belgisi:** frontend dasturchi API ga so'rov yuborganda brauzer konsolida CORS xatosi chiqmaydi.

---

### 🟥 2-topshiriq: .env fayllari

**Kimga:** Backend dasturchi #1
**Fayllar:** `.env`, `.env.example`

**Aniq nima qilish kerak:**

1. `london_project/.env.example` faylini yarating:
   ```env
   SECRET_KEY=change-me-to-random-string
   DEBUG=True
   ALLOWED_HOSTS=*

   DB_ENGINE=django.db.backends.sqlite3
   DB_NAME=db.sqlite3

   # PostgreSQL uchun (Docker bilan ishlatilsa):
   # DB_ENGINE=django.db.backends.postgresql
   # DB_NAME=london_db
   # DB_USER=postgres
   # DB_PASSWORD=postgres
   # DB_HOST=db
   # DB_PORT=5432
   ```
2. `.env` faylini yarating (`.env.example` dan nusxa oling)
3. `.gitignore` da `.env` borligini tekshiring (bor)
4. SECRET_KEY generatsiya qiling:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Natijani `.env` ga yozing

**Tayyorlik belgisi:** loyiha SECRET_KEY ni kod ichida ko'rsatmasdan ishlaydi.

---

### 🟥 3-topshiriq: Docker

**Kimga:** DevOps
**Fayllar:** `Dockerfile`, `docker-compose.yml`, `.dockerignore`

**Aniq nima qilish kerak:**

**Dockerfile:**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**docker-compose.yml:**
```yaml
version: '3.9'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - .env
    volumes:
      - .:/app
      - static_volume:/app/static
      - media_volume:/app/media
    command: >
      sh -c "python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"

  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data
    env_file:
      - .env
    environment:
      - POSTGRES_DB=london_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    ports:
      - "5432:5432"

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

**.dockerignore:**
```
__pycache__
*.pyc
*.pyo
.env
.git
.gitignore
venv
.venv
*.sqlite3
```

**Tayyorlik belgisi:** `docker compose up --build` loyihani ishga tushiradi, API `http://localhost:8000` da javob beradi.

---

### 🟧 4-topshiriq: CustomUser ni kengaytirish

**Kimga:** Backend dasturchi #2
**Fayllar:** `accounts/models.py`, `accounts/serializers.py`

**Aniq nima qilish kerak:**

1. `accounts/models.py` ni oching. Hozirgi holat:
   ```python
   class CustomUser(AbstractUser):
       pass
   ```

2. Yangi maydonlarni qo'shing:
   ```python
   class CustomUser(AbstractUser):
       phone = models.CharField(max_length=20, blank=True, verbose_name='Telefon')
       avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')

       class Meta:
           verbose_name = 'Foydalanuvchi'
           verbose_name_plural = 'Foydalanuvchilar'
   ```

3. `accounts/serializers.py` ni yangilang:
   - `RegisterSerializer.Meta.fields` ga `'phone'`, `'avatar'` qo'shing
   - `UserSerializer.Meta.fields` ga `'phone'`, `'avatar'` qo'shing

4. Migratsiya qiling:
   ```bash
   python manage.py makemigrations accounts
   python manage.py migrate
   ```

**Tayyorlik belgisi:** ro'yxatdan o'tishda `phone` va `avatar` yuborish mumkin, ular DB da saqlanadi.

---

### 🟧 5-topshiriq: Contact uchun DetailView

**Kimga:** Backend dasturchi #2
**Fayllar:** `contact/views.py`, `contact/urls.py`

**Aniq nima qilish kerak:**

1. `contact/views.py` ga yangi klass qo'shing:
   ```python
   class ContactMessageRetrieveView(generics.RetrieveAPIView):
       queryset = ContactMessage.objects.all()
       serializer_class = ContactMessageSerializer
       permission_classes = (permissions.IsAdminUser,)
   ```

2. `contact/urls.py` ga yo'nalish qo'shing:
   ```python
   path('<int:pk>/', ContactMessageRetrieveView.as_view(), name='contact-detail'),
   ```

**Tayyorlik belgisi:**
- `GET /api/contact/1/` admin uchun bitta xabarni ko'rsatadi
- Anonimga 401/403 qaytadi
- Mavjud bo'lmagan ID ga 404 qaytadi

---

### 🟧 6-topshiriq: Filtrlash

**Kimga:** Backend dasturchi #2
**Fayllar:** `menu/views.py`, `news/views.py`, `contact/views.py`

**Aniq nima qilish kerak:**

**menu/views.py** da `DishViewSet` ga qo'shing:
```python
filterset_fields = ('category', 'is_available')
search_fields = ('name', 'description')
ordering_fields = ('name', 'price', 'order')
```

**news/views.py** da `NewsArticleViewSet` ga qo'shing:
```python
filterset_fields = ('is_published',)
search_fields = ('title', 'content')
ordering_fields = ('created_at', 'title')
```

**contact/views.py** da `ContactMessageListCreateView` ga qo'shing:
```python
filterset_fields = ('is_read',)
search_fields = ('name', 'email', 'message')
ordering_fields = ('created_at',)
```

**Tayyorlik belgisi:** Swagger UI da filtr, qidirish va tartiblash maydonlari paydo bo'ladi.

---

### 🟧 7-topshiriq: Taom nomi unikalligi validatsiyasi

**Kimga:** Backend dasturchi #2
**Fayllar:** `menu/models.py` yoki `menu/serializers.py`

**Model orqali (tavsiya qilinadi):**

`menu/models.py` da `Dish.Meta` ga qo'shing:
```python
class Meta:
    verbose_name_plural = 'dishes'
    ordering = ('order', 'name')
    constraints = [
        models.UniqueConstraint(
            fields=['category', 'name'],
            name='unique_dish_in_category'
        )
    ]
```

Migratsiya: `python manage.py makemigrations menu && python manage.py migrate`

**Tayyorlik belgisi:** bitta kategoriyada ikkita bir xil nomli taom yaratish mumkin emas (400 xato).

---

### 🟩 8-topshiriq: accounts testlari

**Kimga:** Backend dasturchi #3
**Fayllar:** `accounts/tests.py`

**Testlar ro'yxati:**

- `test_register_success` — to'g'ri registratsiya → 201
- `test_register_no_password` — parolsiz registratsiya → 400
- `test_register_duplicate_username` — ikki marta bir username → 400
- `test_login_success` — to'g'ri login → 200 + token
- `test_login_wrong_password` — noto'g'ri parol → 401
- `test_refresh_success` — to'g'ri refresh token → 200
- `test_refresh_invalid` — yolg'on refresh token → 401

**Tayyorlik belgisi:** `python manage.py test accounts` — barcha testlar o'tadi.

---

### 🟩 9-topshiriq: menu testlari

**Kimga:** Backend dasturchi #3
**Fayllar:** `menu/tests.py`

**Testlar ro'yxati:**

- Kategoriya modeli: `test_str`, `test_ordering`
- Kategoriya API: list (200), create anon (401), create admin (201), create user (403), detail (200), update admin (200), delete admin (204)
- Taom API: list (200), create admin (201), filter by category, search by name

**Tayyorlik belgisi:** `python manage.py test menu` — barcha testlar o'tadi.

---

### 🟩 10-topshiriq: news testlari

**Kimga:** Backend dasturchi #3
**Fayllar:** `news/tests.py`

**Testlar ro'yxati:**

- Model: `test_str`, `test_ordering`
- API: list (200), create anon (401), create admin (201), detail (200), update admin (200), delete admin (204), filter published, search title

**Tayyorlik belgisi:** `python manage.py test news` — barcha testlar o'tadi.

---

### 🟩 11-topshiriq: contact testlari

**Kimga:** Backend dasturchi #3
**Fayllar:** `contact/tests.py`

**Testlar ro'yxati:**

- Model: `test_str`
- API: send message anon (201), send without email (400), list anon (401), list admin (200), list user (403), filter by is_read

**Tayyorlik belgisi:** `python manage.py test contact` — barcha testlar o'tadi.

---

### 🟩 12-topshiriq: about testlari

**Kimga:** Backend dasturchi #3
**Fayllar:** `about/tests.py`

**Testlar ro'yxati:**

- GET anon (200), PUT anon (401), PUT admin (200), GET returns content, singleton auto create

**Tayyorlik belgisi:** `python manage.py test about` — barcha testlar o'tadi.

---

### 🟦 13-topshiriq: Gunicorn

**Kimga:** DevOps
**Fayllar:** `requirements.txt`

`requirements.txt` ga `gunicorn` qo'shing va o'rnating.

**Tayyorlik belgisi:** `gunicorn config.wsgi:application --bind 0.0.0.0:8000` ishlaydi.

---

### 🟦 14-topshiriq: Nginx konfigi

**Kimga:** DevOps
**Fayllar:** `deploy/nginx.conf`

`deploy/` papkasini va `nginx.conf` ni yarating (yuqoridagi ruscha bo'limdagi nginx konfigini ishlating).

**Tayyorlik belgisi:** `nginx -t -c deploy/nginx.conf` xatosiz.

---

### 🟦 15-topshiriq: CI/CD (GitHub Actions)

**Kimga:** DevOps
**Fayllar:** `.github/workflows/ci.yml`

`.github/workflows/ci.yml` ni yarating (yuqoridagi ruscha bo'limdagi YAML ni ishlating).

**Tayyorlik belgisi:** GitHub ga push qilinganda Actions da pipeline ishlaydi va testlar o'tadi.

---

### 🟪 16–22-topshiriqlar: Frontend (agar frontend jamoasi bo'lsa)

**Kimga:** Frontend dasturchilar

**Sahifalar:**

1. **Avtorizatsiya:** Register, Login, token saqlash, refresh, logout
2. **Menyu:** Kategoriyalar va taomlar ro'yxati, admin uchun CRUD
3. **Yangiliklar:** Yangiliklar ro'yxati va detali, admin uchun CRUD
4. **Biz haqimizda:** Matnni ko'rsatish, admin uchun tahrirlash
5. **Kontaktlar:** Forma (name, email, message), admin uchun xabarlar ro'yxati
6. **Admin panel:** Barcha ma'lumotlarni boshqarish

---

## 📅 Bajarish tartibi

| Hafta | Kim | Nima qiladi |
|---|---|---|
| 1 | Backend #1 | CORS + .env |
| 1 | Backend #2 | CustomUser + Contact Detail |
| 1 | DevOps | Docker |
| 2 | Backend #2 | Filtrlar + validatsiya |
| 2 | Backend #3 | Testlar (barcha 5 ilova) |
| 2 | DevOps | Gunicorn + Nginx |
| 3 | DevOps | CI/CD |
| 3 | Frontend | Barcha sahifalar |

---

> Savollar bo'lsa — jamoa chatiga yozing. Har bir bajarilgan vazifani shu faylda belgilab qo'ying. Omad! 🚀

#https://www.figma.com/design/nxbT73EVpP2spkWwjLO2E3/%F0%9F%8D%94London?node-id=0-1&p=f&t=yaigVQ7AyK18DXRI-0
#figma link