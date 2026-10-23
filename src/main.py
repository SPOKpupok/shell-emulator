import getpass
import socket
import argparse


def get_prompt():
    user = getpass.getuser()
    host = socket.gethostname()

    return f"{user}@{host}:~"

def parse_command(user_input):
    parts = user_input.strip().split()
    if not parts:
        return None, []
    return parts[0], parts[1:]

def execute_command(command, args):
    """Выполняет команду. Возвращает True (успех), False (ошибка) или 'EXIT'."""
    if command == "exit":
        return "EXIT"
    elif command in ["ls", "cd"]:
        print(f"[STUB] Вызвана команда: {command}")
        if args:
            print(f"[STUB] Аргументы: {args}")
        return True
    # Сюда мы потом добавим tac, cat, uname, mv
    else:
        print(f"Ошибка: команда '{command}' не найдена.")
        return False

def cmd_stub(command, args):
    print(f'[STUB] Вызвана команда: {command}')
    if args:
        print(f"[STUB] Аргументы: {args}")

def main():
    print("Добро пожаловать в эмулятор оболочки (Этап 1: REPL)")
    print("Введите 'exit' для выхода.\n")

def run_script(filepath):
    print(f"\n--- Запуск скрипта: {filepath} ---")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                prompt = get_prompt()
                print(f"{prompt}{line}")

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
    # Настройка аргументов командной строки
    parser = argparse.ArgumentParser(description="Эмулятор оболочки (Этап 2)")
    parser.add_argument("--vfs", help="Путь к виртуальной файловой системе (XML)")
    parser.add_argument("--script", help="Путь к стартовому скрипту")
    args = parser.parse_args()

    # Отладочный вывод параметров (требование Этапа 2)
    print("=== Параметры запуска ===")
    print(f"VFS: {args.vfs if args.vfs else 'не задан'}")
    print(f"Скрипт: {args.script if args.script else 'не задан'}")
    print("=========================\n")

    # Если передан скрипт - выполняем его
    if args.script:
        run_script(args.script)

    # Если VFS задан, но мы на Этапе 2 - просто заглушка
    if args.vfs:
        print(f"[STUB] Загрузка VFS из {args.vfs} (будет реализовано на Этапе 3)")

    # Запуск интерактивного режима
    print("Добро пожаловать в эмулятор оболочки (Этап 2: Конфигурация)")
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
