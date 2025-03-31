from email.message import EmailMessage
import random
import smtplib
import ssl

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.shortcuts import render,redirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from datetime import *

from ctapp.models import *
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import os
from django.db.models import Count

# Create your views here.
def index(request):
    today = date.today()
    return render(request,'index.html',{'today':today})
def user_login(request):
     return render(request,'login.html')
def user_registration(request):
     today = date.today()
     return render(request,'user_registration.html',{'today':today})
# def user_registration(request):
  
#     return render(request,'user_registration.html',{'today':today})
def admin_logout(request):
    logout(request)
    request.session.delete()
    return redirect('user_login')
def user_logout(request):
    logout(request)
    request.session.delete()
    return redirect('user_login')
def user_action(request):
   
    username=request.POST.get("username")
    username_exists = Login.objects.filter(username=username).exists() or User.objects.filter(username=username).exists()
    data = {
    'username_exists': username_exists,
    'error': "Username Already Exists" if username_exists else ""
    }
    if(data["username_exists"]==False):
        tbl1=Login()
        username=request.POST.get("username")
        tbl1.username=request.POST.get("username")
        password=request.POST.get("password")
        tbl1.password=password
        tbl1.user_type="User"
        tbl1.status="Approved"
        tbl1.save()
        obj=Login.objects.get(username=username,password=password)

        u=UserInfo()

        u.login_id = obj.login_id
        u.name=request.POST.get("Name")
        u.phone_number =request.POST.get("phone")
        u.email_id=request.POST.get("Email")
        u.dob=request.POST.get("dob")
        u.address=request.POST.get("address")
       
        u.save()
        messages.add_message(request, messages.INFO, 'Registered successfully.')
        return redirect('user_registration')
    else:
        messages.add_message(request, messages.INFO, 'User name is already Exist. Sorry Registration Failed.')
        return redirect('user_registration')
def login_action(request):
    u=request.POST.get("username")
    p=request.POST.get("password")
    obj=authenticate(username=u,password=p)
    if obj is not None:
        if obj.is_superuser == 1:
            request.session['aname'] = u
            request.session['slogid'] = obj.id
            return redirect('admin_home')
        else:
          messages.add_message(request, messages.INFO, 'Invalid User.')
          return redirect('user_login')
    else:
        newp=p
        try:
            obj1=Login.objects.get(username=u,password=newp)

            if obj1.user_type=="User":
                if(obj1.status=="Approved"):
                    request.session['uname'] = u
                    request.session['slogid'] = obj1.login_id
                    return redirect('user_home')
                elif(obj1.status=="Not Approved"):
                  messages.add_message(request, messages.INFO, 'Waiting For Approval.')
                  return redirect('user_login')
                else:
                  messages.add_message(request, messages.INFO, 'Invalid User.')
                  return redirect('user_login')
            elif obj1.user_type=="Police":
                if(obj1.status=="Approved"):
                    request.session['pname'] = u
                    request.session['slogid'] = obj1.login_id
                    return redirect('police_home')
                elif(obj1.status=="Not Approved"):
                  messages.add_message(request, messages.INFO, 'Waiting For Approval.')
                  return redirect('user_login')
                else:
                  messages.add_message(request, messages.INFO, 'Invalid User.')
                  return redirect('user_login')
            else:
                 messages.add_message(request, messages.INFO, 'Invalid User.')
                 return redirect('user_login')
        except Login.DoesNotExist:
         messages.add_message(request, messages.INFO, 'Invalid User.')
         return redirect('user_login') 
def admin_home(request):
    if 'aname' in request.session:
       
        return render(request, 'Master/index.html')
    
    else:
      return redirect('user_login')
def user_home(request):
    if 'uname' in request.session:
       
        return render(request, 'User/index.html')
    
    else:
      return redirect('user_login')
  
def save_category(request):
    if 'aname' in request.session:
        
        tbl=Category()
        tbl.category=request.POST.get("category")
        tbl.save()
        messages.add_message(request, messages.INFO, 'Added successfully.')
        return redirect('add_category')
    else:
        return redirect('login')
