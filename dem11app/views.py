# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, SignInForm
from django.contrib.messages import add_message,WARNING,success

def homepage(request):
    return render(request,"homepage.html")
# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             success(request, 'Account created successfully. You can now sign in.')
#             return redirect('signin')
#     else:
#         form = SignUpForm()
#     return render(request, 'signup.html', {'form': form})


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

# def signin(request):
#     if request.method == 'POST':
#         form = SignInForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 if login(request, user):
#                     return redirect('dashboard')  # Redirect to your dashboard or any other page
                

    # else:
    #     form = SignInForm()
    # return render(request, 'signin.html', {'form': form})

# def signin(request):
#     if request.method == 'POST':
#         form = SignInForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             print(f"Username: {username}, Password: {password}, User: {user}")

#             if user is not None:
#                 if login(request, user):
#                     print("Login successful")
#                     return redirect('dashboard')  # Redirect to your dashboard or any other page
#                 else:
#                     print("Login function returned False")
#             else:
#                 print("Authentication failed")

#     else:
#         form = SignInForm()

#     return render(request, 'signin.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(f"Username: {username}, Password: {password}, User: {user}")

            if user is not None:
                print("User is not None, attempting login...")
                login_success = login(request, user)
                print(f"Login success: {login_success}")

                if login_success:
                    print("Login successful")
                    return redirect('dashboard') 
                else:
                    print("Login function returned False after authentication")

            else:
                print("Authentication failed")

    else:
        form = SignInForm()

    return render(request, 'signin.html', {'form': form})


def dashboard(request):
    return render(request,"dashboard.html")