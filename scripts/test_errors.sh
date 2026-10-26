#!/bin/bash
# Тестирование обработки ошибок

echo "=== Запуск теста: Обработка ошибок ==="

echo "1. Запуск с несуществующей VFS:"
python src/main.py --vfs vfs/not_found.xml

echo ""
echo "2. Запуск с несуществующим скриптом:"
python src/main.py --vfs vfs/example.xml --script scripts/not_found.txt

echo "=== Тест завершен ==="