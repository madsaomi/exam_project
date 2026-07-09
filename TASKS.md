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

### Чистка и доработка кода
- Убран неиспользуемый импорт `mixins` в `about/views.py`
- `from datetime import timedelta` перенесён наверх (PEP8)
- `BASE_DIR` теперь импортируется из `settings` (без дублирования)
- `accounts/views.py` — прямой импорт `CustomUser`
- Длинные строки в `menu/tests.py` разбиты
- Убрана утечка API-эндпоинтов в сообщениях пользователям
- Исправлен `main.js` (потенциальный TypeError)
- Добавлен `data-login-btn` в `register.html`
- Бренд приведён к единому виду: `LONDON GRILL HOUSE`
- Исправлен адрес в футере
- Удалена пустая директория `frontend/assets/`

### i18n — Мультиязычность (EN / RU / UZ)
- Создан `js/i18n.js` со словарём на 40+ ключей × 3 языка
- Переключатель языка в шапке всех 7 страниц
- Язык сохраняется в `localStorage`
- Все надписи, кнопки, заголовки, футер — переключаются
- JS-сообщения (пустые списки, ошибки, успех) — через `__()`

### News Modal
- По клику "Read More" открывается модальное окно
- Показывает полный текст, заголовок, дату, картинку
- Закрывается по ✕, на фон, по Escape

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
| 11 | **Тесты contact** | ✅ 7 тестов (починены) |
| 12 | **Тесты about** | ✅ 5 тестов |
| 13 | **Gunicorn** | ✅ в `requirements.txt` |
| 14 | **Nginx конфиг** | ✅ `deploy/nginx.conf` |
| 15 | **CI/CD** | ✅ `.github/workflows/ci.yml` |
| 16 | **Frontend** | ✅ HTML/CSS/JS, подключён к API |
| 17 | **Демо-данные** | ✅ 8 категорий, 34 блюда, 5 новостей |
| 18 | **Серверы запущены** | ✅ Backend :8000, Frontend :5500 |
| 19 | **Чистка кода** | ✅ Импорты, PEP8, BASE_DIR, brand, адрес |
| 20 | **i18n (EN/RU/UZ)** | ✅ Все 7 страниц, 40+ ключей, `localStorage` |
| 21 | **News Modal (Read More)** | ✅ Модальное окно с полным текстом |
| 22 | **CI requirements.txt** | ✅ Добавлены все зависимости |

**Всего тестов: 42/42 — проходят ✅**

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
https://www.figma.com/design/nxbT73EVpP2spkWwjLO2E3/%F0%9F%8D%94London?node-id=0-1&p=f&t=yaigVQ7AyK18DXRI-0
<!-- figma link -->
---

## 🇺🇿 O'zbekcha bo'lim

---

## ✅ Bajarilgan vazifalar holati

| # | Vazifa | Holati | Kim bajargan | Izoh |
|---|---|---|---|---|
| 1 | **CORS** | ✅ Tayyor | Backend #1 | `django-cors-headers` qo'shilgan |
| 2 | **.env fayllari** | ✅ Tayyor | Backend #1 | `.env.example` va `.env` yaratilgan |
| 3 | **Docker** | ✅ Tayyor | DevOps | `Dockerfile`, `docker-compose.yml`, `.dockerignore` yaratilgan |
| 4 | **CustomUser kengaytirish** | ✅ Tayyor | Backend #2 | `phone`, `avatar` maydonlari qo'shilgan |
| 5 | **Contact DetailView** | ✅ Tayyor | Backend #2 | `ContactMessageRetrieveView` qo'shilgan |
| 6 | **Filtrlash** | ✅ Tayyor | Backend #2 | DishViewSet + NewsArticleViewSet ga filtr qo'shilgan |
| 7 | **Taom unikalligi** | ✅ Tayyor | Backend #2 | `UniqueConstraint` qo'shilgan |
| 8 | **accounts testlari** | ✅ Tayyor | Backend #3 | 7 ta test, hammasi o'tadi |
| 9 | **menu testlari** | ✅ Tayyor | Backend #3 | 10 ta test, hammasi o'tadi |
| 10 | **news testlari** | ✅ Tayyor | Backend #3 | 10 ta test, hammasi o'tadi |
| 11 | **contact testlari** | ⚠️ Tuzatildi | — | Xatolar bor edi, men tuzatdim |
| 12 | **about testlari** | ✅ Tayyor | Backend #3 | 5 ta test qo'shilgan |
| 13 | **Gunicorn** | ✅ Tayyor | DevOps | `requirements.txt` da bor |
| 14 | **Nginx konfigi / Deploy** | ✅ Tayyor | DevOps | Railway uchun Whitenoise va dj-database-url qo'shildi |
| 15 | **CI/CD** | ✅ Tayyor | DevOps | `.github/workflows/ci.yml` tayyorlangan |
| 16–22 | **Frontend** | ✅ Tayyor | — | Barcha sahifalar ishlaydi |
| 23 | **Code cleanup** | ✅ Tayyor | — | Imports, PEP8, brand, address |
| 24 | **i18n (EN/RU/UZ)** | ✅ Tayyor | — | 7 sahifa, 40+ kalit, localStorage |
| 25 | **News Modal** | ✅ Tayyor | — | Read More to'liq matn oynasi |

**Jami testlar: 42/42 — hammasi o'tadi ✅**

---

## ❗ Barcha vazifalar bajarildi ✅

Loyiha to'liq tayyor. 42 test, 3 tilda frontend, Docker, CI/CD, GitHub.

---

> Savollar bo'lsa — jamoa chatiga yozing. Omad! 🚀

#https://www.figma.com/design/nxbT73EVpP2spkWwjLO2E3/%F0%9F%8D%94London?node-id=0-1&p=f&t=yaigVQ7AyK18DXRI-0
#figma link
