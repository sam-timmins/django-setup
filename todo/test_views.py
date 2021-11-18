from django.test import TestCase
from .models import Item

# Create your tests here.
class testViews(TestCase):

    def test_get_todo(self):
        """
        Sets response to equal the home page
        Checks to see if the response code is suuccessful, code 200
        Confirms that template it uses is correct
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_list.html')


    def test_get_add_item_page(self):
        """
        Sets response to equal the add page
        Checks to see if the response code is suuccessful, code 200
        Confirms that template it uses is correct
        """
        response = self.client.get('/add')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/add_item.html')

    
    def test_get_edit_item_page(self):
        """
        Creates an item to use in the test
        Sets response to equal the edit page with the item's id added to the end
        Checks to see if the response code is suuccessful, code 200
        Confirms that template it uses is correct
        """
        item = Item.objects.create(name='Test Todo Item')
        response = self.client.get(f'/edit/{item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/edit_item.html')


    def test_can_add_item(self):
        """
        Sets response to an item as if one has been submitted
        Confirms redirect back to the homepage
        """
        response = self.client.post('/add', {'name': 'Test Added ITem'})
        self.assertRedirects(response, '/')


    def test_can_toggle_item(self):
        """
        Sets response to an item as if one has been submitted
        Create a get request to delete with the item's id added to the end
        Confirms redirect back to the homepage
        Check it has been deleted by attempting to get it from the database.
        Check the length of the existing items
        """
        item = Item.objects.create(name='Test Todo Item')
        response = self.client.get(f'/delete/{item.id}')
        self.assertRedirects(response, '/')
        existing_items = Item.objects.filter(id=item.id)
        self.assertEqual(len(existing_items), 0)


    def test_can_delete_item(self):
        """
        Sets response to an item as if one has been done and submitted
        Create a get request to toggle with the item's id added to the end
        Confirms redirect back to the homepage
        Get the item again
        Check the done status
        """
        item = Item.objects.create(name='Test Todo Item', done=True)
        response = self.client.get(f'/toggle/{item.id}')
        self.assertRedirects(response, '/')
        updated_item = Item.objects.get(id=item.id)
        self.assertFalse(updated_item.done)

    
    def test_can_edit_item(self):
        item = Item.objects.create(name='Test Todo Item')
        response = self.client.post(f'/edit/{item.id}', {'name': 'Updated Name'})
        self.assertRedirects(response, '/')
        updated_item = Item.objects.get(id=item.id)
        self.assertEqual(updated_item.name, 'Updated Name')
