from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('news/', views.news_view, name='news'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),  # Updated to match the function name
]





