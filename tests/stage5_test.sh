#!/bin/bash
echo "====================================="
echo "--- ДЕМОНСТРАЦИЯ ЭТАПА 5: mv ---"
echo "====================================="

# Создаем файл с командами
cat > /tmp/s5_script.txt << 'EOF'
cd home
ls
mv notes.txt renamed.txt
ls
mv renamed.txt user
ls
cd user
ls
EOF

echo "Выполняем перемещение и переименование:"
python src/main.py --vfs vfs/example.xml --script /tmp/s5_script.txt