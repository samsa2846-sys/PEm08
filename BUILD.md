# Инструкция по сборке и тестированию

## Шаг 1: Подготовка окружения

```bash
# Создать виртуальное окружение
python -m venv venv

# Активировать (Windows)
venv\Scripts\activate

# Активировать (Linux/Mac)
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
```

## Шаг 2: Настройка API ключей

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Заполните API ключи в `.env`:
```env
DEEPSEEK_API_KEY=ваш_ключ_deepseek
YANDEX_VISION_API_KEY=ваш_ключ_yandex
YANDEX_VISION_FOLDER_ID=ваш_folder_id
```

**⚠️ ВАЖНО**: Файл `.env` уже добавлен в `.gitignore` - он НЕ попадет в Git!

## Шаг 3: Тестирование перед сборкой

### Тест desktop приложения:
```bash
python desktop_app.py
```

Проверьте:
- ✅ Приложение запускается
- ✅ Вкладки переключаются
- ✅ Загрузка примера работает
- ✅ Анализ текста выполняется
- ✅ Загрузка изображения работает
- ✅ Анализ изображения выполняется

### Тест web приложения:
```bash
cd backend
python -m uvicorn main:app --reload
```

Откройте http://localhost:8000 и проверьте функциональность.

## Шаг 4: Сборка desktop приложения

```bash
python build.py
```

Результат: `dist/CompetitionMonitor.exe`

## Шаг 5: Тестирование CompetitionMonitor.exe

1. Скопируйте `.env` в папку `dist/`:
```bash
copy .env dist\.env
```

2. Запустите `dist/CompetitionMonitor.exe`

3. Проверьте все функции:
   - Анализ текста с примером
   - Загрузка и анализ изображения
   - Корректное отображение результатов

## Шаг 6: Публикация на GitHub

```bash
# Добавить новые файлы
git add desktop_app.py build.py BUILD.md
git add requirements.txt backend/config.py
git add .gitignore README.md

# Коммит
git commit -m "Add desktop application with PyQt6 and build script"

# Пуш
git push origin main
```

## Проверка безопасности

✅ Убедитесь, что `.env` **НЕ** в репозитории:
```bash
git status
# .env не должен отображаться

git ls-files | grep .env
# Должен показать только .env.example
```

✅ Проверьте `.gitignore`:
```bash
cat .gitignore | grep .env
# Должно быть: .env
```

## Результат

После выполнения всех шагов:
1. ✅ Desktop приложение собрано и протестировано
2. ✅ CompetitionMonitor.exe работает
3. ✅ Репозиторий опубликован на GitHub
4. ✅ API ключи защищены (в .env, который в .gitignore)
5. ✅ README описывает весь проект

## Troubleshooting

### Ошибка при сборке PyInstaller
```bash
pip install --upgrade pyinstaller
python build.py
```

### Ошибка "module not found"
```bash
pip install --upgrade -r requirements.txt
```

### .exe не находит модули
Добавьте в `build.py` hidden-import:
```python
'--hidden-import=имя_модуля',
```

