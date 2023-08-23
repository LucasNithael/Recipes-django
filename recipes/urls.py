from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('recipes/search/', views.search, name='search'),
    path('', views.home, name='home'),
    path('recipes/category/<int:category_id>/', views.category, name='category'),  # noqa: E501
    path('recipes/<int:id>/', views.recipe, name='recipe'),
    path('recipes/save/', views.recipe_save, name='recipe_save'),

]
