from django.urls import path, include
from . import views 
from .views import DepositMoneyView
urlpatterns = [
     path('details/<int:id>', views.DetailBookView.as_view(), name='detail_book'),
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
path('return_book/<int:transaction_id>/', views.return_book, name='return_book'),

]