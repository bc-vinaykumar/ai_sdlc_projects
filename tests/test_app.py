import unittest
import json
import os
from unittest.mock import patch
from flask import Flask
from data.simple_todo_list.app import TodoItem, TodoList, WebApp


## TodoItem Tests
class TestTodoItem(unittest.TestCase):
    """
    Test cases for the TodoItem class.
    """

    def test_todo_item_creation(self):
        """
        Test that a TodoItem can be created with the correct attributes.
        """
        item: TodoItem = TodoItem(text="Test Task")
        self.assertEqual(item.get_text(), "Test Task")
        self.assertFalse(item.is_completed())
        self.assertIsNotNone(item.get_id())

        item2: TodoItem = TodoItem(text="Test Task 2", completed=True, id="test_id")
        self.assertEqual(item2.get_text(), "Test Task 2")
        self.assertTrue(item2.is_completed())
        self.assertEqual(item2.get_id(), "test_id")

    def test_todo_item_getters_and_setters(self):
        """
        Test the getter and setter methods of the TodoItem class.
        """
        item: TodoItem = TodoItem(text="Test Task")
        item.set_completed(True)
        self.assertTrue(item.is_completed())
        self.assertEqual(item.get_text(), "Test Task")

    def test_todo_item_to_dict(self):
        """
        Test the to_dict method of the TodoItem class.
        """
        item: TodoItem = TodoItem(text="Test Task", completed=True, id="test_id")
        item_dict: dict = item.to_dict()
        self.assertEqual(item_dict['id'], "test_id")
        self.assertEqual(item_dict['text'], "Test Task")
        self.assertTrue(item_dict['completed'])

    def test_todo_item_from_dict(self):
        """
        Test the from_dict method of the TodoItem class.
        """
        item_dict: dict = {'id': "test_id", 'text': "Test Task", 'completed': True}
        item: TodoItem = TodoItem.from_dict(item_dict)
        self.assertEqual(item.get_id(), "test_id")
        self.assertEqual(item.get_text(), "Test Task")
        self.assertTrue(item.is_completed())


## TodoList Tests
class TestTodoList(unittest.TestCase):
    """
    Test cases for the TodoList class.
    """

    def setUp(self):
        """
        Set up a TodoList instance for each test.
        """
        self.todo_list: TodoList = TodoList()

    def test_add_item(self):
        """
        Test adding an item to the TodoList.
        """
        self.todo_list.add_item("Test Task")
        self.assertEqual(len(self.todo_list.items), 1)
        self.assertEqual(self.todo_list.items[0].get_text(), "Test Task")

    def test_delete_item(self):
        """
        Test deleting an item from the TodoList.
        """
        self.todo_list.add_item("Test Task")
        item_id: str = self.todo_list.items[0].get_id()
        self.todo_list.delete_item(item_id)
        self.assertEqual(len(self.todo_list.items), 0)

    def test_complete_item(self):
        """
        Test completing an item in the TodoList.
        """
        self.todo_list.add_item("Test Task")
        item_id: str = self.todo_list.items[0].get_id()
        self.todo_list.complete_item(item_id)
        self.assertTrue(self.todo_list.items[0].is_completed())

    def test_get_item(self):
        """
        Test getting an item from the TodoList.
        """
        self.todo_list.add_item("Test Task")
        item_id: str = self.todo_list.items[0].get_id()
        item: TodoItem | None = self.todo_list.get_item(item_id)
        self.assertEqual(item.get_text(), "Test Task")

        item2: TodoItem | None = self.todo_list.get_item("non_existent_id")
        self.assertIsNone(item2)

    def test_get_all_items(self):
        """
        Test getting all items from the TodoList.
        """
        self.todo_list.add_item("Test Task 1")
        self.todo_list.add_item("Test Task 2")
        items: list[TodoItem] = self.todo_list.get_all_items()
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].get_text(), "Test Task 1")
        self.assertEqual(items[1].get_text(), "Test Task 2")

    def test_to_dict(self):
        """
        Test the to_dict method of the TodoList class.
        """
        self.todo_list.add_item("Test Task")
        todo_dict: dict = self.todo_list.to_dict()
        self.assertEqual(len(todo_dict['items']), 1)
        self.assertEqual(todo_dict['items'][0]['text'], "Test Task")

    def test_from_dict(self):
        """
        Test the from_dict method of the TodoList class.
        """
        data: dict = {'items': [{'id': "test_id", 'text': "Test Task", 'completed': True}]}
        self.todo_list.from_dict(data)
        self.assertEqual(len(self.todo_list.items), 1)
        self.assertEqual(self.todo_list.items[0].get_text(), "Test Task")
        self.assertEqual(self.todo_list.items[0].get_id(), "test_id")
        self.assertTrue(self.todo_list.items[0].is_completed())

    def test_from_dict_empty_items(self):
        """
        Test the from_dict method with empty items.
        """
        data: dict = {}
        self.todo_list.from_dict(data)
        self.assertEqual(len(self.todo_list.items), 0)

        data2: dict = {'items': []}
        self.todo_list.from_dict(data2)
        self.assertEqual(len(self.todo_list.items), 0)


