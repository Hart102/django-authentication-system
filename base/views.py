import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from .form import MyUserCreationForm, UserUpdateForm, UpdateImage
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password


#==========USER REGISTRATION ENDPOINT==========
def user_registration(request):
    form = MyUserCreationForm()
    message = ""

    if request.user.is_authenticated:
        return redirect("profile", pk=request.user.id)

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email'] # ASSIGN EMAIL TO USER NAME
            user.firstname = request.POST.get("firstname").lower()
            user.lastname = request.POST.get("lastname").lower()
            user.save()
            login(request, user)
            return redirect("profile", pk=request.user.id)
        else:
            message = "Email already exist."

    context = {"form": form, "message": message}
    return render(request, "base/login_register.html", context)


#=========USER LOGIN ENDPOINT=========
def user_login (request):
    if request.user.is_authenticated:
        return redirect("profile", pk = request.user.id)
        
    page = "login"
    message = ""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            # COMPARE USER PASSWORD
            if not check_password(password, user.password):
                message = "Incorrect Email Or Password"
            else:
                login(request, user)
                return redirect("profile", pk = request.user.id)

        except:
            message = "User does not exist!"

    context = {"page": page, "message": message}
    return render(request, "base/login_register.html", context)


#=========USER LOGOUT ENDPOINT=========
def user_logout (request):
    logout(request)
    return redirect("login")


#=========USER PROFILE ENDPOINT=========
def user_profile (request, pk):
    user = User.objects.get(id = pk)

    if not request.user.is_authenticated:
        return redirect("login")
        
    context = {"user": user}
    return render(request, "base/user_profile.html", context)


#=======PROFILE UPDATE ENDPOINT=======
def user_update_profile (request, pk):
    user = User.objects.get(id = pk)
    form = UserUpdateForm(instance=user)
    message = ""

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile", pk = request.user.id)
        else:
            message = "Something went wrong while updating profile. Please try again!"

    context = { "form": form, "user": user }
    return render(request, "base/login_register.html", context)


#======IMAGE UPDATE ENDPOINT======
def update_profile_image (request):
    user = request.user
    form = UpdateImage(instance=user)

    # GET PREVIOUS IMAGE PATH
    image_path = user.avatar.path

    if request.method == "POST":
        form = UpdateImage(request.POST, request.FILES, instance=user)
        # GET THE INDEX OF THE LAST "/" IN THE FROM THE IMAGE PATH
        indexOfTheLastWord = image_path.rfind("/") 

        if indexOfTheLastWord != -1:
            # USE THE INDEX TO GET THE LAST WORLD IN THE STRING (WHICH IS THE IMAGE NAME)
            image_name = image_path[indexOfTheLastWord + len("/"):]

            if form.is_valid():
                if image_name == "avatar.svg": # PREVENT DELETING OF DEFAULT IMAGE
                    form.save()
                elif image_name != "avatar.svg":
                    if os.path.exists(image_path):
                        os.remove(image_path) #Delete Image
            
                form.save()


        # uploadedFile = request.FILES["avatar"]
        # file_name = uploadedFile.name

        # if image_path.find("avatar.svg") != -1:
        #     print("Yes, 'avatar.svg' is present in the image path.")
        # else:
        #     print("No, 'avatar.svg' is not present in the image path.")


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

