# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import *
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

            SendMailToAdmin(medicine)
            return redirect('dashboard')
        
    else:
        form=MedicineForm()


    return render(request,"medicine.html",{'form':form})


def SendMailToAdmin(medicine):
    subject = 'New Medicine Submission'
    message = f'A new medicine has been submitted:\n\n'
    message += f'Medicine Name: {medicine.name}\n'
    message += f'Dosage: {medicine.dosage}\n'
    # Add other fields as needed

    from_email = 'anitajustin007@gmail.com'
    admin_email = 'anitajustinc@gmail.com'  # Replace with the actual admin email
    send_mail(subject, message, from_email, [admin_email], fail_silently=False)