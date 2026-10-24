import base64
import xml.etree.ElementTree as ET

class VFSFile:
    """Класс, описывающий файл в нашей виртуальной системе"""
    def __init__(self, name, content):
        self.name = name
        self.content = content

    def get_text(self):
        """Декодирует содержимое из Base64 обратно в обычный текст"""
        try:
            return base64.b64decode(self.content).decode('utf-8')
        except Exception:
            return self.content

class VFSDir:
    """Класс, описывающий папку в нашей виртуальной системе"""
    def __init__(self, name):
        self.name = name
        self.children = {}  # Словарь, где хранятся файлы и папки внутри этой папки

    def add_child(self, child):
        """Добавляет файл или папку внутрь текущей папки"""
        self.children[child.name] = child

def load_vfs(filepath):
    """Функция, которая читает XML-файл и строит дерево объектов в памяти"""
    try:
        # 1. Открываем XML файл
        tree = ET.parse(filepath)
        root = tree.getroot()
        vfs_name = root.get('name', 'unknown_vfs')
        
        # 2. Создаем корневую папку (наш главный диск)
        root_dir = VFSDir("/")
        
        # 3. Вспомогательная функция для обхода вложенных тегов
        def parse_dir(element, current_dir):
            for child in element:
                if child.tag == 'dir':
                    # Если это папка - создаем VFSDir
                    new_dir = VFSDir(child.get('name'))
                    current_dir.add_child(new_dir)
                    parse_dir(child, new_dir) # Заходим внутрь папки (рекурсия)
                elif child.tag == 'file':
                    # Если это файл - создаем VFSFile
                    content = child.text or ""
                    new_file = VFSFile(child.get('name'), content)
                    current_dir.add_child(new_file)

        # 4. Запускаем обход с самого корня
        parse_dir(root, root_dir)
        return root_dir, vfs_name
    except Exception as e:
        raise Exception(f"Ошибка загрузки VFS: {e}")