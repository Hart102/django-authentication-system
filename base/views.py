from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.http import HttpResponse
from .form import PhotoForm

# Create your views here.

#==========User Registration Endpoint==========
def user_registration (request):
    message = ""

    if request.user.is_authenticated:
        return redirect("profile", pk = request.user.id)

    if request.method == "POST":
        email = request.POST.get("email")

        try:
            emailExists = CustomUser.objects.get(email = email)
            message = "Email already exist. Please use a new email"
        
        except CustomUser.DoesNotExist:
          firstname = request.POST.get("firstname")
          lastname = request.POST.get("lastname")
          email = request.POST.get("email")
          phone = request.POST.get("phone")
          password = request.POST.get("password")

          if not firstname or not lastname or not email or not phone or not password:
            message = "No input field is allowed to be empty"

          else:
            # ===========Create user===========
            user = CustomUser(
                firstname = firstname,
                lastname = lastname,
                email = email,
                phone = phone,
            )
            user.set_password(password)

            user.save()
            login(request, user)
            return redirect("profile", pk = request.user.id)

        except IntegrityError as e:
            message = "Something went wrong please try again"

    context = {"message": message}
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

    print(user)

    # form = PhotoForm()
    # print(form)

    if not request.user.is_authenticated:
        return redirect("login")
        
    context = {"user": user}
    return render(request, "base/user_profile.html", context)



def update_profile_image (request, pk):
    user = CustomUser.objects.get(id = pk)
    
    if request.method == "POST":
        user.image = request.FILES
        user.caption = "new image"
        print(request.FILES)


        user.save()
    return render(request, "base/profile.html")



#=======User update Profile Endpoint=======
def user_update_profile (request, pk):
    user = CustomUser.objects.get(id = pk)

    if not request.user.is_authenticated:
        return HttpResponse("You are not allowed here")

    if not firstname or not lastname or not email or not phone or not password:
        message = "No input field is allowed to be empty"

    if request.method == "POST":
        user.firstname = request.POST.get("firstname").lower()
        user.lastname = request.POST.get("lastname").lower()
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")
        # user.image = request.FILES

        # print(request.FILES)/

        user.save()

        print(user)
        return redirect("profile", pk = request.user.id)

    context = {"user": user}
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