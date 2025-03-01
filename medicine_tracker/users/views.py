from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from .models import UserProfile


def register(request):
    """
    Handles user registration and profile creation.
    This view processes the user registration form. If the request method is POST
    and the form is valid, a new user is created with a hashed password, a user
    profile is generated, and the user is automatically logged in. After successful
    registration, the user is redirected to their profile page.
    Args:
        request (HttpRequest): The request object.
    Returns:
        HttpResponse:
            - Redirects to 'profile' after successful registration.
            - Renders the 'register.html' template with the registration form if
              the request method is GET or the form is invalid.
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """
    Handles user authentication and login.
    This view processes the login form. If the request method is POST and
    the form is valid, the user is authenticated and logged in. After
    successful login, the user is redirected to the 'medicine_list' page.
    Args:
        request (HttpRequest): The request object.
    Returns:
        HttpResponse:
            - Redirects to 'medicine_list' after successful login.
            - Renders the 'login.html' template with the authentication form
              if the request method is GET or the form is invalid.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('medicine_list')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    """
    Logs out the currently authenticated user and redirects to the login page.
    This view calls Django's `logout()` function to terminate the user's session
    and then redirects them to the login page.
     Args:
        request (HttpRequest): The request object.
     Returns:
        HttpResponseRedirect: Redirects the user to the 'login' page.
    """
    logout(request)
    return redirect('login')


def profile(request):
    """
    Displays the user's profile page.
    This view renders the profile template for the logged-in user.
    Args:
        request (HttpRequest): The request object.
    Returns:
        HttpResponse: Renders the 'profile.html' template.
    """
    return render(request, 'users/profile.html')
