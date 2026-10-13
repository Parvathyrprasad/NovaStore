
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Product, Banner


def home(request):
    banners = Banner.objects.filter(is_active=True).order_by("-created_at")
    products = Product.objects.select_related("category").order_by("-created_at")

    return render(
        request,
        "store/home.html",
        {"banners": banners, "products": products},
    )


def product_detail(request, product_id):
    product = get_object_or_404(
        Product.objects.select_related("category"),
        id=product_id
    )
    return render(
        request,
        "store/product_detail.html",
        {"product": product}
    )


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created successfully!")
            return redirect("account")
    else:
        form = UserCreationForm()

    return render(request, "store/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("account")
    else:
        form = AuthenticationForm(request)

    return render(request, "store/login.html", {"form": form})


def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
    return redirect("account")


@login_required
def account(request):
    return render(request, "store/account.html")
