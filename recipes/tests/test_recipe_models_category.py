from django.core.exceptions import ValidationError

from .test_recipes_base import RecipeTestBase


class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category Testing'
        )
        return super().setUp()

    def test_recipe_category_model_string_representarion_is_name_field(self):
        self.assertEqual(
            str(self.category),
            self.category.name
        )
        '''
            Aqui testa se o método __str__ do model Category é igual
            ao campo name
        '''

    def test_recipe_category_model_name_max_length_is_65_chars(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
        '''
            - testa se o campo name de Category levanta erro se
            ultrapassar os 65 caracteres

            - save() ele salva os dados com mais caracteres que
            o determinado pelo campo sem levantar error, mas o
            método full_clean() ele salva os dados e levanta error
            se a quantidade de caracteres forem maior que determinada
        
            - self.assertRaises(ValidationError) afirma que o código
            abaixo levanta um error validation error
        '''
