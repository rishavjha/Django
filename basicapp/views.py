from django.shortcuts import render
from basicapp.forms import UserForm,UserProfileInfoForm
# Create your views here.
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse

from django.contrib.auth.decorators import login_required






def index(request):
    return render(request,'basicapp/index.html')

@login_required
def special(request):
    return HttpResponse("you are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered=False

    if request.method=="POST":
        userform=UserForm(data=request.POST)
        profileform=UserProfileInfoForm(data=request.POST)

        if userform.is_valid() and profileform .is_valid():
            user=userform.save()
            user.set_password(user.password)
            # password to hash table
            user.save()
            profile=profileform.save(commit=False)
            profile.user=user
            # provide one to one relationship so no collision


            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()

            registered=True
        else:
            print(userform.errors,profileform.errors)


    else:
        userform=UserForm()
        profileform=UserProfileInfoForm()



    return render(request,'basicapp/registration.html',{'userform':userform,'profileform':profileform,'registered':registered})



def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'basicapp/login.html', {})