def add_category(request):
 if 'aname' in request.session:
    data=Category.objects.all()
    return render(request,'Master/category.html',{'data':data})
 else:
      return redirect('login')
def edit_category(request,id):
 if 'aname' in request.session:
    data=Category.objects.get(category_id=id)
    return render(request,'Master/edit_category.html',{'data':data})
 else:
      return redirect('login')


def update_category(request,id):
 if 'aname' in request.session:
    tbl=Category.objects.get(category_id=id)
    tbl.category=request.POST.get("category")
    tbl.save()
    messages.add_message(request, messages.INFO, 'Updated successfully.')
    return redirect('add_category')
 else:
      return redirect('login')
def delete_category(request,id):
 if 'aname' in request.session:
    tbl=Category.objects.get(category_id=id)
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Deleted successfully.')
    return redirect('add_category')
 else:
      return redirect('login')
           
      
def users_list(request):
    if 'aname' in request.session:
     data=UserInfo.objects.all()
     return render(request,'Master/users_list.html',{'data':data})
    else:
      return redirect('user_login')
 
def profile(request):
    if 'uname' in request.session:
        data=get_user(request.session['slogid'])
       
        return render(request,'User/profile.html',{'data':data})
    else:
       return redirect('user_login')
    # ----------------End Feedback -------------------------------------------------



def add_complaints(request):
    if 'uname' in request.session:
            crime = Category.objects.all() 
            state = State.objects.all() 
            current_datetime = datetime.now()
            context = {'crime_types': crime,'state':state,'current_datetime': current_datetime}
            return render(request, 'User/add_complaints.html',context)
    else:
        return redirect('user_login')
def submit_complaint(request):
    if 'uname' in request.session:
                        
                user=get_user(request.session['slogid'])
                category_id = request.POST.get('crimeType')
                district_id = request.POST.get('district')
                police_station_id = request.POST.get('police_station')
                place = request.POST.get('place')
                subject = request.POST.get('subject')
                complaint_text = request.POST.get('complaintText')
                crime_datetime = request.POST.get('crimeDatetime')
                latitude = request.POST.get("latitude")
                longitude = request.POST.get("longitude")
           

                # Fetch related objects
                category = Category.objects.get(category_id=category_id)
                district = District.objects.get(district_id=district_id)
                police_station = PoliceStation.objects.filter(police_station_id=police_station_id).first()

                document=request.FILES['document']

                split_tup = os.path.splitext(document.name)
                file_extension = split_tup[1]
                # folder path
                dir_path = settings.MEDIA_ROOT
                count = 0
                # Iterate directory
                for path in os.listdir(dir_path):
                # check if current path is a file
                    if os.path.isfile(os.path.join(dir_path, path)):
                        count += 1
                filecount=count+1
                filename=str(filecount)+file_extension
                obj=FileSystemStorage()
                file=obj.save(filename,document)
                url1=obj.url(file)
                # Save the complaint
                complaint = Crime.objects.create(
                    user=user,
                    category=category,
                    district=district,
                    police_station=police_station,
                    place=place,
                    subject=subject,
                    complaint_text=complaint_text,
                    crime_datetime=crime_datetime,
                    supporting_document=url1,
                    latitude = latitude,
                    longitude = longitude,
                    
                )
                
                # Redirect or send a success response
                messages.add_message(request, messages.INFO, 'Added successfully.')
                return redirect('add_complaints')
    else:
        return redirect('user_login')
def display_police_station(request):
    district_id = request.GET.get("district_id")
    try:

        dist = PoliceStation.objects.filter(district_id = district_id)
    except Exception:
        data=[]
        data['error_message'] = 'error'
        return JsonResponse(data)
    return JsonResponse(list(dist.values('police_station_id', 'place')), safe = False)
def display_police(request):
    police_station_id = request.GET.get("police_station_id")
    try:

        dist = PoliceOfficer.objects.filter(police_station_id = police_station_id)
    except Exception:
        data=[]
        data['error_message'] = 'error'
        return JsonResponse(data)
    return JsonResponse(list(dist.values('police_officer_id', 'name')), safe = False)
