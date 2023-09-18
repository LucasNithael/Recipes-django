from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name='search'),
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path('recipes/category/<int:category_id>/', views.RecipeListViewCategory.as_view(), name='category'),  # noqa: E501
    path('recipes/<int:pk>/', views.RecipeDetail.as_view(), name='recipe'),
]
