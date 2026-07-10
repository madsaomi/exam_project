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
- `RegisterForm` — Django Form для регистрации через сайт
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
- `ContactForm` — Django Form для отправки через сайт
- endpoint: `/api/contact/`
- Админка

### App `about` — О нас
- Модель `AboutContent` (title, content, updated_at) — singleton
- `AboutContentRetrieveUpdateView` (GET — все, PUT — админ)
- endpoint: `/api/about/`
- Админка

### Инфраструктура
- `requirements.txt` со всеми зависимостями (+ Pillow)
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- OpenAPI Schema: `/api/schema/`
- `.gitignore`
- `README.md` (русский + узбекский)
- Миграции созданы и накатаны, `python manage.py check` проходит без ошибок

### Django Templates — Серверный рендеринг
- `templates/base.html` — базовый шаблон (header, nav, footer, i18n)
- `templates/pages/home.html` — главная: hero, популярные блюда, меню, новости, testimonials
- `templates/pages/menu.html` — меню: sidebar с категориями + сетка блюд
- `templates/pages/news.html` — список новостей
- `templates/pages/news_detail.html` — детальная страница новости
- `templates/pages/about.html` — "О нас"
- `templates/pages/contact.html` — форма обратной связи (CSRF)
- `templates/pages/login.html` — вход (Django session auth)
- `templates/pages/register.html` — регистрация
- `config/page_views.py` — все template view функции
- `static/css/style.css`, `static/js/i18n.js` — статика

### Страницы ошибок
- `templates/404.html` — "Страница не найдена" (красивая страница с.brand)
- `templates/403.html` — "Доступ запрещён"
- `templates/500.html` — "Ошибка сервера" (standalone HTML, без template tags — безопасен)
- `handler404`, `handler500`, `handler403` в `config/urls.py`
- Пользователь НИКОГДА не видит traceback

### i18n — Мультиязычность (EN / RU / UZ)
- `static/js/i18n.js` — словарь на 90+ ключей × 3 языка
- Переключатель языка EN/RU/UZ в шапке всех страниц
- Язык сохраняется в `localStorage`
- **Полный покрытие**: hero, testimonials, contact, newsletter, breadcrumbs, empty states, ошибки
- `data-i18n` на всех видимых текстах
- `data-i18n-placeholder` на всех input полях

### Тесты
- `accounts/tests.py` — 7 тестов (API)
- `menu/tests.py` — 10 тестов (API)
- `news/tests.py` — 10 тестов (API)
- `contact/tests.py` — 7 тестов (API)
- `about/tests.py` — 5 тестов (API)
- `config/tests.py` — 17 тестов (Django template views)
- **Всего: 59/59 — проходят ✅**

### Чистка и доработка кода
- Убраны все JS-файлы фронтенда (api.js, main.js, home.js, menu.js, news.js, about.js, contact.js, auth.js)
- Удалены HTML-страницы старого фронтенда
- CSS и i18n.js перенесены в `static/`
- CSRF_TRUSTED_ORIGINS исправлен для Django 4.0+
- Logout кнопка использует POST (Django 5+)
- STATIC_ROOT/STATICFILES_DIRS разделены для collectstatic

---

## ✅ Финальный статус — всё готово

| # | Задача | Статус |
|---|---|---|
| 1 | **CORS** | ✅ |
| 2 | **.env файлы** | ✅ `.env` + `.env.example` |
| 3 | **Docker** | ✅ `Dockerfile`, `docker-compose.yml`, `.dockerignore` |
| 4 | **Расширить CustomUser** | ✅ `phone`, `avatar` |
| 5 | **DetailView Contact** | ✅ |
| 6 | **Фильтры** | ✅ |
| 7 | **Валидация уникальности блюда** | ✅ |
| 8 | **Тесты accounts** | ✅ 7 тестов |
| 9 | **Тесты menu** | ✅ 10 тестов |
| 10 | **Тесты news** | ✅ 10 тестов |
| 11 | **Тесты contact** | ✅ 7 тестов |
| 12 | **Тесты about** | ✅ 5 тестов |
| 13 | **Gunicorn** | ✅ в `requirements.txt` |
| 14 | **Nginx конфиг** | ✅ `deploy/nginx.conf` |
| 15 | **CI/CD** | ✅ `.github/workflows/ci.yml` |
| 16 | **Django Templates** | ✅ 9 шаблонов, server-side rendering |
| 17 | **Демо-данные** | ✅ 8 категорий, 34 блюда, 5 новостей |
| 18 | **Страницы ошибок** | ✅ 404, 403, 500 без traceback |
| 19 | **Чистка кода** | ✅ Удалён JS-фронтенд |
| 20 | **i18n (EN/RU/UZ)** | ✅ 90+ ключей, полный покрытие |
| 21 | **Template тесты** | ✅ 17 тестов для views |
| 22 | **Pillow** | ✅ для ImageField |
| 23 | **Session Auth** | ✅ Django login/logout/register |
| 24 | **Logout POST** | ✅ Django 5 совместимость |
| 25 | **CSRF** | ✅ во всех формах |