def view_complaints(request):
    if 'uname' in request.session:
            user=get_user(request.session['slogid'])
            crime=Crime.objects.filter(user=user)
            context = {'crime': crime,}
            return render(request, 'User/view_complaints.html',context)
    else:
        return redirect('user_login')
def crime_more(request,id):
    if 'uname' in request.session:
     
            crime=Crime.objects.get(pk=id)
            fir = FIR.objects.filter(crime_id=id).first() 
            
            context = {'crime': crime,'fir':fir}
            return render(request, 'User/crime_more.html',context)
    else:
        return redirect('user_login')
    

# ------------- Feedback ------------------------------------------


def feedback(request):
    if 'uname' in request.session:
        user=get_user(request.session['slogid'])
        data1 = Feedback.objects.filter(user=user)
        return render(request,'User/feedback.html',{'data1':data1})
    else:
       return redirect('user_login')
def save_feedback(request):
    if 'uname' in request.session:
        tbl=Feedback()
    
        tbl.user=UserInfo.objects.get(user_id=get_user(request.session['slogid']).user_id)
        # tbl.feedback_subject=request.POST.get("subject")
        tbl.feedback=request.POST.get("feedback")
        tbl.save()
        messages.add_message(request, messages.INFO, 'Added successfully.')
        return redirect('feedback')
    else:
       return redirect('user_login')

def delete_feedback(request,id):
    if 'uname' in request.session:
        tbl=Feedback.objects.get(feedback_id=id)
        tbl.delete()
        messages.add_message(request, messages.INFO, 'Deleted successfully.')
        return redirect('feedback')
    else:
       return redirect('user_login')
    
def view_feedback(request):
    if 'aname' in request.session:
        
        data= Feedback.objects.filter(reply__isnull=True)
        return render(request,'Master/view_feedback.html',{'data':data})
    else:
       return redirect('user_login')
def feedback_replied_list(request):
    if 'aname' in request.session:
        data= Feedback.objects.filter(reply__isnull=False)
        return render(request,'Master/replied_feedback.html',{'data':data})
    else:
       return redirect('user_login')
def adm_reply_feedback(request,id):
    if 'aname' in request.session:

        return render(request,'Master/reply_feedback.html',{'id':id})
    else:
       return redirect('user_login')
def add_reply_feedback(request,id):
    tbl=Feedback.objects.get(feedback_id=id)
    tbl.reply=request.POST.get("reply")
    tbl.save()
    return redirect('feedback_replied_list')

def profile(request):
    if 'uname' in request.session:
        data=get_user(request.session['slogid'])
       
        return render(request,'User/profile.html',{'data':data})
    else:
       return redirect('user_login')
    
def police_home(request):
    if 'pname' in request.session:
        data = get_police_o(request.session['slogid'])
        p_type = data.p_type
        link = "CISI" if p_type in ['CI', 'DSP'] else ""
        
        return render(request, 'Police/index.html', {
            'pdata': data,
            'link': link
        })
    
    else:
        return redirect('user_login')
    
 
def add_police_station(request):
    if 'aname' in request.session:
            data=State.objects.all()
            return render(request, 'Master/add_police_station.html',{'data':data})
    else:
        return redirect('user_login')
    
def save_station(request):
    if 'aname' in request.session:
       
            tbl=PoliceStation()
            tbl.district_id=request.POST.get("district")
            tbl.place=request.POST.get("place")
            tbl.address=request.POST.get("address")
            tbl.phone_number=request.POST.get("phone")
            tbl.mail_id=request.POST.get("mail_id")
            tbl.save()
            messages.add_message(request, messages.INFO, 'Added successfully.')
            return redirect('add_police_station')
      
    else:
        return redirect('user_login')
def display_district(request):
    state_id = request.GET.get("state_id")
    try:

        dist = District.objects.filter(state_id = state_id)
    except Exception:
        data=[]
        data['error_message'] = 'error'
        return JsonResponse(data)
    return JsonResponse(list(dist.values('district_id', 'district')), safe = False)

