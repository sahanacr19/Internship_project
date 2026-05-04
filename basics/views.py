from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import pickle
import pandas as pd
import os



# Create your views here.
def index(request):
    return render(request,  "index.html")

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        if pass1!=pass2:
            return HttpResponse("Your password and confirm password are not same!!")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render(request,"signup.html")

def LoginPage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=User.objects.filter(username=username)
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            result="Password Entered is wrong"
            return HttpResponse("Username or Password is Incorrect!!")
    return render(request,'login.html')


def logoutUser(request):
    logout(request)
    return redirect("/login/")

def introvert_extrovert_predict(request):

    if request.method == "POST":

        import numpy as np
        import pickle

        model = pickle.load(open("personality_model.pkl","rb"))

        data = request.POST

        values = [

        float(data.get("social_energy")),
        float(data.get("alone_time_preference")),
        float(data.get("talkativeness")),
        float(data.get("deep_reflection")),
        float(data.get("group_comfort")),
        float(data.get("party_liking")),
        float(data.get("listening_skill")),
        float(data.get("creativity")),
        float(data.get("organization")),
        float(data.get("leadership")),
        float(data.get("risk_taking")),
        float(data.get("public_speaking_comfort")),
        float(data.get("curiosity")),
        float(data.get("routine_preference")),
        float(data.get("excitement_seeking")),
        float(data.get("friendliness")),
        float(data.get("emotional_stability")),
        float(data.get("planning")),
        float(data.get("spontaneity")),
        float(data.get("adventurousness")),
        float(data.get("reading_habit")),
        float(data.get("sports_interest")),
        float(data.get("online_social_usage")),
        float(data.get("travel_desire")),
        float(data.get("gadget_usage")),
        float(data.get("work_style_collaborative")),
        float(data.get("decision_speed")),
        float(data.get("stress_handling"))

        ]

        prediction = model.predict([values])

        if prediction[0] == 0:
            result = "Extrovert"
        else:
            result = "Introvert"

        return render(request,'introvert_vs_extrovert.html',{"result":result})

    return render(request,'introvert_vs_extrovert.html')



model = pickle.load(open('job_role_model.pkl','rb'))

def predict_job(request):

    if request.method == "POST":

        import pickle

        model = pickle.load(open("job_role_model.pkl","rb"))

        data = request.POST

        age = float(data.get("age"))
        gender = float(data.get("gender"))
        degree = float(data.get("degree"))
        field = float(data.get("field"))
        experience = float(data.get("experience"))
        certifications = float(data.get("certifications"))
        skills = float(data.get("skills"))
        location = float(data.get("location"))
        projects = float(data.get("projects"))

        values = [[
            age,
            gender,
            degree,
            field,
            experience,
            certifications,
            skills,
            location,
            projects
        ]]

        prediction = model.predict(values)

        job_roles = {
            0: "Software Developer",
            1: "Data Scientist",
            2: "AI Engineer",
            3: "Business Analyst",
            4: "Network Engineer",
            5: "Teacher"
        }

        result = job_roles[prediction[0]]

        return render(request,'job_role.html',{"prediction":result})

    return render(request,'job_role.html')