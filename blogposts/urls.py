from django.urls import path
from . import views

app_name = 'blogposts'

urlpatterns = [
    path('create/', views.create_post, name='create'),
    path('', views.list_post, name='list'),
    path('list/<str:author>/<int:author_id>/<slug:slug>/',
         views.detail_post, name='detail'),
    path('<str:author>/<int:author_id>/',
         views.user_post_list, name='user_post_list'),
    path('update/<str:author>/<int:author_id>/<slug:slug>/',
         views.update_post, name='update'),
    path('delete/<int:author_id>/<slug:slug>/',
         views.delete_post, name='delete'),
]
