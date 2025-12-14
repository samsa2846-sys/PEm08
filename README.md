# MotionCraft AI Competition Analyzer

AI-инструмент для анализа конкурентов в области 3D-анимации и моушн-дизайна.

## Возможности

- **Анализ текста**: Анализ описаний конкурентов и УТП с использованием DeepSeek AI
- **Анализ изображений**: Визуальный анализ контента с использованием Yandex Vision OCR
- **Система оценок**: Оценка конкурентов по дизайну, анимации, инновациям, исполнению и фокусу на клиентах
- **Desktop приложение**: PyQt6 GUI с CompetitionMonitor.exe
- **Web интерфейс**: Современный адаптивный веб-интерфейс для доступа через браузер

## Технологический стек

- **Backend**: FastAPI (Python 3.6+)
- **AI сервисы**: 
  - DeepSeek API для анализа текста
  - Yandex Vision для распознавания изображений
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Деплой**: Совместимо с Python 3.6 для shared hosting

## Структура проекта

```
pem08/
├── backend/
│   ├── config.py              # Конфигурация и настройки
│   ├── main.py                # FastAPI приложение
│   ├── models/
│   │   └── schemas.py         # Pydantic модели
│   └── services/
│       └── analyzer_service.py # Логика AI анализа
├── frontend/
│   ├── index.html             # Веб-интерфейс
│   ├── app.js                 # JavaScript логика
│   └── styles.css             # Стили
├── desktop_app.py             # PyQt6 desktop приложение
├── build.py                   # Скрипт сборки PyInstaller
├── requirements.txt           # Python зависимости
├── requirements-python36.txt  # Зависимости для Python 3.6
├── .env.example              # Шаблон переменных окружения
├── .gitignore                # Правила игнорирования Git
├── proxy.php                 # PHP proxy для shared hosting
└── .htaccess                 # Конфигурация Apache

```

## Установка

### Локальная разработка

1. **Клонировать репозиторий**:
```bash
git clone https://github.com/samsa2846-sys/PEm08.git
cd PEm08
```

2. **Создать виртуальное окружение**:
```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

3. **Установить зависимости**:
```bash
pip install -r requirements.txt
```

4. **Настроить окружение**:
Создайте файл `.env`:
```env
DEEPSEEK_API_KEY=ваш_ключ_deepseek
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions

YANDEX_VISION_API_KEY=ваш_ключ_yandex
YANDEX_VISION_FOLDER_ID=ваш_folder_id
YANDEX_VISION_ENDPOINT=https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze

API_HOST=0.0.0.0
API_PORT=8000
```

5. **Запустить приложение**:
```bash
cd backend
python -m uvicorn main:app --reload
```

Откройте `http://localhost:8000`

## Desktop приложение

### Сборка Desktop приложения

1. **Установить зависимости**:
```bash
pip install -r requirements.txt
```

2. **Собрать исполняемый файл**:
```bash
python build.py
```

Это создаст `dist/CompetitionMonitor.exe`

3. **Запустить приложение**:
   - Скопируйте файл `.env` в ту же папку, что и `CompetitionMonitor.exe`
   - Дважды кликните на `CompetitionMonitor.exe`

### Использование Desktop приложения

Desktop приложение предоставляет:
- **Вкладка анализа текста**: Анализ текстовых описаний конкурентов
- **Вкладка анализа изображений**: Загрузка и анализ визуального контента
- **Вкладка настроек**: Просмотр статуса конфигурации API

Возможности:
- Автономный исполняемый файл (не требует Python)
- Нативный desktop GUI с PyQt6
- Асинхронный анализ с индикаторами прогресса
- Загрузка примеров текста
- Возможность экспорта результатов

### Деплой на shared hosting (Python 3.6)

Для shared hosting с Python 3.6:

1. Загрузите файлы на сервер
2. Создайте виртуальное окружение:
```bash
python3.6 -m venv venv
source venv/bin/activate
```

3. Установите совместимые с Python 3.6 зависимости:
```bash
pip install -r requirements-python36.txt
```

4. Настройте `.env` с вашими API ключами

5. Запустите uvicorn:
```bash
nohup uvicorn backend.main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
```

6. Настройте Apache (`.htaccess`) для проксирования запросов через `proxy.php`

## API Endpoints

- `GET /` - Отдача frontend
- `GET /health` - Проверка здоровья
- `POST /analyze_text` - Анализ текста конкурента
- `POST /analyze_image` - Анализ изображения
- `GET /history` - Получить историю анализа
- `DELETE /history` - Очистить историю

## Переменные окружения

| Переменная | Описание | Обязательно |
|------------|----------|-------------|
| `DEEPSEEK_API_KEY` | API ключ DeepSeek | Да |
| `DEEPSEEK_API_URL` | Endpoint API DeepSeek | Да |
| `YANDEX_VISION_API_KEY` | API ключ Yandex Cloud | Да |
| `YANDEX_VISION_FOLDER_ID` | Folder ID Yandex Cloud | Да |
| `YANDEX_VISION_ENDPOINT` | Endpoint Yandex Vision | Да |
| `API_HOST` | Хост сервера | Нет (по умолчанию: 0.0.0.0) |
| `API_PORT` | Порт сервера | Нет (по умолчанию: 8000) |

## Использование

1. **Анализ текста**:
   - Вставьте текст конкурента (копия сайта, описание услуг)
   - Опционально введите название конкурента
   - Нажмите "Анализировать текст"
   - Просмотрите оценки и выводы

2. **Анализ изображений**:
   - Загрузите скриншот или изображение дизайна
   - Нажмите "Анализировать изображение"
   - Получите анализ визуального стиля и рекомендации

3. **Загрузить пример**:
   - Нажмите "Загрузить пример" для тестирования с примерными данными

## Настройка API ключей

### DeepSeek API
1. Зарегистрируйтесь на [DeepSeek](https://platform.deepseek.com/)
2. Сгенерируйте API ключ в панели управления
3. Добавьте в файл `.env`

### Yandex Vision
1. Создайте аккаунт на [Yandex Cloud](https://cloud.yandex.com/)
2. Включите Vision API
3. Сгенерируйте API ключ и folder ID
4. Добавьте в файл `.env`

## Разработка

**Кодировка файлов**: Все файлы используют кодировку UTF-8. Русский текст в JavaScript использует Unicode escape sequences для совместимости.

**Совместимость с Python**: Backend совместим с Python 3.6+ для деплоя на shared hosting.

## Лицензия

MIT License

## Автор

Создано в рамках проекта MotionCraft для анализа конкурентов в индустрии моушн-дизайна.

## Поддержка

По вопросам или проблемам создайте issue на GitHub.
