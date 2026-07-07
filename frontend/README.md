# London Grill — фронтенд (по мотивам Figma "🍔London")

Чистый HTML/CSS/JS (без сборки, без фреймворков), готовый работать поверх твоего Django REST API
(`london_project`). Дизайн повторяет структуру макета: Home, Menu, News, About Us, Contact Us,
Log In / Sign Up. Названия и логотип заменены на нейтральный плейсхолдер "London Grill" —
поменяй под свой бренд в файлах `*.html` (строки с `.brand` и `.footer-brand`).

## Структура

```
eaturkish/
├── index.html      # Главная: hero, Popular Dishes, Menu preview, отзывы, новости, Instagram, подписка
├── menu.html        # Категории + список блюд (из API)
├── news.html        # Список новостей + "View More"
├── about.html        # Текст "О нас" из API
├── contact.html      # Контакты, форма обратной связи, карта
├── login.html / register.html   # JWT-логин и регистрация
├── css/style.css     # Вся дизайн-система (цвета, типографика, компоненты)
└── js/
    ├── api.js         # Конфиг API_BASE_URL + все fetch-запросы + JWT refresh
    ├── main.js        # Общие штуки: бургер-меню, подписка, форматирование
    ├── home.js / menu.js / news.js / about.js / contact.js / auth.js
```

## Как запустить

1. Открой `js/api.js` и поставь адрес своего бэкенда:
   ```js
   const API_BASE_URL = "http://127.0.0.1:8000/api";
   ```
2. Раздай папку любым статик-сервером, например:
   ```bash
   npx serve eaturkish
   # или
   python -m http.server 5500 --directory eaturkish
   ```
3. На бэкенде включи CORS для адреса, с которого открываешь фронт (`django-cors-headers`):
   ```python
   INSTALLED_APPS += ["corsheaders"]
   MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")
   CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:5500"]
   ```

## Как фронт мапится на твои эндпоинты

| Страница | Запросы |
|---|---|
| `index.html` | `GET /api/menu/categories/`, `GET /api/menu/dishes/`, `GET /api/news/` |
| `menu.html` | `GET /api/menu/categories/`, `GET /api/menu/dishes/?category={id}` |
| `news.html` | `GET /api/news/` (пагинация "View More" — на клиенте) |
| `about.html` | `GET /api/about/` |
| `contact.html` | `POST /api/contact/` |
| `login.html` | `POST /api/auth/login/` → сохраняет `access`/`refresh` в localStorage |
| `register.html` | `POST /api/auth/register/` |

Токен `access` автоматически обновляется через `POST /api/auth/refresh/`, если запрос идёт
с `auth: true` и сервер вернул 401 — см. `apiRequest()` в `js/api.js`.

## Поля, которые ожидает фронт

Код написан гибко (через `pick()` в `api.js`) и сам подбирает первое существующее поле, поэтому
не страшно, если названия немного отличаются:

- **Категория**: `id`, `name`/`title`
- **Блюдо**: `id`, `name`/`title`, `price`, `image`/`photo` (можно относительный путь `/media/...`
  — фронт сам достроит домен из `API_BASE_URL`), `category`
- **Новость**: `id`, `title`/`name`, `content`/`body`/`summary`/`excerpt`, `image`/`photo`,
  `created_at`/`date`/`published_at`
- **О нас**: `title`, `content`/`text`/`description`/`body`, `image`

Если картинки не пришли с бэкенда, показывается плейсхолдер с picsum.photos — просто чтобы макет
не выглядел пустым, замени на реальные фото блюд/интерьера.

## Разделы без бэкенд-эндпоинта

В макете есть "Happy Customers" (отзывы) и Instagram-галерея — под них API не описан в ТЗ,
поэтому они оставлены статичными (заглушки). Если появятся эндпоинты — подключаются так же,
как остальные (`fetch` + рендер списком).

## Что стоит донастроить

- Реальный логотип/название бренда вместо "London Grill"
- Карта в `contact.html` сейчас на OpenStreetMap (координаты примерные) — поставь реальный адрес
- Иконки соцсетей в футере — сейчас буквы-заглушки, замени на SVG-иконки при желании