def list_police_station(request):
    if 'aname' in request.session:
            data=PoliceStation.objects.all()
            return render(request, 'Master/list_police_station.html',{'data':data})
    else:
        return redirect('user_login')
def edit_police_station(request,id):
    if 'aname' in request.session:
            data=PoliceStation.objects.get(police_station_id=id)
            return render(request, 'Master/edit_police_station.html',{'data':data})
    else:
        return redirect('user_login')
def update_police_station(request,id):
    if 'aname' in request.session:

       


        tbl=PoliceStation.objects.get(police_station_id=id)
    
        tbl.place=request.POST.get("place")
        tbl.address=request.POST.get("address")
        tbl.phone_number=request.POST.get("phone")
        tbl.mail_id=request.POST.get("mail_id")
        tbl.save()
        messages.add_message(request, messages.INFO, 'Updated successfully.')
        return redirect('list_police_station')
    else:
        return redirect('user_login')
def delete_police_station(request,id):
 if 'aname' in request.session:
        police_station =PoliceStation.objects.get(police_station_id=id)
        login = police_station.login
        police_station.delete()              
        login.delete()
        messages.add_message(request, messages.INFO, 'Deleted successfully.')
        return redirect('list_police_station')
 else:
      return redirect('login')
def police_registration(request):
            today = date.today()
            min_dob = today.replace(year=today.year - 20)  # 20 years before today
            data=State.objects.all()
            return render(request, 'police_registration.html',{'data':data,'today':min_dob})

def save_police(request):
        username=request.POST.get("username")
        data = {
        'username_exists':      Login.objects.filter(username=username).exists(),
            'error':"Username Already Exist"
        }
        if(data["username_exists"]==False):
            username=request.POST.get("username")
            password=request.POST.get("password")
            tbl1=Login()
            tbl1.username=username
            tbl1.password=password
            tbl1.user_type="Police"
            tbl1.status="Submitted"
            tbl1.save()
        
            obj=Login.objects.get(username=username,password=password)

            tbl=PoliceOfficer()
            tbl.login_id = obj.login_id
            tbl.name=request.POST.get("full_name")
            tbl.district_id=request.POST.get("district")
            tbl.place=request.POST.get("place")
            tbl.address=request.POST.get("address")
            tbl.phone_number=request.POST.get("phone")
            tbl.mail_id=request.POST.get("mail_id")
            tbl.qualification=request.POST.get("qualification")
            tbl.gender=request.POST.get("gender")
            tbl.date_of_birth=request.POST.get("date_of_birth")
            
            
            photo=request.FILES['photo']

            split_tup = os.path.splitext(photo.name)
            file_extension = split_tup[1]
            # folder path
            dir_path = settings.MEDIA_ROOT
            count = 0
            # Iterate directory
            for path in os.listdir(dir_path):
            # check if current path is a file
                if os.path.isfile(os.path.join(dir_path, path)):
                    count += 1
            filecount=count+1
            filename=str(filecount)+file_extension
            obj=FileSystemStorage()
            file=obj.save(filename,photo)
            url1=obj.url(file)
            # proof
            proof=request.FILES['proof']

            split_tup = os.path.splitext(proof.name)
            file_extension = split_tup[1]
            # folder path
            dir_path = settings.MEDIA_ROOT
            count = 0
            # Iterate directory
            for path in os.listdir(dir_path):
            # check if current path is a file
                if os.path.isfile(os.path.join(dir_path, path)):
                    count += 1
            filecount=count+1
            filename=str(filecount)+file_extension
            obj=FileSystemStorage()
            file=obj.save(filename,proof)
            url2=obj.url(file)
            tbl.photo=url1
            tbl.proof=url2
            tbl.save()
            messages.add_message(request, messages.INFO, 'Registered successfully.')
            return redirect('police_registration')
        else:
            messages.add_message(request, messages.INFO, 'User name is already Exist. Sorry Registration Failed.')
            return redirect('police_registration')

