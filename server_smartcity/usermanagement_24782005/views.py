from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect
from .forms import CitizenRegistrationForm


# ======================
# LOGIN
# ======================
class CustomLoginView(LoginView):
    template_name = 'usermanagement/login.html'

    def form_valid(self, form):
        messages.success(self.request, f"Selamat datang, {form.get_user().username}!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Username atau password salah.")
        return super().form_invalid(form)


# ======================
# LOGOUT
# ======================
class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, "Kamu berhasil logout.")
        return super().dispatch(request, *args, **kwargs)


# ======================
# REGISTER (Citizen only)
# ======================
class RegisterView(View):
    template_name = 'usermanagement/register.html'

    def get(self, request):
        # Kalau sudah login, redirect ke home
        if request.user.is_authenticated:
            return redirect('report_list')
        form = CitizenRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Akun berhasil dibuat! Selamat datang, {user.username}.")
            return redirect('report_list')
        return render(request, self.template_name, {'form': form})