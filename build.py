"""
Скрипт сборки для MotionCraft Competition Analyzer
Создает автономный исполняемый файл с использованием PyInstaller
"""
import PyInstaller.__main__
import sys
import os
from pathlib import Path

def build_executable():
    """Собрать исполняемый файл с помощью PyInstaller"""
    
    # Получить корневую директорию проекта
    project_root = Path(__file__).parent.absolute()
    
    # Аргументы PyInstaller
    args = [
        'desktop_app.py',  # Главный скрипт
        '--name=CompetitionMonitor',  # Имя исполняемого файла
        '--onefile',  # Один исполняемый файл
        '--windowed',  # Без консольного окна
        '--icon=NONE',  # Добавьте путь к иконке, если есть
        
        # Добавить файлы данных
        f'--add-data=frontend{os.pathsep}frontend',
        f'--add-data=.env.example{os.pathsep}.',
        
        # Скрытые импорты
        '--hidden-import=PyQt6',
        '--hidden-import=httpx',
        '--hidden-import=pydantic',
        '--hidden-import=backend',
        '--hidden-import=backend.config',
        '--hidden-import=backend.services',
        '--hidden-import=backend.services.analyzer_service',
        '--hidden-import=backend.models',
        '--hidden-import=backend.models.schemas',
        
        # Чистая сборка
        '--clean',
        
        # Директория вывода
        '--distpath=dist',
        '--workpath=build',
        '--specpath=.',
    ]
    
    print("=" * 60)
    print("Сборка MotionCraft Competition Analyzer")
    print("=" * 60)
    print(f"Корневая директория проекта: {project_root}")
    print(f"Версия Python: {sys.version}")
    print("=" * 60)
    
    # Запустить PyInstaller
    try:
        PyInstaller.__main__.run(args)
        print("\n" + "=" * 60)
        print("Сборка завершена успешно!")
        print("=" * 60)
        print(f"Расположение исполняемого файла: {project_root / 'dist' / 'CompetitionMonitor.exe'}")
        print("\nДля запуска:")
        print("  1. Скопируйте файл .env в ту же папку, что и CompetitionMonitor.exe")
        print("  2. Запустите CompetitionMonitor.exe")
        print("=" * 60)
    except Exception as e:
        print("\n" + "=" * 60)
        print("Ошибка сборки!")
        print("=" * 60)
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_executable()

