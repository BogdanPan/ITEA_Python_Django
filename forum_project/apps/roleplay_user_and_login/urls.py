from .views import signup, CabinetView, InventoryView
from django.urls import path, include
urlpatterns = [
	path('', include('django.contrib.auth.urls')),
	path('signup/', signup),
	path('cabinet/', CabinetView.as_view()),
	path('inventory/<int:pk>', InventoryView.as_view()),
]