def submitted_police(request):
    if 'aname' in request.session:
       
        submitted_users = Login.objects.filter(status="Submitted").values_list('login_id', flat=True)
        police_officers = PoliceOfficer.objects.filter(login_id__in=submitted_users)
        context = {'police_officers': police_officers}
        return render(request, 'Master/submitted_police.html', context)
    else:
        return redirect('user_login')
def to_approve_police(request,id):
    if 'aname' in request.session:
            data=State.objects.all()
            return render(request, 'Master/to_approve_police.html',{'state':data,'id':id})
    else:
        return redirect('user_login')
def approve_police(request,id):
    if 'aname' in request.session:

        police_id = id
        police_station_id = request.POST.get('police_station')

        if not police_id or not police_station_id:
            return JsonResponse({'message': 'Invalid data provided!'}, status=400)

        # Fetch the police record and update its status and police station
        police = get_object_or_404(PoliceOfficer, pk=police_id)
        police.police_station_id = police_station_id
        police.p_type=request.POST.get("p_type")
        police.save()

        # Update the login table status to 'Approved'
        logid=police.login_id
        login = get_object_or_404(Login, login_id=logid)
        login.status = "Approved"  
        login.save()
        messages.add_message(request, messages.INFO, 'Approved successfully.')
        return redirect('submitted_police')
    else:
        return redirect('user_login')
def reject_police(request,id):
    if 'aname' in request.session:

        police_id = id
      
        police = get_object_or_404(PoliceOfficer, pk=police_id)
        logid=police.login_id
        login = get_object_or_404(Login, login_id=logid)
        login.status = "Rejected"  
        login.save()
        messages.add_message(request, messages.INFO, 'Rejected successfully.')
        return redirect('submitted_police')
    else:
        return redirect('user_login')
def approved_list(request):
    if 'aname' in request.session:
        data=State.objects.all()
        submitted_users = Login.objects.filter(status="Approved").values_list('login_id', flat=True)
        police_officers = PoliceOfficer.objects.filter(login_id__in=submitted_users)
        context = {'police_officers': police_officers,'state':data}
        return render(request, 'Master/approved_list.html', context)
    else:
        return redirect('user_login')
def search_police(request):
    if 'aname' in request.session:
        station=request.POST.get('police_station')
        data=State.objects.all()
        submitted_users = Login.objects.filter(status="Approved").values_list('login_id', flat=True)
        police_officers = PoliceOfficer.objects.filter(login_id__in=submitted_users,police_station_id=station)
        context = {'police_officers': police_officers,'state':data}
        return render(request, 'Master/approved_list.html', context)
    else:
        return redirect('user_login')
def submitted_crimes(request):
    if 'aname' in request.session:
           
            crime=Crime.objects.filter(status="Pending")
            context = {'crime': crime,}
            return render(request, 'Master/view_crime.html',context)
    else:
        return redirect('user_login')
def adm_crime_more(request,id):
    if 'aname' in request.session:
     
            crime=Crime.objects.get(pk=id)
            fir=FIR.objects.get(crime_id=id)
            
            context = {'crime': crime,'fir':fir}
            return render(request, 'Master/crime_more.html',context)
    else:
        return redirect('user_login')
def assign_crimes(request,id):
    if 'aname' in request.session:
        crime=Crime.objects.get(pk=id)
        crime.status="Assigned to Police"
        crime.police_officer_id=request.POST.get('police')
        crime.save()
        messages.add_message(request, messages.INFO, 'Assigned to Police successfully.')
        return redirect('submitted_crimes')
    else:
        return redirect('user_login')
def to_assign_crimes(request,id):
    if 'aname' in request.session:
        data=State.objects.all()
        crime=Crime.objects.get(crime_id=id)
     
        return render(request, 'Master/to_assign_crimes.html',{'state':data,'id':id,'crime':crime})
    else:
        return redirect('user_login')
