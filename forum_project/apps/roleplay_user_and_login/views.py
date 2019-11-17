from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView, DetailView, RedirectView, CreateView
from .models import Inventory, Item
from .forms import UserCreationForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'roleplay_user_and_login/signup.html', {'form': form})

class CabinetView(TemplateView):
    template_name = 'roleplay_user_and_login/cabinet.html'

    def get_context_data(self, **kwargs):
        ctx = {'inventory': Inventory.get_user_inventorys(self.request.user)}
        return ctx

class InventoryView(CreateView):
    template_name = 'roleplay_user_and_login/inventory.html'
    model = Inventory
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        inv = Inventory.objects.filter(id=self.get_object().pk).first()
        ctx = {'items': Item.get_inventory_items(inv)}
        return ctx
