import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from .form import MyUserCreationForm, UserUpdateForm, UpdateImage
from django.http import HttpResponse
from django.db import IntegrityError


#==========User Registration Endpoint==========
def user_registration (request):
    form = MyUserCreationForm()
    message = ""

    if request.user.is_authenticated:
        return redirect("profile", pk = request.user.id)

    if request.method == "POST":
        # try:
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.firstname = request.POST.get("firstname").lower()
            user.lastname = request.POST.get("lastname").lower()
            user.save()
            login(request, user)
            return redirect("profile", pk = request.user.id)

            # else:
                # print("Not a valid user")
        # except:
        #     print("something went wrong")
       


            

    context = { "form": form, "message": message }
    return render(request, "base/login_register.html", context)




#=========User Login Endpoint=========
def user_login (request):
    page = "login"
    message = ""

    # if request.user.is_authenticated:
    #     return redirect("profile", pk = request.user.id)

    # if request.method == "POST":
    #     email = request.POST.get("email")
    #     password = request.POST.get("password")

    #     try:
    #         user = User.objects.get(email = email)
    #     except:
    #         message = "Invalid email or password"

    #     user = authenticate(request, email = email, password = password)

    #     if user is not None:
    #         login(request, user)
    #         return redirect("profile", pk = request.user.id)

    #     else:
    #         message = "User does not exist"
        # User.objects.all().delete()

    context = {"page": page, "message": message}
    return render(request, "base/login_register.html", context)




#=========User Logout Endpoint=========
def user_logout (request):
    logout(request)
    return redirect("login")




#=========User Profile Endpoint=========
def user_profile (request, pk):
    user = User.objects.get(id = pk)

    if not request.user.is_authenticated:
        return redirect("login")
        
    context = {"user": user}
    return render(request, "base/user_profile.html", context)




#=======User update Profile Endpoint=======
def user_update_profile (request, pk):
    user = User.objects.get(id = pk)
    form = UserUpdateForm(instance=user)
    message = ""

    # if request.method == "POST":
    #     form = UserUpdateForm(request.POST, instance=user)

    #     if form.is_valid():
    #         form.save()
    #         return redirect("profile", pk = request.user.id)
    #     else:
    #         message = "Something went wrong please try again"

    context = { "form": form, "user": user }
    return render(request, "base/login_register.html", context)



#======Update profile Image Endpoint======
def update_profile_image (request):
    user = request.user
    form = UpdateImage(instance=user)

    # Get previous Image
    # image_path = user.avatar.path

    # if request.method == "POST":
    #     form = UpdateImage(request.POST, request.FILES, instance=user)
        
    #     if "avatar.svg" in image_path:
    #         pass
    #     else:
    #         if os.path.exists(image_path):
    #             os.remove(image_path) #Delete Image

    #     print(image_path)
    #     if form.is_valid():
    #         form.save()
        
    context = {"form": form}
    return render(request, "base/user_profile.html", context)


#==========Display modal endpoint==========
def display_modal (request):
    user = request.user
    return render(request, "base/modal.html", {"user": user})



#==========Delete account endpoint==========
def delete_account (request, pk):
    user = User.objects.get(id = pk)
    user.delete()
    return render(request, "base/delete.html")




# form = MyUserCreationForm(request.POST)
        
# except:
#     print("something went wrong")

# try:
#     if form.is_valid():
#         user = form.save(commit=False)

#         user.firstname = user.firstname.lower()
#         user.lastname = user.lastname.lower()
#         user.save()
#         login(request, user)
#         return redirect("profile", pk = request.user.id)
#     else:
#         message = "Password mismatched or too short."

# except IntegrityError as e:
#     # print(f"IntegrityError: {e}")
#     message = "Email already exist. Please try another email."