# llm_agent/tool_todolist.py

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class TodoListTool:
    """
    Инструмент для управления списком задач (Todo List)
    Поддерживает: добавление, удаление, отметка выполнения, просмотр
    """
    name = "todo_list"
    description = """
    Поддерживает команды:
    add: добавить новую задачу
    list: показать все задачи
    done: отметить задачу как выполненную
    delete: удалить задачу
    clear: очистить все задачи
    """

    def __init__(self, storage_path: str = "data/todos.json"):
        """Инициализация инструмента"""
        self.storage_path = storage_path
        self._ensure_storage_exists()
        self.todos = self._load_todos()

    def _ensure_storage_exists(self):
        """Создаёт папку и файл для хранения, если их нет"""
        path = Path(self.storage_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            with open(path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _load_todos(self) -> List[Dict]:
        """Загружает задачи из JSON файла"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_todos(self):
        """Сохраняет задачи в JSON файл"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.todos, f, ensure_ascii=False, indent=2)

    def _get_next_id(self) -> int:
        """Генерирует следующий ID для задачи"""
        if not self.todos:
            return 1
        return max(todo['id'] for todo in self.todos) + 1

    def use(self, command: str, *args) -> str:
        """
        Основной метод для выполнения команд
        Args:
            command: команда (add, list, done, delete, clear)
            *args: аргументы для команды
        Returns:
            str: результат выполнения команды
        """
        command = command.lower().strip()
        
        if command == "add":
            if not args:
                return "Ошибка: укажите текст задачи"
            return self._add_task(args[0])
        
        elif command == "list":
            return self._list_tasks()
        
        elif command == "done":
            if not args:
                return "Ошибка: укажите ID задачи."
            try:
                task_id = int(args[0])
                return self._mark_done(task_id)
            except ValueError:
                return "Ошибка: ID должен быть числом"
        
        elif command == "delete":
            if not args:
                return "Ошибка: укажите ID задачи."
            try:
                task_id = int(args[0])
                return self._delete_task(task_id)
            except ValueError:
                return "Ошибка: ID должен быть числом"
        
        elif command == "clear":
            return self._clear_all()
        
        else:
            return f"Неизвестная команда. Доступные: add, list, done, delete, clear"

    def _add_task(self, text: str) -> str:
        """Добавляет новую задачу"""
        task = {
            "id": self._get_next_id(),
            "text": text,
            "done": False,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.todos.append(task)
        self._save_todos()
        return f"Задача #{task['id']} добавлена: {text}"

    def _list_tasks(self) -> str:
        """Показывает все задачи"""
        if not self.todos:
            return "Список задач пуст"
        
        # Разделяем на выполненные и невыполненные
        pending = [t for t in self.todos if not t['done']]
        completed = [t for t in self.todos if t['done']]
        
        result = []
        
        if pending:
            result.append("Невыполненные задачи:")
            for task in pending:
                result.append(f"  {task['id']}. {task['text']}")
        
        if completed:
            result.append("\nВыполненные задачи:")
            for task in completed:
                result.append(f"  {task['id']}. {task['text']}")
        
        result.append(f"\nВсего: {len(self.todos)} задач "
                     f"(невыполненных: {len(pending)}, выполненных: {len(completed)})")
        
        return "\n".join(result)

    def _mark_done(self, task_id: int) -> str:
        """Отмечает задачу как выполненную"""
        for task in self.todos:
            if task['id'] == task_id:
                if task['done']:
                    return f"Задача #{task_id} уже выполнена"
                task['done'] = True
                task['updated_at'] = datetime.now().isoformat()
                self._save_todos()
                return f"Задача #{task_id} отмечена как выполненная: {task['text']}"
        
        return f"❌ Задача #{task_id} не найдена"

    def _delete_task(self, task_id: int) -> str:
        """Удаляет задачу"""
        for i, task in enumerate(self.todos):
            if task['id'] == task_id:
                text = task['text']
                del self.todos[i]
                self._save_todos()
                return f"Задача #{task_id} удалена: {text}"
        
        return f"Задача #{task_id} не найдена"

    def _clear_all(self) -> str:
        """Очищает все задачи"""
        count = len(self.todos)
        if count == 0:
            return "Список задач уже пуст"
        
        self.todos = []
        self._save_todos()
        return f"Удалено {count} задач"

    def get_stats(self) -> Dict:
        """Возвращает статистику задач"""
        total = len(self.todos)
        done = sum(1 for t in self.todos if t['done'])
        pending = total - done
        return {
            "total": total,
            "done": done,
            "pending": pending
        }