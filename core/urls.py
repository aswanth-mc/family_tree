from django.urls import path
from . import views

urlpatterns = [
    path('', views.tree_view, name='tree_canvas'),
    path('api/tree/', views.get_tree, name='api_get_tree'),
    path('api/add-relative/', views.add_relative, name='api_add_relative'),
    path('api/people/', views.create_person, name='api_create_person'),
    path('api/people/<uuid:person_id>/', views.delete_person, name='api_delete_person'),
]