**Всего тестов: 59/59 — проходят ✅**

**URL-ы сайта:**

| URL | Страница |
|-----|----------|
| `/pages/` | Главная |
| `/pages/menu/` | Меню |
| `/pages/menu/<id>/` | Меню по категории |
| `/pages/news/` | Новости |
| `/pages/news/<id>/` | Детали новости |
| `/pages/about/` | О нас |
| `/pages/contact/` | Контакты |
| `/login/` | Вход |
| `/register/` | Регистрация |
| `/logout/` | Выход |

**Признак готовности:** все страницы работают, авторизация проходит полный цикл (register → login → logout), 59 тестов проходят, i18n работает на 3 языках, ошибки не показывают traceback.

---

## ❗ Нужно сделать / Что осталось

| # | Задача | Приоритет | Статус |
|---|--------|-----------|--------|
| 1 | **Деплой на Railway** | Высокий | ✅ Dockerfile, Procfile, railway.json, security settings |
| 2 | **Админ-панель для staff** | Средний | ✅ `staff/` app — dashboard, CRUD категорий/блюд/новостей, просмотр сообщений, редактирование about |
| 3 | **Картинки блюд** | Средний | ✅ Шаблоны используют picsum placeholder при отсутствии изображения. Нужно загрузить реальные фото через админку |
| 4 | **Тёмная тема** | Низкий | ✅ Переключатель в шапке, сохраняется в localStorage |
| 5 | **Пагинация на страницах** | Низкий | ✅ Меню (12/стр), новости (6/стр) |
| 6 | **Поиск по меню** | Низкий | ✅ Поиск по названию на странице меню |
| 7 | **Email подтверждение** | Низкий | ❌ Не требуется |
| 8 | **Соцсети в footer** | Низкий | ✅ Facebook, Twitter, Instagram ссылки |

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
| 3 | Frontend | Django Templates (замена JS) |
| 3 | Frontend | i18n полный покрытие |
| 3 | Frontend | Страницы ошибок (404/403/500) |
| 3 | Frontend | Template тесты (17 штук) |

---

> Вопросы — в чат команды. Каждую выполненную задачу отмечать готово в этом файле.

---

https://www.figma.com/design/nxbT73EVpP2spkWwjLO2E3/%F0%9F%8D%94London?node-id=0-1&p=f&t=yaigVQ7AyK18DXRI-0
<!-- figma link -->
---

## 🇺🇿 O'zbekcha bo'lim

---

## ✅ Bajarilgan vazifalar holati

| # | Vazifa | Holati | Izoh |
|---|---|---|---|
| 1 | **CORS** | ✅ | `django-cors-headers` |
| 2 | **.env fayllari** | ✅ | `.env.example` + `.env` |
| 3 | **Docker** | ✅ | `Dockerfile`, `docker-compose.yml` |
| 4 | **CustomUser** | ✅ | `phone`, `avatar` |
| 5 | **Contact DetailView** | ✅ | `ContactMessageRetrieveView` |
| 6 | **Filtrlash** | ✅ | DishViewSet + NewsArticleViewSet |
| 7 | **Taom unikalligi** | ✅ | `UniqueConstraint` |
| 8 | **Testlar (API)** | ✅ | 42 ta test |
| 9 | **Testlar (Templates)** | ✅ | 17 ta test |
| 10 | **Django Templates** | ✅ | 9 ta shablon, server-side rendering |
| 11 | **Xato sahifalari** | ✅ | 404, 403, 500 — traceback ko'rsatilmaydi |
| 12 | **i18n (EN/RU/UZ)** | ✅ | 90+ kalit, to'liq qamrov |
| 13 | **Session Auth** | ✅ | Django login/logout/register |
| 14 | **CI/CD** | ✅ | `.github/workflows/ci.yml` |
| 15 | **Pillow** | ✅ | ImageField uchun |

**Jami testlar: 59/59 — hammasi o'tadi ✅**

---

## ❗ Qoldiq vazifalar

| # | Vazifa | Muhimlik | Tavsif |
|---|--------|----------|--------|
| 1 | **Railway deploy** | Yuqori | Dockerfile ni yangilash, staticfiles tekshirish |
| 2 | **Admin panel saytda** | O'rta | CRUD boshqaruv sahifalari staff uchun |
| 3 | **Rasmlar** | O'rta | Haqiqiy rasmlar yuklash (hozir placeholder) |
| 4 | **Qorong'u tema** | Past | Tema almashtirgich qo'shish |
| 5 | **Sahifalash** | Past | Yangiliklar/taomlarga pagination |

---

> Savollar bo'lsa — jamoa chatiga yozing. Omad! 🚀
