#!/bin/bash
echo "====================================="
echo "--- ДЕМОНСТРАЦИЯ ЭТАПА 3: VFS ---"
echo "====================================="

echo "1. Загрузка правильной VFS (vfs/example.xml):"
echo "exit" | python src/main.py --vfs vfs/example.xml | head -n 6

echo ""
echo "2. Загрузка несуществующей VFS (vfs/no_such_file.xml):"
echo "exit" | python src/main.py --vfs vfs/no_such_file.xml | head -n 6