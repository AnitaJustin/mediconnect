# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import *
from .models import *
from django.contrib.messages import add_message,warning,success,info,WARNING
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.apps import apps
from django.http import JsonResponse


def homepage(request):
    return render(request,"homepage.html")
def about(request):
    return render(request,"about.html")
def contact(request):
    return render(request,"contact.html")
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
        form=SignUpForm()

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

def admin_signin(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            admin_user = Admin.objects.filter(username=username,password=password).first()

            if admin_user is not None:
                return redirect('admin_dashboard') 
            
            else:
                info(request,'Invalid Credentials')

    else:
        form = AdminForm()

    return render(request, 'admin_signin.html', {'form': form})

@login_required
def dashboard(request):
    return render(request,"dashboard.html")

@login_required
def admin_dashboard(request):
    
    donated_meds=medicines.objects.filter(removed="False")
    donated_aids=OtherAids.objects.filter(removed="False")
    request_med=req_med.objects.filter(removed="False")
    req_aids=saving_request.objects.filter(removed="False")

    return render(request,"admin_dashboard.html",{'donated_meds':donated_meds,'donated_aids':donated_aids,'req_med':request_med,'req_aids':req_aids})

@login_required
def approve(request):
    if request.method=='GET':
        id=request.GET.get('id')
        table=request.GET.get('table')
        model = apps.get_model(app_label='dem11app', model_name=table)
        obj=model.objects.filter(id=id).first()
        obj.approved="True"
        obj.save()  
        if table=="req_med":
            user_mail=obj.user.email
            from_email = 'mediconnect007@gmail.com'
            send_mail("Request from Mediconnect",f"We are happy to help you.\nWe have accepted your request.\nMedicine : {obj.medicine}\nQuantity : {obj.quantity}",from_email,[user_mail],html_message=None)
        if table=="saving_request":
            user_mail=obj.user.email
            from_email = 'mediconnect007@gmail.com'
            send_mail("Request from Mediconnect",f"We are happy to help you.\nWe have accepted your request.\nEquipment : {obj.aid.name}\nRate : {obj.aid.rate}",from_email,[user_mail],html_message=None)
    return redirect('admin_dashboard')

@login_required
def remove(request):
    if request.method=='GET':
        id=request.GET.get('id')
        table=request.GET.get('table')
        model = apps.get_model(app_label='dem11app', model_name=table)
        obj=model.objects.filter(id=id).first()
        obj.removed="True"
        obj.save()  
    return redirect('admin_dashboard')
@login_required
def medicine(request):
    if request.method=='POST':
        form=MedicineForm(request.POST)
        
        if form.is_valid():
            selected_disease = request.POST.get('disease')
            other_disease = request.POST.get('other_disease')
            if selected_disease == 'Other':
                disease = other_disease
            else:
                disease = selected_disease

            print(selected_disease,other_disease)

            medicine=form.save(commit=False)
            medicine.user=request.user
            medicine.disease=disease

            existing_medicine = medicines.objects.filter(name=medicine.name, disease=medicine.disease).first()

            if existing_medicine:
                existing_medicine.quantity += medicine.quantity
                existing_medicine.save()
            else:
                medicine.save()

            SendMailToAdmin('New Medicine Submission',get_medicine_message(medicine))
            SendMailToUser('Thankyou for Your Donation',get_medicine_user_message(medicine),medicine.user.email)
            success(request,'Donation submitted successfully.')
            return redirect('dashboard')
        else:
            print(form.errors)
    else:
        form = MedicineForm()
        print(form['disease'])

        

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
            SendMailToUser('Thankyou for Your Donation',get_aids_user_message(aids),aids.user.email)
            success(request, 'Donation submitted successfully.')
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
            success(request, 'Request submitted successfully.')
            return redirect('dashboard')
        
    else:
        form=Req_med_Form()
    return render(request,"req_med.html",{'form':form})

@login_required
def request_aid(request):
    aids = OtherAids.objects.all()
    return render(request,"req_aids.html",{'aids':aids})
@login_required
def saving_req(request):
    aid_id=request.GET.get('id')
    aid = OtherAids.objects.get(id=aid_id)
    existing_request = saving_request.objects.filter(user=request.user, aid=aid).exists()
    if existing_request:
        info(request, 'You have already requested this aid.')
        return redirect('request_aid')
    # Create a new aid request
    aid_request = saving_request.objects.create(user=request.user, aid=aid)
    SendMailToAdmin('New request Submitted',get_req_aid_message(aid_request))
    success(request, 'Request submitted successfully.')
    return redirect('dashboard')
def get_medicines(request,disease):
    medicines_list = medicines.objects.filter(disease=disease).values('name')
    return JsonResponse(list(medicines_list), safe=False)

def SendMailToAdmin(subject,message):
   
    from_email = 'mediconnect007@gmail.com'
    admin_email = 'anitajustinc@gmail.com'
    send_mail(subject, message, from_email, [admin_email], fail_silently=False)
def SendMailToUser(subject,message,mail_id):
    from_email='mediconnect007@gmail.com'
    user_mail=mail_id
    send_mail(subject, message, from_email, [user_mail], fail_silently=False)



def get_aids_message(aids):
    return f'A new aids submission:\n\n' \
           f'Aids Name: {aids.name}\n' \
           

def get_medicine_message(medicine):
    return f'A new medicine has been submitted:\n\n' \
           f'Medicine Name: {medicine.name}\n' \
           f'Dosage: {medicine.dosage}\n'

def get_req_med_message(receiver):
    medicines = req_med.objects.filter(medicine=receiver.medicine).first()
    return f'A new request has been submitted:\n\n' \
           f'Medicine Name: {medicines.medicine}\n' \
           f'Disease: {medicines.disease}\n'

def get_req_aid_message(aid_request):
    return f'A new request has been submitted:\n\n' \
           f'Aid Name: {aid_request.aid}\n' \
           f'requested by: {aid_request.user}\n'

def get_medicine_user_message(medicine):
    return f'We want to express our heartfelt gratitude for your generous donation of medicine to Mediconnect. \n'\
           f'Your act of kindness is making a significant impact on the lives of those in need.\n'\
           f'Here are some details regarding your donation:\n'\
           f'Medicine Name: {medicine.name}\n'\
           f'Quantity: {medicine.quantity}\n'\
           f'Disease: {medicine.disease}\n'
def get_aids_user_message(aids):
    return f'We want to express our heartfelt gratitude for your generous donation to Mediconnect. \n'\
           f'Your act of kindness is making a significant impact on the lives of those in need.\n'\
           f'Here are some details regarding your donation:\n'\
           f'Name of Equipment: {aids.name}\n'\
           f'Rate: {aids.rate}\n'
