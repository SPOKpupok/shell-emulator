import os
import getpass
import socket
import sys


def get_promt():
    user = getpass.getuser()
    host = socket.gethostname()

    return f"{user}@{host}:~"

def parse_command(user_input):
    parts = user_input.strip().split()
    if not parts:
        return None, []
    return parts[0], parts[1:]

def cmd_stub(command, args):
    print(f'[STUB] Вызвана команда: {command}')
    if args:
        print(f"[STUB] Аргументы: {args}")

def main():
    print("Добро пожаловать в эмулятор оболочки (Этап 1: REPL)")
    print("Введите 'exit' для выхода.\n")

    while True:
        try:
            user_input = input(get_promt())
            command, args = parse_command(user_input)

            if command is None:
                continue
            if command=="EXIT":
                print("Выход...")
                break
            elif command in ["ls", "cd"]:
                cmd_stub(command, args)
            else:
                print(f"Ошибка: команда '{command}' не найдена.")

        except KeyboardInterrupt:
            print("\nВыход...")
            break

        except EOFError:
            # Обработка Ctrl+D
            break
if __name__ == "__main__":
    main()

