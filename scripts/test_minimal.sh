#!/bin/bash
# Тестирование минимальной VFS без стартового скрипта

echo "=== Запуск теста: Минимальная VFS ==="
python src/main.py --vfs vfs/example2.xml
echo "=== Тест завершен ==="