# test_todolist.py

import unittest
import json
import os
import tempfile
from llm_agent.tool_todolist import TodoListTool


class TestTodoListTool(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(
            suffix='.json', 
            delete=False,
            mode='w+'
        )
        self.temp_file.close()
        self.storage_path = self.temp_file.name
        self.tool = TodoListTool(storage_path=self.storage_path)

    def tearDown(self):
        if os.path.exists(self.storage_path):
            os.unlink(self.storage_path)

    def test_add_task(self):
        """ Добавление задачи"""
        result = self.tool.use("add", "Купить молоко")
        self.assertIn("Задача #1 добавлена", result)
        self.assertIn("Купить молоко", result)
        
        # Проверяем, что задача сохранилась
        todos = self.tool._load_todos()
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0]['text'], "Купить молоко")
        self.assertFalse(todos[0]['done'])

    def test_list_tasks(self):
        """Просмотр списка задач"""
        # Добавляем несколько задач
        self.tool.use("add", "Задача 1")
        self.tool.use("add", "Задача 2")
        
        # Проверяем список
        result = self.tool.use("list")
        self.assertIn("Задача 1", result)
        self.assertIn("Задача 2", result)
        self.assertIn("Невыполненные задачи", result)

    def test_mark_done(self):
        """Отметка задачи как выполненной"""
        self.tool.use("add", "Сделать дз")
        
        # Проверяем, что задача не выполнена
        todos = self.tool._load_todos()
        self.assertFalse(todos[0]['done'])
        
        # Отмечаем как выполненную
        result = self.tool.use("done", "1")
        self.assertIn("Задача 1 отмечена выполненой", result)
        
        # Проверяем, что задача выполнена
        todos = self.tool._load_todos()
        self.assertTrue(todos[0]['done'])

    def test_delete_task(self):
        """Удаление задачи"""
        self.tool.use("add", "Удалить меня")
        self.assertEqual(len(self.tool._load_todos()), 1)
        
        result = self.tool.use("delete", "1")
        self.assertIn("Задача 1 удалена", result)
        self.assertEqual(len(self.tool._load_todos()), 0)


def run_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestTodoListTool)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    run_tests()