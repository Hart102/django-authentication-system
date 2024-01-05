from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.http import HttpResponse

# Create your views here.

#==========User Registration Endpoint==========
def user_registration (request):

    users = CustomUser.objects.all()
    if request.user.is_authenticated:
        return redirect("profile", pk = request.user.id)

    message = ""
    form = RegistrationForm()

    if request.method == "POST":
        email = request.POST.get("email")

        try:
            emailExists = CustomUser.objects.get(email = email)
            message = "Email already exist. Please use a new email"
        
        except CustomUser.DoesNotExist:
            # ===========Create user===========
            user = CustomUser(
                firstname = request.POST.get("firstname"),
                lastname = request.POST.get("lastname"),
                email = request.POST.get("email"),
                phone = request.POST.get("phone"),
            )

            user.set_password(request.POST.get("password"))
            user.save()
            login(request, user)
            return redirect("profile", pk = request.user.id)

        except IntegrityError as e:
            message = "Something went wrong please try again"

    context = {"form": form, "message": message, "users": users}
    return render(request, "base/login_register.html", context)




#=========User Login Endpoint=========
def user_login (request):
    page = "login"
    message = ""

    if request.user.is_authenticated:
        return redirect("profile", pk = request.user.id)

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(email = email)
        except:
            message = "Invalid email or password"

        user = authenticate(request, email = email, password = password)

        if user is not None:
            login(request, user)
            return redirect("profile", pk = request.user.id)

        else:
            message = "User does not exist"
        # CustomUser.objects.all().delete()

    context = {"page": page, "message": message}
    return render(request, "base/login_register.html", context)




#=========User Logout Endpoint=========
def user_logout (request):
    logout(request)
    return redirect("login")




#=========User Profile Endpoint=========
def user_profile (request, pk):
    user = CustomUser.objects.get(id = pk)

    if not request.user.is_authenticated:
        return redirect("login")
        
    context = {"user": user}
    return render(request, "base/user_profile.html", context)




#=======User update Profile Endpoint=======
def user_update_profile (request, pk):
    user = CustomUser.objects.get(id = pk)
    form = RegistrationForm(instance = user)
    page = "update"

    print(form)

    if not request.user.is_authenticated:
        return HttpResponse("You are not allowed here")
        

    if request.method == "POST":
        user.firstname = request.POST.get("firstname").lower()
        user.lastname = request.POST.get("lastname").lower()
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")

        user.save()
        return redirect("profile", pk = request.user.id)

    context = {"form": form, "user": user, "page": page}
    return render(request, "base/login_register.html", context)




#==========Display modal endpoint==========
def display_modal (request):
    user = request.user
    return render(request, "base/modal.html", {"user": user})



#==========Delete account endpoint==========
def delete_account (request, pk):
    user = CustomUser.objects.get(id = pk)
    user.delete()
    return render(request, "base/delete.html")