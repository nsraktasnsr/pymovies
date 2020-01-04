from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
# Create your views here.


def loginUser(request):

    form = LoginForm(request.POST or None)

    context = {
        'form': form
    }
    # form true olarak geldiyse
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, 'Kullanici adi veya parola hatali!')
            return render(request, 'user/login.html', context)

        messages.success(request, 'Basariyla giris yaptiniz!')
        login(request, user)

        return redirect('index')

    # eger form post olarak donmezse yani false olarak donerse
    return render(request, 'user/login.html', context)


def register(request):

    form = RegisterForm(request.POST or None)
    # form post olarak donerse
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        newUser = User(username=username,email=email)
        newUser.set_password(password)
        # yeni bir kullanici olusturduk

        newUser.save()
        login(request, newUser)
        # yeni kullaniciyla giris yaptik

        messages.success(request, "Basariyla kayit oldunuz.")

        return redirect("index")
    else:
        # eger register get olarak donerse
        context = {
            "form": form
        }
        return render(request, "user/register.html", context)


def logoutUser(request):
    logout(request)
    messages.success(request, "Basariyla Cikis Yaptiniz.")
    return redirect('index')
