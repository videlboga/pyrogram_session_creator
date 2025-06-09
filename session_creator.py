#!/usr/bin/env python3

"""
🐱 CyberKitty Pyrogram Session Creator
=====================================

Простой интерактивный инструмент для создания Pyrogram сессий.
Работает независимо от любых других систем.

Версия: 1.0.0

Автор: Команда CyberKitty 🐾
GitHub: https://github.com/videlboga/pyrogram_session_creator
"""

import os
import sys
import random
from pathlib import Path

def meow():
    """Добавляет случайное мяуканье 🐱"""
    meows = ["🐱 Мяу!", "🐾 Мррр~", "😸 Мяяяу!", "🐱 Мур-мур!", "😻 Мяв!", "🐾 Мррряу!"]
    return random.choice(meows)


def check_dependencies():
    """Проверяет наличие необходимых зависимостей"""
    try:
        import pyrogram
        print(f"{meow()} Pyrogram найден!")
        return True
    except ImportError:
        print(f"❌ {meow()} Ошибка: Pyrogram не установлен!")
        print("📦 Установите командой: pip install pyrogram")
        print("💡 Для ускорения также установите: pip install tgcrypto")
        return False

def print_banner():
    """Выводит красивый баннер"""
    print("\n" + "🔐" + "="*60)
    print("   CYBERKITTY PYROGRAM SESSION CREATOR v1.0.0")
    print("   Создание сессий Telegram быстро и просто")
    print("="*62)
    print()

def get_api_credentials():
    """Получает API credentials интерактивно"""
    print("📋 Для создания сессии нужны API данные:")
    print("   1. Идите на https://my.telegram.org/apps")
    print("   2. Создайте новое приложение")
    print("   3. Скопируйте API ID и API Hash")
    print()
    
    while True:
        api_id = input("🔑 Введите API ID: ").strip()
        if api_id.isdigit():
            api_id = int(api_id)
            break
        else:
            print("❌ API ID должен содержать только цифры!")
    
    while True:
        api_hash = input("🔑 Введите API Hash: ").strip()
        if len(api_hash) == 32 and all(c in '0123456789abcdef' for c in api_hash.lower()):
            break
        else:
            print("❌ API Hash должен быть 32-символьной hex строкой!")
    
    return api_id, api_hash

def get_session_details():
    """Получает детали сессии"""
    print()
    session_name = input("📝 Имя файла сессии (без .session): ").strip()
    if not session_name:
        session_name = "my_telegram_session"
    
    # Убираем .session если добавлено
    if session_name.endswith('.session'):
        session_name = session_name[:-8]
    
    # Получаем директорию
    current_dir = os.getcwd()
    print(f"📁 Текущая директория: {current_dir}")
    save_here = input("💾 Сохранить сессию здесь? (Y/n): ").strip().lower()
    
    if save_here in ['n', 'no', 'нет']:
        output_dir = input("📂 Введите путь для сохранения: ").strip()
        if not output_dir:
            output_dir = current_dir
    else:
        output_dir = current_dir
    
    # Создаем директорию если нужно
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    session_path = os.path.join(output_dir, session_name)
    
    return session_path

def create_session_interactive(api_id, api_hash, session_path):
    """Создает сессию интерактивно"""
    from pyrogram import Client
    
    print()
    print("🚀 Начинаю создание сессии...")
    print("📱 Подключаюсь к Telegram...")
    
    try:
        # Создаем клиент
        app = Client(
            session_path,
            api_id=api_id,
            api_hash=api_hash
        )
        
        print("✅ Соединение установлено!")
        print("📲 Сейчас потребуется авторизация через Telegram...")
        print()
        
        # Запускаем авторизацию
        with app:
            me = app.get_me()
            
            print()
            print("🎉 Авторизация успешна!")
            print(f"👤 Пользователь: {me.first_name} {me.last_name or ''}")
            if me.username:
                print(f"🔗 Username: @{me.username}")
            print(f"📞 Телефон: {me.phone_number}")
            print()
            
            session_file = f"{session_path}.session"
            print(f"💾 Сессия сохранена: {session_file}")
            
            if os.path.exists(session_file):
                size = os.path.getsize(session_file)
                print(f"📊 Размер: {size:,} байт")
            
            print()
            print("✨ Готово! Теперь используйте сессию в своих проектах:")
            print(f'   app = Client("{session_path}")')
            
            print(f"{meow()} Pyrogram найден!")
        return True
            
    except KeyboardInterrupt:
        print("\n❌ Операция прервана пользователем")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def cleanup_on_failure(session_path):
    """Очищает файлы при неудаче"""
    files_to_remove = [
        f"{session_path}.session",
        f"{session_path}.session-shm",
        f"{session_path}.session-wal"
    ]
    
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️  Удален: {file_path}")
            except:
                pass

def main():
    """Основная функция"""
    print_banner()
    
    # Проверяем зависимости
    if not check_dependencies():
        sys.exit(1)
    
    try:
        # Получаем API данные
        api_id, api_hash = get_api_credentials()
        
        # Получаем детали сессии
        session_path = get_session_details()
        
        # Проверяем существование файла
        session_file = f"{session_path}.session"
        if os.path.exists(session_file):
            print(f"⚠️  Файл {session_file} уже существует!")
            overwrite = input("🔄 Перезаписать? (y/N): ").strip().lower()
            if overwrite not in ['y', 'yes', 'да']:
                print("❌ Операция отменена")
                return
        
        # Создаем сессию
        success = create_session_interactive(api_id, api_hash, session_path)
        
        if success:
            print("🎊 Сессия успешно создана и готова к использованию!")
        else:
            cleanup_on_failure(session_path)
            print("💥 Не удалось создать сессию")
            
    except KeyboardInterrupt:
        print("\n👋 До свидания!")
    except Exception as e:
        print(f"💥 Неожиданная ошибка: {e}")

if __name__ == "__main__":
    main() 