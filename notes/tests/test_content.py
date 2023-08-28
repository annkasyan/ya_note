from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.another_author = User.objects.create(username='Другой автор')
        cls.note = Note.objects.create(
            title='example',
            author=cls.author
        )
        cls.another_note = Note.objects.create(
            title='example_two',
            author=cls.another_author
        )

    def test_authorized_client_has_form(self):
        self.client.force_login(self.author)
        url_add = reverse('notes:add')
        url_edit = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.get(url_add)
        self.assertIn('form', response.context)
        response = self.client.get(url_edit)
        self.assertIn('form', response.context)

    def test_note_in_object_list(self):
        self.client.force_login(self.author)
        url = reverse('notes:list')
        response = self.client.get(url)
        self.assertIn(self.note, response.context['object_list'])
        self.assertNotIn(self.another_note, response.context['object_list'])
