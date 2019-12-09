from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView, DetailView, RedirectView, CreateView, FormView
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from .models import Inventory, Item, MyUser
from ..core.models import Comment
from .forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .tokens import account_activation_token
from django.http import HttpResponse  
from django.shortcuts import render  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin

class RegistrationView(FormView):
    template_name = 'roleplay_user_and_login/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('core:index')
    def form_valid(self, form):
        print('form is valid')
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        print('user saved')
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string(
            'roleplay_user_and_login/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            }
        )
        user.send_user_mail(mail_subject, message)
        return render(self.request, 'roleplay_user_and_login/confirm_email.html')


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


class CabinetView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
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

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('core:index')
    else:
        return render(request, 'roleplay_user_and_login/invalid_link.html')
