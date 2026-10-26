#!/bin/bash
echo "====================================="
echo "--- ДЕМОНСТРАЦИЯ ЭТАПА 2: Конфигурация ---"
echo "====================================="
echo "Передаем параметры --vfs и --script:"

# Создаем временный файл со скриптом
cat > /tmp/s2.txt << 'EOF'
ls
qwerty
exit
EOF

python src/main.py --vfs vfs/example.xml --script /tmp/s2.txt