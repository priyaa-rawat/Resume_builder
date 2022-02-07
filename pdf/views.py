from django.shortcuts import render,redirect
from .models import profile
from .forms import NewUserForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import pdfkit

# Create your views here.


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form":form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('home')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})


def home(request):
    return render(request, "index.html")


def accept(request,id):
    user = User.objects.get(pk=id)
    if user:
        if request.method == "POST":
            name = request.POST.get("name", "")
            phone = request.POST.get("phone", "")
            email = request.POST.get("email", "")
            school = request.POST.get("school", "")
            degree = request.POST.get("degree", "")
            university = request.POST.get("university", "")
            skills = request.POST.get("skills", "")
            about_you = request.POST.get("about_you", "")
            previous_work = request.POST.get("previous_work", "")
            portfolio = request.POST.get("portfolio","")

            Profile = profile(user = user, name=name, phone=phone, email=email, school=school, degree=degree,
                      university=university, skills=skills, about_you=about_you, previous_work=previous_work, portfolio=portfolio)
            Profile.save()
            return render(request, "display.html" ,{'user_profile':Profile})
        else:
            return render(request,"accept.html")
    return redirect("login")

def download(request, id):
    user_profile = profile.objects.get(pk=id)
    template = loader.get_template("dwnld.html")
    html = template.render({"user_profile":user_profile})
    options={
        "page-size":"Letter",
        "encoding":"UTF-8"
    }
    config = pdfkit.configuration(wkhtmltopdf=r"E:\deploydjango\Lib\site-packages\wkhtmltopdf\bin\wkhtmltopdf.exe")
    pdf = pdfkit.from_string(html,False,configuration=config,options=options)
    response = HttpResponse(pdf,content_type="application/pdf")
    response["Content-Disposition"] = "attachments"
    return response


def rlist(request,id):
    user = User.objects.get(pk=id)
    resume_list = user.profile_set.all()
    return render(request,"rlist.html",{'user':user,'resume_list':resume_list})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")



