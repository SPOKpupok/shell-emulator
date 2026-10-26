#!/bin/bash
echo "====================================="
echo "--- ДЕМОНСТРАЦИЯ ЭТАПА 4: Основные команды ---"
echo "====================================="

# Создаем файл с командами
cat > /tmp/s4_script.txt << 'EOF'
ls
cd home
ls
uname
cd user
tac readme.txt
EOF

echo "Выполняем команды из скрипта:"
python src/main.py --vfs vfs/example.xml --script /tmp/s4_script.txt