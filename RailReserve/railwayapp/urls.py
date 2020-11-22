from django.urls import path
from rest_framework.authtoken import views as authviews
from . import views

app_name = 'railwayapp'

urlpatterns = [
    path('api/login/', authviews.obtain_auth_token, name='api-login'),
    path('api/register/', views.RegisterView.as_view(), name='api-register'),
    path('api/get_route/<str:train_name>/', views.TrainRouteView.as_view(), name='api-route'),
    path('api/search/', views.GeneralSearchView.as_view(), name='api-search'),
    path('api/history/', views.TicketHistoryView.as_view(), name='api-history'),
    path('api/buy/', views.buy_ticket, name='api-buy'),

    path('search/', views.GeneralSearch.as_view(), name='search'),
    path('', views.mainpage, name='mainpage'),
    path('logout/', views.logoutpage, name='logout'),
    path('login/', views.loginpage, name='login'),
    path('register/', views.registerpage, name='register'),
    path('schedule/', views.TrainRoute.as_view(), name='schedulepage'),
    path('history/', views.historypage, name='history'),
]