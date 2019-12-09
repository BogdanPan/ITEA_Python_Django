from .views import RegistrationView, CabinetView, InventoryView, LoginView, LogoutView, activate
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


app_name = 'roleplay_user_and_login'
urlpatterns = [
	path('login/', LoginView.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('signup/', RegistrationView.as_view(), name='signup'),
	path('activate/<uidb64>/<token>/', activate, name='activate'),  
	path('reset/', auth_views.PasswordResetView.as_view(
		template_name='roleplay_user_and_login/pw_reset.html',
		success_url='done/'
	), name='reset_password'),
	path('reset/done/', TemplateView.as_view(
		template_name='roleplay_user_and_login/pw_reset_done.html'
	), name='reset_password_done'),
	path('cabinet/', CabinetView.as_view(), name='cabinet'),
	path('inventory/<int:pk>', InventoryView.as_view(), name='inventory'),
	path('', include('django.contrib.auth.urls'))
]
