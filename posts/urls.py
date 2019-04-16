from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('create/', views.create, name="create"),
    path('', views.list, name="list"),
    path('<int:id>/delete/', views.delete, name="delete"),
    path('<int:id>/update/', views.update, name="update"),
    path('<int:id>/like/', views.like, name="like"),
    path('<int:post_id>/create/comment/', views.create_comment, name="create_comment"),
    path('<int:post_id>/delete/comment/<int:comment_id>/', views.delete_comment, name="delete_comment"),
]