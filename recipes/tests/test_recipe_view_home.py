from django.urls import resolve, reverse
from unittest.mock import patch
from recipes import views

from .test_recipes_base import RecipeTestBase


class RecipeHomeViewsTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)
        '''
            - resolve nos dar os dados que a url tem, dentre
            esses dados a função que a aquela url leva

            - reserve nos retorna o caminho completo da url que
            pedimos para gerar, no caso desse teste é retornado
            apenas '/'

            - assertIs verifica se os parâmetros tem os mesmo
            endereços de memória
        '''

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        '''
            - o django prover um cliente para realização de testes
            então podemos simular um requisição de um cliente e pegarmos
            o response gerado

            - dentre os varios dados que a response traz,tem o status code
            da requisição, isso permite realizar nossos testes
        '''

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')
        '''
            - na response podemos saber qual template foi utilizado
            na renderilização
        '''

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found here</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)
        '''
            - aqui criamos um template, então quando o cliente acessa
            a url será mostrado na renderilização apenas um template

        '''

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found here</h1>',
            response.content.decode('utf-8')
        )
        '''
            - na view definimos exibir os recipes apenas que estiverem
            com o campo is_published igual a true, caso não seja carregada
            nenhuam recipe no template é mostrada a mensagem "No recipes 
            found here"

            - response.content.decode: 
                - content: acessa todo conteúdo do html renderizado
                - decode: converte o conteúdo do contente em string
        '''

    def test_recipe_home_is_paginated(self):
        for i in range(8):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)

    def test_invalid_page_query_uses_page_one(self):
        url = reverse('recipes:home') + '?page=1A'
        response = self.client.get(url)
        self.assertEqual(response.context['recipes'].number, 1)