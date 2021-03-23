from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,HttpResponse,redirect
from .models import *
import bcrypt
from django.contrib import messages
from django.db.models import Count


def index(request):
    return render(request,"Login_Registration.html")

def create_user(request):
    if(request.method=='POST'):
        errors=User.objects.create_validator(request.POST)
        if len(errors)>=1:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/') 
        else: 
            password = request.POST['password'] 
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            dk=User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=pw_hash)
            return redirect('/')

def login(request):
    if(request.method=="POST"):
        user = User.objects.filter(email=request.POST['email'])
        if len(user)!=0:
            logged_user=user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/main')
        messages.error(request, "email and password don't match")
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def main(request):
    if('user_id' not in request.session):
        return redirect('/')
    context={
        "curr_user":User.objects.get(id=request.session['user_id']),
        "all_orgs":Organization.objects.annotate(total_members=Count('members')).order_by('-total_members')
    }
    return render(request,"main.html",context)

def create_organization(request):
    if(request.method=="POST"):
        errors=Organization.objects.create_validator(request.POST)
        if len(errors)>=1:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/main') 
        else:
            logged_user=User.objects.get(id=request.session['user_id'])
            bk=Organization.objects.create(name=request.POST["name"],desc=request.POST["desc"],creator=logged_user)
            messages.success(request,"organisation successfully created")
            logged_user.org_joined.add(bk)
            #bk.members.add(logged_user)
            return redirect('/main')

def delete(request,org_id):
    if request.method=="POST":
        list_orgs=Organization.objects.filter(id=org_id)
        if len(list_orgs)==0:
            return redirect('/main')
        org_to_delete = Organization.objects.get(id=org_id)
        if org_to_delete.creator.id==request.session['user_id']:
            org_to_delete.delete()
    return redirect('/main')


def display_details(request,org_id):
    if('user_id' not in request.session):
        return redirect('/')
    if len(Organization.objects.filter(id=org_id))>=1:
        context={
            'curr_org':Organization.objects.get(id=org_id),
            'curr_user':User.objects.get(id=request.session['user_id']),
            'all_members':Organization.objects.get(id=org_id).members.all()
        }
        return render(request,'org_details.html',context)
    else:
        return redirect('/main')

def join_group(request,org_id):
    if('user_id' not in request.session):
        return redirect('/')
    curr_user = User.objects.get(id=request.session['user_id'])
    curr_org=Organization.objects.get(id=org_id)
    if request.method=="POST":
        if curr_user not in  curr_org.members.all():
            curr_org.members.add(curr_user)
    return redirect(f"/org/display_details/{org_id}")

def leave_group(request,org_id):
    if('user_id' not in request.session):
        return redirect('/')
    curr_user = User.objects.get(id=request.session['user_id'])
    curr_org=Organization.objects.get(id=org_id)
    if request.method=="POST":
        if curr_user in  curr_org.members.all():
            curr_org.members.remove(curr_user)
    return redirect(f"/org/display_details/{org_id}")
