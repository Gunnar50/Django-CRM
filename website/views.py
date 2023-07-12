from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


def home(request):
    records = Record.objects.all()
    
    # Check to see if loggin in
    if request.method == "POST":
        username = request.POST["username"]  # name="username"
        password = request.POST["password"]
        
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect("home")
        else:
            messages.error(request, "There was an error loggin in, please try again.")
            return redirect("home")
            
    else:
        return render(request, "home.html", {"records":records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # authenticate and login
            username = form.cleaned_data["username"]  # whatever the user type in the form for username
            password = form.cleaned_data["password1"]  # whatever the user type in the form for password
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully registered and logged in")
                return redirect("home")
    else:
        form = SignUpForm()
        return render(request, "register.html", {"form": form})
    
    return render(request, "register.html", {"form": form})
    
    
def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, "record.html", {"customer_record": customer_record})
    
    else:
        messages.success(request, "You must be logged in")
        return redirect("home")
        
        
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete = Record.objects.get(id=pk)
        delete.delete()
        messages.success(request, "Record deleted successfully")
        return redirect("home")
    else:
        messages.success(request, "You must be logged in")
        return redirect("home")

def add_record(request):
    if request.user.is_authenticated:
        form = AddRecordForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "You have successfully added a new record!")
                return redirect("home")
        return render(request, "add.html", {"form": form})
        
    else:
        messages.success(request, "You must be logged in")
        return redirect("home")
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated successfully")
            return redirect("home")
        return render(request, "update.html", {"form": form})
    else:
        messages.success(request, "You must be logged in")
        return redirect("home")
    
    