def assigned_crimes(request):
    if 'aname' in request.session:
           
            crime=Crime.objects.filter(status="Assigned to Police")
            context = {'crime': crime,}
            return render(request, 'Master/view_assigned_crime.html',context)
    else:
        return redirect('user_login')
def transfer(request):
    if 'aname' in request.session:
            state = State.objects.all() 
            context = {'state': state}
            return render(request, 'Master/transfer.html',context)
    else:
        return redirect('user_login')
def transfer_details(request):
    if 'aname' in request.session:
            state = State.objects.all() 
            context = {'state': state}
            return render(request, 'Master/transfer.html',context)
    else:
        return redirect('user_login')
def save_transfer(request):
    if 'aname' in request.session:
        police_id = request.POST.get('police')
        new_police_id = request.POST.get('police1')
        police_station_id = request.POST.get('police_station')
        assigned_station_id = request.POST.get('police_station1')
        new_station_id = request.POST.get('police_station2')
        if police_station_id != assigned_station_id:
            messages.error(request, 'New assigned officer must be in the same police station as the current officer.')
            return redirect('transfer')

        if police_id == new_police_id:
            messages.error(request, 'New assigned police officer must be different from the current officer.')
            return redirect('transfer')

        if police_station_id == new_station_id:
            messages.error(request, 'Cannot transfer to the same police station.')
            return redirect('transfer')

        #Crime Change
        crime=Crime.objects.filter(police_officer=request.POST.get('police')).update(police_officer_id=request.POST.get('police1'))
      
        # transfer

        p=PoliceOfficer.objects.get(police_officer_id=request.POST.get('police'))
        p.police_station_id=request.POST.get('police_station2')
        p.save()
        messages.add_message(request, messages.INFO, 'Assigned to Police successfully.')
        return redirect('transfer')  
    else:
        return redirect('user_login')
def p_assigned_crimes(request):
    if 'pname' in request.session:
        data = get_police_o(request.session['slogid'])
        police_officer_id = data.police_officer_id

        crime_list = Crime.objects.filter(status="Assigned to Police", police_officer_id=police_officer_id)
        fir_records = FIR.objects.filter(crime_id__in=crime_list).values_list('crime_id', flat=True)

        context = {'crime': crime_list, 'fir_records': fir_records}
        return render(request, 'Police/view_assigned_crime.html', context)
    else:
        return redirect('user_login')
def crime_updates(request,id):
    if 'pname' in request.session:
        
            CrimeUpdatesdata = CrimeUpdates.objects.filter(crime_id=id)
            context = {'CrimeUpdates': CrimeUpdatesdata,'id':id}
            return render(request, 'Police/crime_updates.html',context)
    else:
        return redirect('user_login')
def save_updates(request,id):
    if 'pname' in request.session:
        data=get_police_o(request.session['slogid'])
        police_officer_id=data.police_officer_id
        crime=CrimeUpdates()
        crime.crime_id=id
        crime.police_officer_id=police_officer_id
        crime.crime_updates=request.POST.get('updates')
        filedoc = request.FILES.get('filedoc')
        if filedoc:
            split_tup = os.path.splitext(filedoc.name)
            file_extension = split_tup[1]

            # Get media directory path
            dir_path = settings.MEDIA_ROOT
            count = sum(os.path.isfile(os.path.join(dir_path, path)) for path in os.listdir(dir_path))

            # Generate a unique filename
            filecount = count + 1
            filename = str(filecount) + file_extension

            # Save file
            obj = FileSystemStorage()
            file = obj.save(filename, filedoc)
            url1 = obj.url(file)
            crime.filedoc = url1  # Store file URL in database

        crime.save()
        messages.add_message(request, messages.INFO, 'Updated Successfully.')
        return redirect('crime_updates',id)
    else:
        return redirect('user_login')
def p_crime_more(request,id):
    if 'pname' in request.session:
     
            crime=Crime.objects.get(pk=id)
            context = {'crime': crime,}
            return render(request, 'Police/crime_more.html',context)
    else:
        return redirect('user_login')
