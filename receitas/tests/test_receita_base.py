import os
import tempfile

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from receitas.models import Category, Receita


class RecipeMixin:
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(self, first_name='user',
                    last_name='name',
                    username='username',
                    password='123456',
                    email='username@email.com',):
        return User.objects.create_user(first_name=first_name,
                                        last_name=last_name,
                                        username=username,
                                        password=password,
                                        email=email,)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def make_receita(self, category_data=None,
                     author_data=None,
                     title='Recipe Title',
                     description='Recipe Description',
                     slug='recipe-slug',
                     preparation_time_unit='10 Minutes',
                     servings_unit='5 Servings',
                     preparation_steps='Recipe Preparation Steps',
                     preparation_steps_is_html=False,
                     is_published=True,
                     cover=None):
        image_path = os.path.join(
            settings.BASE_DIR,
            'media', 'receitas', 'covers', '2022', '06', '22', 'test_img.png')

        with open(image_path, 'rb') as f:
            image_content = f.read()

        self.image = SimpleUploadedFile(
            name='test_img.png',
            content=image_content,
            content_type='image/png'
        )
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        if cover is None:
            cover = self.image

        return Receita.objects.create(category=self.make_category(**category_data),  # noqa:E501
                                      author=self.make_author(**author_data),
                                      title=title,
                                      description=description,
                                      slug=slug,
                                      preparation_time_unit=preparation_time_unit,  # noqa:E501
                                      servings_unit=servings_unit,
                                      preparation_steps=preparation_steps,
                                      preparation_steps_is_html=preparation_steps_is_html,  # noqa:E501
                                      is_published=is_published,
                                      cover=cover,)

    def make_recipe_in_batch(self, qtd=10):
        receitas = []
        for i in range(qtd):
            kwargs = {'title': f'Recipe Title {i}', 'slug': f'r{i}',
                      'author_data': {'username': f'u{i}'}}
            receita = self.make_receita(**kwargs)
            receitas.append(receita)
        return receitas


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class ReceitaTestBase(TestCase, RecipeMixin):

    def setUp(self) -> None:
        return super().setUp()
