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

# --- Функции для команд ---

def cmd_ls(args):
    target_dir = CURRENT_DIR
    if args:
        target_dir = CURRENT_DIR.children.get(args[0])
        if not target_dir or not isinstance(target_dir, VFSDir):
            print(f"ls: нет доступа к '{args[0]}': Нет такого файла или каталога")
            return True

    items = list(target_dir.children.keys())
    if items:
        print("  ".join(items))
    return True

def cmd_cd(args):
    global CURRENT_DIR
    if not args:
        if CURRENT_DIR.parent:
            CURRENT_DIR = CURRENT_DIR.parent
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
            print(f"cd: нет такого файла или каталога: {target_name}")
        return True

def cmd_uname(args):
    print(VFS_NAME)
    return True

def cmd_tac(args):
    if not args:
        print("tac: не указан файл")
        return True
    
    target = CURRENT_DIR.children.get(args[0])
    if target and isinstance(target, VFSFile):
        text = target.get_text()
        lines = text.splitlines()
        for line in reversed(lines):
            print(line)
    else:
        print(f"tac: {args[0]}: Нет такого файла или каталога")
    return True

def cmd_mv(args):
    global CURRENT_DIR
    if len(args) != 2:
        print("mv: не указаны файлы для перемещения")
        return True
    
    source_name, dest_name = args[0], args[1]
    source = CURRENT_DIR.children.get(source_name)
    if not source:
        print(f"mv: невозможно переместить '{source_name}': Нет такого файла или каталога")
        return True

    dest_obj = CURRENT_DIR.children.get(dest_name)
    
    if dest_obj and isinstance(dest_obj, VFSDir):
        target_dir = dest_obj
        del CURRENT_DIR.children[source_name]
        target_dir.add_child(source)
        print(f"'{source_name}' перемещен в каталог '{dest_name}'")
    else:
        del CURRENT_DIR.children[source_name]
        source.name = dest_name
        CURRENT_DIR.children[dest_name] = source
        print(f"'{source_name}' переименован в '{dest_name}'")
    return True

# --- Главный диспетчер команд ---

def execute_command(command, args):
    # Словарь, который связывает название команды и функцию
    commands = {
        "ls": cmd_ls,
        "cd": cmd_cd,
        "uname": cmd_uname,
        "tac": cmd_tac,
        "mv": cmd_mv
    }
    
    if command == "exit":
        return "EXIT"
        
    if command in commands:
        return commands[command](args)
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