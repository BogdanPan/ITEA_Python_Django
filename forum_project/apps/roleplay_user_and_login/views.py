from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView, DetailView, RedirectView, CreateView, FormView
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from .models import Inventory, Item
from ..core.models import Comment
from .forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


# def signup(request):
#    if request.method == 'POST':
#        form = UserCreationForm(request.POST)
#        if form.is_valid():
#            form.save()
#            username = form.cleaned_data.get('username')
#            raw_password = form.cleaned_data.get('password1')
#            user = authenticate(username=username, password=raw_password)
#            login(request, user)
#            return redirect('index')
#    else:
#        form = UserCreationForm()
#    return render(request, 'roleplay_user_and_login/signup.html', {'form': form})
class RegistrationView(FormView):
    template_name = 'roleplay_user_and_login/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('core:index')
    def form_valid(self, form):
        user = form.save()
        user.send_user_mail('Registration', 'Welcome!')
        login(self.request, user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return JsonResponse(form.errors)


class LoginView(FormView):
    template_name = 'roleplay_user_and_login/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

class LogoutView(RedirectView):
    pattern_name = 'core:index'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)

class CabinetView(TemplateView):
    template_name = 'roleplay_user_and_login/cabinet.html'

    def get_context_data(self, **kwargs):
        n_of_comments = Comment.objects.filter(user=self.request.user).count()
        ctx = {
            'inventory': Inventory.get_user_inventorys(self.request.user), 
            'number_of_comments': n_of_comments
        }
        return ctx

class InventoryView(CreateView):
    template_name = 'roleplay_user_and_login/inventory.html'
    model = Inventory
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        inv = Inventory.objects.filter(id=self.get_object().pk).first()
        ctx = {'items': Item.get_inventory_items(inv)}
        return ctx
