import getpass
import socket
import argparse
from vfs import load_vfs, VFSDir, VFSFile

# Глобальные переменные для нашего состояния
CURRENT_DIR = None
VFS_NAME = "unknown"

def get_prompt():
    user = getpass.getuser()
    host = socket.gethostname()
    # Формируем путь для приглашения (пока просто имя текущей папки)
    cwd = CURRENT_DIR.name if CURRENT_DIR else "~"
    if cwd == "/":
        cwd = "/"
    return f"{user}@{host}:{cwd}$ "

def parse_command(user_input):
    parts = user_input.strip().split()
    if not parts:
        return None, []
    return parts[0], parts[1:]

def execute_command(command, args):
    global CURRENT_DIR, VFS_NAME
    
    if command == "exit":
        return "EXIT"
        
    elif command == "ls":
        # Если аргументов нет - показываем текущую папку
        target_dir = CURRENT_DIR
        if args:
            # Если аргумент есть, пытаемся найти папку (упрощенно, только для текущей директории)
            target_dir = CURRENT_DIR.children.get(args[0])
            if not target_dir or not isinstance(target_dir, VFSDir):
                print(f"ls: cannot access '{args[0]}': No such file or directory")
                return True

        # Выводим содержимое
        items = list(target_dir.children.keys())
        if items:
            print("  ".join(items))
        return True

    elif command == "cd":
        if not args:
            # cd без аргументов ведет в корень
            CURRENT_DIR = CURRENT_DIR.parent if CURRENT_DIR.parent else CURRENT_DIR
            return True
        
        target_name = args[0]
        
        if target_name == "..":
            if CURRENT_DIR.parent:
                CURRENT_DIR = CURRENT_DIR.parent
            return True
        elif target_name == "/":
            while CURRENT_DIR.parent:
                CURRENT_DIR = CURRENT_DIR.parent
            return True
        else:
            target = CURRENT_DIR.children.get(target_name)
            if target and isinstance(target, VFSDir):
                CURRENT_DIR = target
            else:
                print(f"cd: no such file or directory: {target_name}")
            return True

    elif command == "uname":
        print(VFS_NAME)
        return True

    elif command == "tac":
        if not args:
            print("tac: missing file operand")
            return True
        
        target = CURRENT_DIR.children.get(args[0])
        if target and isinstance(target, VFSFile):
            # Читаем текст и переворачиваем строки
            text = target.get_text()
            lines = text.splitlines()
            for line in reversed(lines):
                print(line)
        else:
            print(f"tac: {args[0]}: No such file or directory")
        return True

    elif command == "mv":
        # Проверяем, что переданы два аргумента: откуда и куда
        if len(args) != 2:
            print("mv: missing file operand")
            return True
        
        source_name = args[0]
        dest_name = args[1]

        # 1. Ищем исходный файл или папку в текущей директории
        source = CURRENT_DIR.children.get(source_name)
        if not source:
            print(f"mv: cannot stat '{source_name}': No such file or directory")
            return True

        # 2. Проверяем, куда мы перемещаем (dest_name)
        # Если dest_name совпадает с именем существующей папки в текущей директории
        dest_obj = CURRENT_DIR.children.get(dest_name)
        
        if dest_obj and isinstance(dest_obj, VFSDir):
            # Перемещение ВНУТРЬ папки
            target_dir = dest_obj
            
            # Удаляем из старой папки
            del CURRENT_DIR.children[source_name]
            
            # Добавляем в новую папку (перезаписываем, если там уже есть файл с таким именем)
            target_dir.add_child(source)
            
            print(f"Файл '{source_name}' перемещен в папку '{dest_name}'")
            
        else:
            # ПЕРЕИМЕНОВАНИЕ (если второго аргумента-папки нет, просто меняем имя)
            
            # Удаляем старый ключ из словаря текущей папки
            del CURRENT_DIR.children[source_name]
            
            # Меняем имя самому объекту
            source.name = dest_name
            
            # Добавляем обратно в текущую папку уже с новым именем
            CURRENT_DIR.children[dest_name] = source
            
            print(f"Файл переименован в '{dest_name}'")
            
        return True

    else:
        print(f"Ошибка: команда '{command}' не найдена.")
        return False

    

    


def run_script(filepath):
    print(f"\n--- Запуск скрипта: {filepath} ---")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"): continue
                
                print(f"{get_prompt()}{line}")
                cmd, args = parse_command(line)
                res = execute_command(cmd, args)
                
                if res == "EXIT":
                    print("Выход...")
                    return
                if res is False:
                    print("[!] Ошибка выполнения скрипта. Остановка.")
                    return
    except FileNotFoundError:
        print(f"Ошибка: Файл скрипта не найден: {filepath}")
    print("--- Завершение скрипта ---\n")

def main():
    global CURRENT_DIR, VFS_NAME
    
    parser = argparse.ArgumentParser(description="Эмулятор оболочки (Этап 4)")
    parser.add_argument("--vfs", help="Путь к VFS (XML)")
    parser.add_argument("--script", help="Путь к стартовому скрипту")
    args = parser.parse_args()

    print("=== Параметры запуска ===")
    print(f"VFS: {args.vfs if args.vfs else 'не задан'}")
    print(f"Скрипт: {args.script if args.script else 'не задан'}")
    print("=========================\n")

    # Загрузка VFS
    if args.vfs:
        try:
            CURRENT_DIR, VFS_NAME = load_vfs(args.vfs)
            print(f"Успешно загружена VFS: '{VFS_NAME}'")
        except Exception as e:
            print(e)
    else:
        # Создаем пустую VFS, если файл не передан
        CURRENT_DIR = VFSDir("/")
        VFS_NAME = "empty_vfs"

    if args.script:
        run_script(args.script)

    print("Добро пожаловать в эмулятор оболочки (Этап 4)")
    print("Введите 'exit' для выхода.\n")

    while True:
        try:
            user_input = input(get_prompt())
            command, cmd_args = parse_command(user_input)
            
            if command is None:
                continue

            res = execute_command(command, cmd_args)
            if res == "EXIT":
                print("Выход...")
                break

        except KeyboardInterrupt:
            print("\nВыход...")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()