## WebApp Tests
class TestWebApp(unittest.TestCase):
    """
    Test cases for the WebApp class.
    """

    def setUp(self):
        """
        Set up a WebApp instance for each test.
        """
        self.web_app: WebApp = WebApp()
        self.app: Flask = self.web_app.app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # Clean up data.json before each test
        if os.path.exists('data.json'):
            os.remove('data.json')

    def tearDown(self):
        """
        Clean up data.json after each test.
        """
        if os.path.exists('data.json'):
            os.remove('data.json')

    def test_add_task_route(self):
        """
        Test the add_task route.
        """
        response = self.client.post('/add_task', json={'text': 'Test Task'})
        self.assertEqual(response.status_code, 200)
        data: list[dict] = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['text'], 'Test Task')
        self.assertFalse(data[0]['completed'])

        # Test with missing text
        response = self.client.post('/add_task', json={})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'Text is required')

    def test_delete_task_route(self):
        """
        Test the delete_task route.
        """
        # First, add a task
        self.client.post('/add_task', json={'text': 'Test Task'})
        # Get the task ID
        response = self.client.get('/get_tasks')
        data: list[dict] = json.loads(response.get_data(as_text=True))
        task_id: str = data[0]['id']

        # Delete the task
        response = self.client.post(f'/delete_task/{task_id}')
        self.assertEqual(response.status_code, 200)
        data: list[dict] = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 0)

    def test_complete_task_route(self):
        """
        Test the complete_task route.
        """
        # First, add a task
        self.client.post('/add_task', json={'text': 'Test Task'})
        # Get the task ID
        response = self.client.get('/get_tasks')
        data: list[dict] = json.loads(response.get_data(as_text=True))
        task_id: str = data[0]['id']

        # Complete the task
        response = self.client.post(f'/complete_task/{task_id}')
        self.assertEqual(response.status_code, 200)
        data: list[dict] = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 1)
        self.assertTrue(data[0]['completed'])

    def test_get_tasks_route(self):
        """
        Test the get_tasks route.
        """
        # Add some tasks
        self.client.post('/add_task', json={'text': 'Test Task 1'})
        self.client.post('/add_task', json={'text': 'Test Task 2'})

        # Get the tasks
        response = self.client.get('/get_tasks')
        self.assertEqual(response.status_code, 200)
        data: list[dict] = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['text'], 'Test Task 1')
        self.assertEqual(data[1]['text'], 'Test Task 2')

    def test_load_initial_data_from_file(self):
        """
        Test loading initial data from a file.
        """
        # Create a data.json file
        data: dict = {'items': [{'id': 'test_id', 'text': 'Test Task', 'completed': True}]}
        with open('data.json', 'w') as f:
            json.dump(data, f)

        # Create a new WebApp instance
        web_app: WebApp = WebApp()

        # Check that the data was loaded correctly
        self.assertEqual(len(web_app.todo_list.items), 1)
        self.assertEqual(web_app.todo_list.items[0].get_text(), 'Test Task')
        self.assertEqual(web_app.todo_list.items[0].get_id(), 'test_id')
        self.assertTrue(web_app.todo_list.items[0].is_completed())

    def test_load_initial_data_file_not_found(self):
        """
        Test loading initial data when the file is not found.
        """
        # Ensure data.json does not exist
        if os.path.exists('data.json'):
            os.remove('data.json')

        # Create a new WebApp instance
        web_app: WebApp = WebApp()

        # Check that the todo list is empty
        self.assertEqual(len(web_app.todo_list.items), 0)

    def test_load_initial_data_invalid_json(self):
        """
        Test loading initial data when the JSON is invalid.
        """
        # Create a data.json file with invalid JSON
        with open('data.json', 'w') as f:
            f.write('invalid json')

        # Create a new WebApp instance
        web_app: WebApp = WebApp()

        # Check that the todo list is empty
        self.assertEqual(len(web_app.todo_list.items), 0)

    def test_save_data(self):
        """
        Test saving data to a file.
        """
        # Add some tasks to the todo list
        self.web_app.todo_list.add_item('Test Task 1')
        self.web_app.todo_list.add_item('Test Task 2')

        # Save the data
        self.web_app.save_data()

        # Load the data from the file
        with open('data.json', 'r') as f:
            data: dict = json.load(f)

        # Check that the data was saved correctly
        self.assertEqual(len(data['items']), 2)
        self.assertEqual(data['items'][0]['text'], 'Test Task 1')
        self.assertEqual(data['items'][1]['text'], 'Test Task 2')


if __name__ == '__main__':
    unittest.main()
