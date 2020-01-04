from django.urls import path
from . import views


urlpatterns = [
  path('', views.index, name="movies"),
    path('<int:movie_id>', views.detail, name="detail"),
    path('category/',views.category, name='category'),
    path('imdb/', views.imdb, name = 'imdb'),
    path('older/', views.older, name='older'),
    path('search', views.search, name="search"),
    # movie detail sayfasinda bulunan comment formun yonlendirilecegi fonksiyonun yolu.
    path('addComment/', views.addComment, name='addComment'),
    path('delComment/', views.delComment, name='delComment'),

]
