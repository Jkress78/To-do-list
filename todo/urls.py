from django.urls import path

from . import views

app_name = "todo"
urlpatterns = [
    path("dashboard/", views.listSelect, name="listSelect"),
    path("add/", views.listCreate, name="listCreate"),
    path("addItem/", views.createItem, name="createItem"),
    path("view/", views.listDetails, name="listDetails"),
    path("profile/", views.userDetails, name="userDetails"),
    path("update/<int:item_id>/", views.updateItem, name="updateItem"),
    path("deleteItem/<int:item_id>/", views.deleteItem, name="deleteItem"),
    path("deleteList/<int:list_id>/", views.deleteList, name="deleteList"),
    path("dashboard/<int:list_id>/edit/", views.editList, name="editList"),
    
]
