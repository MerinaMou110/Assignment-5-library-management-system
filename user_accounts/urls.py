from django.urls import path

from .views import UserRegistrationView ,UserLoginView, UserLogoutView,UserAccountUpdateView,CustomPasswordChangeView
from Library.views import TransactionReportView
urlpatterns = [
    
        path('register/', UserRegistrationView.as_view(), name='register'),
        path('login/', UserLoginView.as_view(), name='login'),
        path('logout/', UserLogoutView.as_view(), name='logout'),
        path('update_profile/', UserAccountUpdateView.as_view(), name='update_profile' ),
        path('profile/',TransactionReportView.as_view(), name='profile' ),
        path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
        
]