def adm_updates(request,id):
    if 'aname' in request.session:
        
            CrimeUpdatesdata = CrimeUpdates.objects.filter(crime_id=id)
            context = {'CrimeUpdates': CrimeUpdatesdata}
            return render(request, 'Master/crime_updates.html',context)
    else:
        return redirect('user_login')



'''def district_wise(request):
    if 'aname' in request.session:
        hotspots = (
            Crime.objects.values('district__district', 'place')
            .annotate(crime_count=Count('crime_id'))
            .order_by('-crime_count')[:3]  # Limit to top 3
        )

        # Convert data into a format for Chart.js
        districts = [hotspot["district__district"] for hotspot in hotspots]
        places = [hotspot["place"] for hotspot in hotspots]
        crime_counts = [hotspot["crime_count"] for hotspot in hotspots]

        context = {
            "districts": districts,
            "places": places,
            "crime_counts": crime_counts,
        }
        return render(request, "Master/district_hotspots.html", context)
    else:
        return redirect("user_login")




def place_wise(request):
    if 'aname' in request.session:
        hotspots = (
            Crime.objects.values('place', 'district__district')
            .annotate(crime_count=Count('crime_id'))
            .order_by('-crime_count')[:3]  # Limit to top 3 places
        )

        # Convert data into format for Chart.js
        places = [hotspot["place"] for hotspot in hotspots]
        districts = [hotspot["district__district"] for hotspot in hotspots]
        crime_counts = [hotspot["crime_count"] for hotspot in hotspots]

        context = {
            "places": places,
            "districts": districts,
            "crime_counts": crime_counts,
        }
        return render(request, "Master/place_hotspots.html", context)
    else:
        return redirect("user_login")'''


from django.db.models import Count

def district_wise(request):
    if 'aname' in request.session:
        hotspots = (
            Crime.objects.values('district__district')  # Group only by district
            .annotate(crime_count=Count('crime_id'))  # Sum all crime counts per district
            .order_by('-crime_count')[:3]  # Limit to top 3 districts
        )

        # Convert data into a format for Chart.js
        districts = [hotspot["district__district"] for hotspot in hotspots]
        crime_counts = [hotspot["crime_count"] for hotspot in hotspots]

        context = {
            "districts": districts,
            "crime_counts": crime_counts,
        }
        return render(request, "Master/district_hotspots.html", context)
    else:
        return redirect("user_login")



from django.db.models import Count
from collections import defaultdict

def place_wise(request):
    if 'aname' in request.session:
        # Fetch crime data and normalize place names
        raw_hotspots = (
            Crime.objects.values('place')
            .annotate(crime_count=Count('crime_id'))
            .order_by('-crime_count')
        )

        # Aggregate crime counts manually to avoid duplicates
        crime_summary = defaultdict(int)
        for entry in raw_hotspots:
            normalized_place = entry["place"].strip().lower()  # Normalize place name
            crime_summary[normalized_place] += entry["crime_count"]

        # Convert dictionary to lists
        places = list(crime_summary.keys())
        crime_counts = list(crime_summary.values())

        context = {
            "places": places,
            "crime_counts": crime_counts,
        }
        return render(request, "Master/place_hotspots.html", context)
    else:
        return redirect("user_login")




def adm_google_map_view_spot(request, latitude, longitude):
    if 'aname' in request.session:
     
            context = {'latitude': latitude,'longitude': longitude,}
            return render(request, 'Master/google_map_view_spot.html',context)
    else:
        return redirect('user_login')
def p_google_map_view_spot(request, latitude, longitude):
    if 'pname' in request.session:
     
            context = {'latitude': latitude,'longitude': longitude,}
            return render(request, 'Police/google_map_view_spot.html',context)
    else:
        return redirect('user_login')
def add_fir(request, id):
    if 'pname' in request.session:
        crime = get_object_or_404(Crime, crime_id=id)
        return render(request, 'Police/fir.html', {'crime': crime})
    else:
        return redirect('user_login')
