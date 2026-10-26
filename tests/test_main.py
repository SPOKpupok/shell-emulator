import unittest
import sys
import os

# Добавляем папку src в пути поиска, чтобы тест видел наши классы
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from vfs import VFSDir, VFSFile

class TestVFS(unittest.TestCase):
    """Тестирование виртуальной файловой системы"""

    def setUp(self):
        """Создаем базовую структуру перед каждым тестом"""
        self.root = VFSDir("/")
        self.home = VFSDir("home", self.root)
        self.root.add_child(self.home)
        self.file = VFSFile("test.txt", "SGVsbG8=") # Hello в base64

    def test_add_child(self):
        """Проверка добавления файла в папку"""
        self.home.add_child(self.file)
        
        # Файл должен появиться в словаре children у папки home
        self.assertIn("test.txt", self.home.children)
        # Родитель файла должен стать папкой home
        self.assertEqual(self.file.parent, self.home)

    def test_get_text(self):
        """Проверка декодирования Base64"""
        text = self.file.get_text()
        self.assertEqual(text, "Hello")

    def test_parent_link(self):
        """Проверка связи родителя и ребенка"""
        self.assertEqual(self.home.parent, self.root)
        self.assertIn("home", self.root.children)

if __name__ == '__main__':
    unittest.main()
