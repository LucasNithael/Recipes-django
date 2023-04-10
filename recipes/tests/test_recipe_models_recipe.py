from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipes_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug-no-defaults',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
        # Esse parameterized cria os campos que devemos testar
        # com os tamanhos dos seus length e permite usarmos ele
        # como um for. E também ele indica qual teste dos testes 
        # passados como paramêtro falhou
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

        '''
            - setattr atribui valores aos campos do parameterized
              de forma dinâmica, pois cada campo será mudado, então
              não daria para fazer 'self.recipe.title = "A" * 66
              pois o title seria um atributo estático

            - full_clean e assertRaises estão explicados nos testes
              categoria
        '''

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='Recipe preparation_steps_is_html is not False',
        )
        '''
            - testa o valor padrão AssertFalse verifica se o valor
            do campo preparation_steps_is_html é false, que é seu valor
            padrão definido no model
        '''

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.is_published,
            msg='Recipe is_published is not False',
        )

    def test_recipe_string_representation(self):
        needed = 'Testing Representation'
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe), needed,
            msg=f'Recipe string representation must be '
                f'"{needed}" but "{str(self.recipe)}" was received.'
        )
        '''
            - Testa se o representão do método __str__ é igual ao  # noqa: E501
            título definido no objeto
        '''