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

            - save() salva os dados sem validação, dessa forma dados
            com mais caracteres do que o número definido no campo do
            model será salvo normal, nesse caso, ele salva até aonde
            dá os caracteres.

            - full_clean() ele valida os dados a serem salvos e caso
            tenha algum erro ele levanta a excetion ValidationError
        
            - self.assertRaises(ValidationError) afirma que o código
            abaixo levanta um error validation error
        '''
