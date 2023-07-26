from django.urls import path
from .views import TaskListView, TaskDetailView,CategoryListView,CategoryDetailView

urlpatterns = [
   
    path('', TaskListView.as_view(), name= 'task_list'),
    path('<int:pk>/',TaskDetailView.as_view(), name= 'task_detail'),
    path('post/', CategoryListView.as_view(), name= 'Category_list'),
    path('post/<int:pk>/',CategoryDetailView.as_view(), name= 'Category_detail')

]