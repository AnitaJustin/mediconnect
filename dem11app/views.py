# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import *
from .models import *
from django.contrib.messages import add_message,WARNING,success,info
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

def homepage(request):
    return render(request,"homepage.html")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Check the form data for errors.
            if not form.cleaned_data['password1']:
                add_message(request, WARNING, 'Password is required.')
                return render(request, 'signup.html', {'form': form})

            # Save the user.
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Redirect the user to the login page.
            success(request, 'Account created successfully. You can now sign in.')
            return redirect('signin')
        else:
            return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                return redirect('dashboard') 
            
            else:
                info(request,'Invalid Credentials')

    else:
        form = SignInForm()

    return render(request, 'signin.html', {'form': form})


def dashboard(request):
    return render(request,"dashboard.html")

@login_required
def medicine(request):
    if request.method=='POST':
        form=MedicineForm(request.POST)
        if form.is_valid():
            medicine=form.save(commit=False)
            medicine.user=request.user
            medicine.save()

            SendMailToAdmin('New Medicine Submission',get_medicine_message(medicine))
            return redirect('dashboard')
        
    else:
        form=MedicineForm()


    return render(request,"medicine.html",{'form':form})

@login_required
def aids(request):
    if request.method=='POST':
        form=AidsForm(request.POST,request.FILES)
        if form.is_valid():
            aids=form.save(commit=False)
            aids.user=request.user
            aids.save()

            SendMailToAdmin('New Aids Submission',get_aids_message(aids))
            return redirect('dashboard')
        
    else:
        form=AidsForm()


    return render(request,"aids.html",{'form':form})


@login_required
def request_med(request):
    if request.method=='POST':
        form=Req_med_Form(request.POST,request.FILES)
        if form.is_valid():
            receiver=form.save(commit=False)
            receiver.user=request.user
            receiver.save()

            SendMailToAdmin('New request Submitted',get_req_med_message(receiver))
            return redirect('dashboard')
        
    else:
        form=Req_med_Form()
    return render(request,"req_med.html",{'form':form})

def request_aid(request):
    aids = OtherAids.objects.all()
    return render(request,"req_aids.html",{'aids':aids})

def SendMailToAdmin(subject,message):
   
    from_email = 'anitajustin007@gmail.com'
    admin_email = 'anitajustinc@gmail.com'  # Replace with the actual admin email
    send_mail(subject, message, from_email, [admin_email], fail_silently=False)

def get_aids_message(aids):
    return f'A new aids submission:\n\n' \
           f'Aids Name: {aids.name}\n' \
           

def get_medicine_message(medicine):
    return f'A new medicine has been submitted:\n\n' \
           f'Medicine Name: {medicine.name}\n' \
           f'Dosage: {medicine.dosage}\n'

def get_req_med_message(receiver):
    return f'A new request has been submitted:\n\n' \
           f'Medicine Name: {receiver.medicine}\n' \
           f'Disease: {receiver.disease}\n'


   

