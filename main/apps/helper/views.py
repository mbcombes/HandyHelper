from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Job, Category
import bcrypt

def index(request):     # GET /
    return render(request, 'helper/index.html')

def create(request):    # POST /create
    # to check if there are errors.
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(errors)
        return redirect('/')
    elif request.method == 'POST':    # if no errors were detected.
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        new_user=User.objects.create(first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=pw_hash)
        request.session['username']=new_user.first_name
        request.session['id']=new_user.id
        print("this is the submit path")
        print(new_user)
        return redirect('/dashboard')

def login(request):    # POST /login
    # to check if there are errors.
    print(request.POST['email'])
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(errors)
        return redirect('/')
    elif request.method == 'POST':    # if no errors were detected.
        user=User.objects.get(email=request.POST['email'])
        request.session['username']=user.first_name
        request.session['id']=user.id
    return redirect('/dashboard')

def dashboard(request):   # GET /dashboard
    if 'id' in request.session:
        all_jobs=Job.objects.exclude(helper=User.objects.get(id=request.session['id']))
        help_jobs=Job.objects.filter(helper=User.objects.get(id=request.session['id']))
        
        context={
            "all_jobs": all_jobs,
            'help_jobs': help_jobs,
        }
        print(all_jobs)
        print(help_jobs)
        return render(request, 'helper/dashboard.html', context)
    else:
        messages.error(request, 'Please Log In.', extra_tags='fail')
        return redirect('/')

def destroy(request):  # /destroy
    del request.session['username']
    del request.session['id']
    print('session cleared')
    return redirect('/')

def newjob(request): # /jobs/new
    all_jobs=Job.objects.all()
    categories=Category.objects.all()
    context={
        'all_jobs': all_jobs,
        'categories':categories
    }
    return render(request, 'helper/new.html', context)

def create_job(request): # /jobs/create
    errors = Job.objects.job_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(errors)
        return redirect('/jobs/new')
    elif request.method == "POST":
        new_job=Job.objects.create(job=request.POST['job'], description=request.POST['description'], location=request.POST['location'], creator=User.objects.get(id=request.session['id']))
        if len(request.POST['otheroption'])>0:
            Category.objects.create(name=request.POST['otheroption'])
            new_job.category.add(Category.objects.get(name=request.POST['otheroption']))
        print(request.POST.getlist('category'))
        if len(request.POST.getlist('category'))>0:
            for choice in request.POST.getlist('category'):
                print(choice)
                new_job.category.add(Category.objects.get(id=choice))
    return redirect('/dashboard')

def edit_job(request, id): # /jobs/<id>/edit
    this_job=Job.objects.get(id=id)
    context={
        'this_job': this_job
    }
    return render(request, 'helper/edit.html', context)

def update_job(request):
    errors = Job.objects.job_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(errors)
        return redirect(f"/jobs/{request.POST['jobid']}/edit")
    elif request.method == 'POST':
        this_job=Job.objects.get(id=request.POST['jobid'])
        this_job.job=request.POST['job']
        this_job.description=request.POST['description']
        this_job.location=request.POST['location']
        # this_job.category=request.POST['category']
        this_job.save()
    return redirect('/dashboard')

def view(request, id):
    this_job=Job.objects.get(id=id)
    context = {
        'this_job': this_job,
    }
    return render(request, 'helper/view.html', context)

def destroy_job(request, id): # /jobs/<id>/destroy
    this_job=Job.objects.get(id=id)
    this_job.delete()
    return redirect('/dashboard')

def join(request, id): # /jobs/<id>/join
    this_user=User.objects.get(id=request.session['id'])
    print(this_user)
    this_job=Job.objects.get(id=id)
    print(this_job)
    this_job.helper.add(this_user)
    return redirect('/dashboard')

def cancel(request, id): # /jobs/<id>/cancel
    this_job=Job.objects.get(id=id)
    helper=User.objects.get(id=request.session['id'])
    this_job.helper.remove(helper)
    return redirect('/dashboard')
