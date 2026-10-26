#!/bin/bash
# Тестирование глубокой VFS и выполнение скрипта команд

echo "=== Запуск теста: Глубокая VFS со скриптом ==="
python src/main.py --vfs vfs/exmaple3.xml --script scripts/test1.txt
echo "=== Тест завершен ==="