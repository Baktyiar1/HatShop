from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.CapIndexViews.as_view()),
    path('index/create/', views.CapCreateAPIView.as_view()),
    path('index/<int:pk>/', views.CapDetailViews.as_view()),
    path('list/', views.CapListAPIView.as_view()),
    path('index/brand/', views.BrandListView.as_view()),
    path('index/bestseller/', views.Bestsellers_capsListView.as_view()),
    path('index/special/', views.Special_capsListView.as_view()),
    path('cart/', views.CartCreateView.as_view()),

]
