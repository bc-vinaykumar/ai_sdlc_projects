from flask import Flask, render_template, request, jsonify
import uuid
import json

class TodoItem:
    def __init__(self, text: str, completed: bool = False, id: str = None):
        self.id: str = id if id else str(uuid.uuid4())
        self.text: str = text
        self.completed: bool = completed

    def get_id(self) -> str:
        return self.id

    def get_text(self) -> str:
        return self.text

    def is_completed(self) -> bool:
        return self.completed

    def set_completed(self, completed: bool) -> None:
        self.completed = completed

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'text': self.text,
            'completed': self.completed
        }

    @staticmethod
    def from_dict(data: dict) -> 'TodoItem':
        return TodoItem(text=data['text'], completed=data['completed'], id=data['id'])


class TodoList:
    def __init__(self):
        self.items: list[TodoItem] = []

    def add_item(self, text: str) -> None:
        new_item = TodoItem(text=text)
        self.items.append(new_item)

    def delete_item(self, id: str) -> None:
        self.items = [item for item in self.items if item.get_id() != id]

    def complete_item(self, id: str) -> None:
        for item in self.items:
            if item.get_id() == id:
                item.set_completed(True)
                break

    def get_item(self, id: str) -> TodoItem | None:
        for item in self.items:
            if item.get_id() == id:
                return item
        return None

    def get_all_items(self) -> list[TodoItem]:
        return self.items

    def to_dict(self) -> dict:
        return {'items': [item.to_dict() for item in self.items]}

    def from_dict(self, data: dict) -> None:
        self.items = [TodoItem.from_dict(item_data) for item_data in data.get('items', [])]


class WebApp:
    def __init__(self):
        self.app: Flask = Flask(__name__)
        self.todo_list: TodoList = TodoList()
        self.app.config['DEBUG'] = True  # Enable debug mode
        self.add_task_route()
        self.delete_task_route()
        self.complete_task_route()
        self.get_tasks_route()
        self.load_initial_data()  # Load data from a file or default data

    def load_initial_data(self):
        # Load initial data from a file (e.g., data.json)
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                self.todo_list.from_dict(data)
        except FileNotFoundError:
            # If the file doesn't exist, start with an empty todo list
            self.todo_list = TodoList()
        except json.JSONDecodeError:
            print("Error decoding JSON from data.json. Starting with an empty todo list.")
            self.todo_list = TodoList()

    def save_data(self):
        # Save data to a file (e.g., data.json)
        with open('data.json', 'w') as f:
            json.dump(self.todo_list.to_dict(), f)

    def add_task_route(self):
        @self.app.route('/add_task', methods=['POST'])
        def add_task():
            text = request.json.get('text')
            if not text:
                return jsonify({'error': 'Text is required'}), 400

            self.todo_list.add_item(text)
            self.save_data()
            return jsonify([item.to_dict() for item in self.todo_list.get_all_items()])

    def delete_task_route(self):
        @self.app.route('/delete_task/<id>', methods=['POST'])
        def delete_task(id: str):
            self.todo_list.delete_item(id)
            self.save_data()
            return jsonify([item.to_dict() for item in self.todo_list.get_all_items()])

    def complete_task_route(self):
        @self.app.route('/complete_task/<id>', methods=['POST'])
        def complete_task(id: str):
            self.todo_list.complete_item(id)
            self.save_data()
            return jsonify([item.to_dict() for item in self.todo_list.get_all_items()])

    def get_tasks_route(self):
        @self.app.route('/get_tasks', methods=['GET'])
        def get_tasks():
            return jsonify([item.to_dict() for item in self.todo_list.get_all_items()])

    def run(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        self.app.run()


if __name__ == '__main__':
    web_app = WebApp()
    web_app.run()