def save_fir(request,id):
    if request.method == "POST":
        crime_id = id
        description = request.POST.get('description')
        witness_details = request.POST.get('witness_details')
        evidence_details = request.POST.get('evidence_details')

        crime = get_object_or_404(Crime, crime_id=crime_id)

        # Check if FIR already exists
        if FIR.objects.filter(crime_id=crime).exists():
            messages.warning(request, "FIR already exists for this crime.")
            return redirect('view_fir', crime_id)

        FIR.objects.create(
            crime_id=crime,
            description=description,
            witness_details=witness_details,
            evidence_details=evidence_details
        )
        messages.success(request, "FIR added successfully.")
        return redirect('view_fir', crime_id)

    return redirect('p_assigned_crimes')   
def view_fir(request, id):
    if 'pname' in request.session:
        fir = get_object_or_404(FIR, crime_id=id)
        return render(request, 'Police/view_fir.html', {'fir': fir})
    else:
        return redirect('user_login') 
def p_profile(request):
    if 'pname' in request.session:
        data=get_police_o(request.session['slogid'])
        police_officer_id=data.police_officer_id
        profile = get_object_or_404(PoliceOfficer, police_officer_id=police_officer_id)
        return render(request, 'Police/profile.html', {'profile': profile})
    else:
        return redirect('user_login') 
    
def p_other_crimes(request):
    if 'pname' in request.session:
        data = get_police_o(request.session['slogid'])  # Get logged-in police officer data
        p_type = data.p_type
        crimes=[]

        # DSP & CI can see all crimes in their district
        if p_type in ['DSP']:
            crimes = Crime.objects.filter(district=data.district)
            link = "CISI"
        elif p_type in ['CI']:
            # Other officers can only see crimes in their police station
            crimes = Crime.objects.filter(police_station=data.police_station)
            link = ""

        return render(request, 'Police/p_other_crimes.html', {
            'pdata': data,
            'crimes': crimes,
            'p_type': p_type
        })
    
    else:
        return redirect('user_login')
    
def forget_password(request):
    return render(request,'forget_password.html')

def send_otp(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    c = Login.objects.filter(username=username,user_type='User').count()
    if(c>0):
        data = Login.objects.get(username=username,user_type='User')
        logid= data.login_id
        data2 = UserInfo.objects.get(login_id=logid)
        reg_email=data2.email_id
        if(str(email)==str(reg_email)):
            sub="Your OTP From CrimeTracker"
            msg=generate_otp(4)
            send_mail(email,msg,sub)
            msg1=msg
            return render(request,'check_otp.html',{'msg':msg1,'logid':logid})
        else:
            messages.add_message(request, messages.INFO, 'This is not your Registered Email Id')
            return redirect('user_login')
    else:
            messages.add_message(request, messages.INFO, 'Invalid User name')
            return redirect('user_login')
def check_otp_action(request):
     logid=request.POST.get("logid")
     otp=request.POST.get("otp")
   
     otpsend = request.POST.get("sendotp")
     if(int(otpsend)==int(otp)):
      
        return render(request,'new_password.html',{'logid':logid})
def change_psd(request):
     logid=request.POST.get("logid")
     password=request.POST.get("password")
     tbl = Login.objects.get(login_id=logid)
     tbl.password=password
     tbl.save()      
     messages.add_message(request, messages.INFO, 'Password has been changed')
     return redirect('user_login')
def send_mail(erc,msg,sub):
    email_sender="meryljo25@gmail.com"
    email_password="qdnngmrsibcxmbvz"
    email_receiver=erc
    subject=sub
    body=msg
    em=EmailMessage()
    em['From']="CrimeTracker"
    em['To']=email_receiver
    em['Subject']=subject
    em.set_content(body)
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_receiver,em.as_string())

def generate_otp(length): # Define the function with the parameter ‘length’
    otp = ""
    for _ in range(length): # Use for loop
        otp += str(random.randint(0, 9)) # 
    return otp
        

def get_user(logid):
     data=UserInfo.objects.get(login_id=logid)
     return data
def get_police_o(logid):
     data=PoliceOfficer.objects.get(login_id=logid)
     return data