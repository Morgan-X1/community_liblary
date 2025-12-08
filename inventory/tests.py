from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Item, Category

User = get_user_model()

@override_settings(STORAGES={
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
})
class DeleteItemTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.category = Category.objects.create(name='Test Category', description='Test Description')
        self.item = Item.objects.create(
            name='Test Item',
            description='Test Description',
            category=self.category,
            owner=self.user,
            status='AVAILABLE'
        )

    def test_delete_item_success(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('delete_item', args=[self.item.id]))
        self.assertRedirects(response, reverse('my_items'))
        self.assertFalse(Item.objects.filter(id=self.item.id).exists())

    def test_delete_item_other_user(self):
        self.client.login(username='otheruser', password='password')
        response = self.client.post(reverse('delete_item', args=[self.item.id]))
        # Should return 404 because of get_object_or_404(Item, pk=item_id, owner=request.user)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Item.objects.filter(id=self.item.id).exists())

    def test_delete_item_get_request(self):
        # GET request should not delete, just redirect
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('delete_item', args=[self.item.id]))
        self.assertRedirects(response, reverse('my_items'))
        self.assertTrue(Item.objects.filter(id=self.item.id).exists())
