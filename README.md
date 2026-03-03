# TikTok Video Publisher Bot

🤖 Автоматическая загрузка видео в TikTok через Official Content Publishing API v2

## Features

- ✅ **Official TikTok API** - используется Content Publishing API v2
- ✅ **OAuth 2.0** - безопасная авторизация
- ✅ **Draft Upload** - загрузка видео как черновиков (можно вручную публиковать)
- ✅ **Mass Upload** - загрузка всех видео из директории одним скриптом
- ✅ **Automated Token Refresh** - обновление access_token через refresh_token

## Requirements

- Python 3.8+
- [TikTok Developer Account](https://developers.tiktok.com)
- Приложение с Content Posting API включено
- Approved scopes: `video.upload` (для черновиков) или `video.publish` (для прямой публикации)

## Installation

1. **Clone repository**
```bash
git clone https://github.com/YOUR_USERNAME/tiktok-publisher.git
cd tiktok-publisher
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Copy config template**
```bash
cp config/api_credentials.json.example config/api_credentials.json
```

## Setup

### 1. Создай TikTok приложение

1. Перейди на [TikTok Developer Portal](https://developers.tiktok.com)
2. Создай приложение
3. Включи **Content Posting API** продукт
4. Запиши `CLIENT_ID` и `CLIENT_SECRET`

### 2. Получи OAuth Authorization Code

Открой эту ссылку в браузере:

```
https://www.tiktok.com/v2/auth/authorize/?client_key=YOUR_CLIENT_ID&redirect_uri=https://oauth.pstmn.io/v1/callback&response_type=code&scope=video.upload&state=123
```

**Scopes:**
- `video.upload` - для черновиков (работает с PUBLIC аккаунтом)
- `video.publish` - для прямой публикации (требует PRIVATE аккаунт если приложение не аудировано)

### 3. Обменяй код на токен

**Быстрый метод:**
```bash
python3 exchange_draft_token.py
```

Скрипт попросит ввести `authorization_code` из callback URL (параметр `code`).

### 4. Настрой config

Файл: `config/api_credentials.json`

```json
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "access_token": "act...",
  "refresh_token": "rft...",
  "open_id": "-000A..."
}
```

## Usage

### Загрузить одно видео как черновик

```bash
python3 upload_as_exact.py
```

**Файл для загрузки:** `../youtube-shorts/downloads/TikTok video #7588920065173556502.mp4`

Или укажи свой файл в скрипте (переменная `VIDEO_PATH`)

### Загрузить все видео из директории

```bash
python3 upload_all_as_drafts.py
```

**Загружает:** все `.mp4` файлы из `../youtube-shorts/downloads/`

### Результаты

После загрузки:
1. Открой TikTok приложение на телефоне
2. Перейди в **Inbox / Drafts**
3. Видео будут там, готовые к публикации

### Publish ID

Каждое загруженное видео получает `publish_id`, например:
`v_inbox_file~v2.7612993423670380561`

Храни этот ID для отслеживания статуса.

## API Endpoints

### TikTok Content Publishing API v2

| Endpoint | Method | Описание |
|----------|--------|----------|
| `/v2/post/publish/inbox/video/init/` | POST | Инициализировать загрузку черновика |
| `/v2/post/publish/video/init/` | POST | Инициализировать прямую публикацию |
| `/v2/post/publish/status/fetch/` | POST | Проверить статус публикации |

### CDN Upload

Метод: `PUT {upload_url}`

Headers:
```
Content-Type: video/mp4
Content-Range: bytes 0-{size-1}/{total_size}
```

## File Structure

```
tiktok-publisher/
├── src/                          # Core bot modules
│   ├── tiktok_bot.py            # Main TikTokBot class
│   ├── tiktok_api.py            # TikTok API client
│   ├── video_processor.py       # Video processing
│   └── video_downloader.py      # YouTube downloader
├── config/                      # Configuration files
│   ├── api_credentials.json     # OAuth credentials (not in git!)
│   └── api_credentials.json.example  # Template
├── upload_as_exact.py           # Upload single video
├── upload_all_as_drafts.py      # Upload all videos
├── exchange_draft_token.py      # Exchange auth code for token
└── requirements.txt             # Python dependencies
```

## Limitations

### Unaудированные приложения

Если приложение ещё не прошло аудит:
- ✅ Можно публиковать в **PRIVATE** аккаунты (direct publish)
- ✅ Можно загружать черновики в **PUBLIC** аккаунты
- ❌ Прямая публикация в PUBLIC аккаунт недоступна

### Video Requirements

- Формат: `.mp4`, `.mov`
- Максимальный размер: 500 MB
- Max длительность: 60 минут
- Рекомендуемое соотношение сторон: 9:16 (вертикальное видео)

## Troubleshooting

### Error: 416 Range Not Satisfiable

**Проблема:** Неправильный Content-Range header

**Решение:** Используй точный формат:
```
Content-Range: bytes 0-{size-1}/{total_size}
```

### Error: unaudited_client_can_only_post_to_private_accounts

**Проблема:** Пытаешься опубликовать напрямую в public аккаунт

**Решение:** Используй `video.upload` scope для черновиков ИЛИ сделай аккаунт приватным

### Access Token Expired

**Проблема:** Token живёт только 24 часа

**Решение:** Используй refresh_token для получения нового access_token

## Security

- ❌ **НЕ** коммить `config/api_credentials.json` в git
- ❌ **НЕ** делиться access_token или refresh_token
- ✅ Используй `.env` файлы для sensitive данных
- ✅ Храни credentials в безопасном месте

## Deployment

### Использование через cron

```bash
# Запуск каждые 6 часов
0 */6 * * * cd /path/to/tiktok-publisher && /usr/bin/python3 upload_all_as_drafts.py >> bot.log 2>&1
```

### Docker (опционально)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "upload_all_as_drafts.py"]
```

## API Reference

- [TikTok Content Posting API](https://developers.tiktok.com/doc/content-posting-api-get-started)
- [TikTok Scopes](https://developers.tiktok.com/doc/scopes-overview)
- [TikTok Application Audit](https://developers.tiktok.com/application/content-posting-api)

## License

MIT

## Contributing

PRs приветствуются!

---

**Developed for automated TikTok video publishing** 🚀
