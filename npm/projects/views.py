from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
import validators
from .models import Project,Remarks,Contact
import re


def formaturl(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'https://{}'.format(url)
    return url

def Index(request):
    sort_by = request.GET.get("sort_by")
    print(sort_by)
    # proList = Project.objects.all()
    # proList = Project.objects.order_by('title')

    if sort_by=='pub_on' or sort_by=='updated_on':
        proList=Project.objects.order_by('-updated_on')
    elif sort_by:
        proList = Project.objects.order_by(sort_by)
    else:
        proList = Project.objects.all()
    params={
        "data":proList
    }
    return render(request,"project/index.html",params)

def Search(request):
    searched=request.POST['searched']
    proList=Project.objects.filter(title__contains=searched)
    params={
        "searched":searched,
        "data":proList
    }
    return render(request,"project/search.html",params)


def CreateView(request):

    return render(request,"project/createForm.html")

def Delete(request,id):
    project = Project.objects.get(id=id)
    if((project.submitted_by.id == request.user.id) or request.user.is_superuser):
        project.delete()
    else:
        messages.add_message(request, messages.ERROR, 'You cannot delete this Project')
        return redirect("/project/")

    messages.add_message(request, messages.SUCCESS, 'Project deleted successfully.')
    return redirect("/project/")


def RemarksForm(request,id):
    try:
        rating = request.POST['rating']
        remarks = request.POST['remarks']
        author = request.user
        project = Project.objects.get(id=id)
        print(float(rating))
        NewRemarks = Remarks(rating = rating ,remarks = remarks , author = author ,  project = project )
        NewRemarks.save()
        return redirect("/project/")
    except Exception as e:
        messages.add_message(request, messages.ERROR, e)
        return redirect("/project/")

    params={}
    return render(request,"project/index.html",params)


def Edit(request,id):
    if request.method == "POST":
        screenshot = None
        email = request.POST.get("email")
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        enroll_no = request.POST.get("enroll_no")
        year = request.POST.get("year")
        sec = request.POST.get("sec")
        git_link = request.POST.get("git_link")
        live_link = request.POST.get("live_link")

        if(request.FILES):
            screenshot = request.FILES["screenshot"]
        submitted_by = request.user # user should be logined in

        # validations
        if(not(len(enroll_no)==10)):
            messages.add_message(request, messages.ERROR, 'Enrollment number Invalid.')
            return redirect("/project/create/")
        if( not (validators.url(git_link))):
            messages.add_message(request, messages.ERROR, 'Link Invalid.')
            return redirect("/project/create/")
        else:
            git_link = formaturl(git_link)
        if( len(live_link)<0 and not (validators.url(live_link))):
            messages.add_message(request, messages.ERROR, 'Link1 Invalid.')
            return redirect("/project/create/")
        else:
            live_link = formaturl(live_link)
        if(request.user is None):
            messages.add_message(request, messages.ERROR, 'You are not Loggedin. ')
            return redirect("/members/login/")

        # validation over
        try:
            project = Project.objects.get(id=id)

            project.email = email
            project.title = title
            project.desc = desc
            project.enroll_no = enroll_no
            project.year = year
            project.sec = sec
            project.git_link = git_link
            project.live_link = live_link if (len(str(live_link))>0) else None
            project.screenshot = screenshot if (not (request.FILES==None))else None
            project.submitted_by = submitted_by

            project.save()
            messages.add_message(request, messages.SUCCESS,"Project edit successfull")
            return redirect("/project/")
        except Exception as e:
                messages.add_message(request, messages.ERROR, e)
                return redirect("/project/")

    else:
        messages.add_message(request, messages.ERROR, 'You are not allowed here')
        return redirect("/project/")


def Create(request):
    if request.method == "POST":
        screenshot = None
        email = request.POST.get("email")
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        enroll_no = request.POST.get("enroll_no")
        year = request.POST.get("year")
        sec = request.POST.get("sec")
        git_link = request.POST.get("git_link")
        live_link = request.POST.get("live_link")
        if(request.FILES):
            screenshot = request.FILES["screenshot"]
        submitted_by = request.user

        # validations
        if(not(len(enroll_no)==10)):
            messages.add_message(request, messages.ERROR, 'Enrollment number Invalid.')
            return redirect("/project/create/")
        if( not (validators.url(git_link))):
            messages.add_message(request, messages.ERROR, 'Link Invalid.')
            return redirect("/project/create/")
        if( len(live_link)<0 and not (validators.url(live_link))):
            messages.add_message(request, messages.ERROR, 'Link1 Invalid.')
            return redirect("/project/create/")
        if(request.user is None):
            messages.add_message(request, messages.ERROR, 'You are not allowed here')
            return redirect("/project/create/")

        # validation over
        try:
            NewProject = Project(
                                    email=email,
                                    title=title,
                                    desc=desc,
                                    enroll_no=enroll_no,
                                    year=year,sec=sec,
                                    git_link=git_link,
                                    live_link=live_link if (not len(live_link)>0)else None,
                                    screenshot= screenshot if (not (request.FILES==None))else None,
                                    submitted_by=submitted_by
                                )
            NewProject.save()
            return redirect("/project/")

        except Exception as e:

                messages.add_message(request, messages.ERROR, e)
                return redirect("/project/")

        return render(request,"project/index.html")
    else:
        messages.add_message(request, messages.ERROR, 'You are not allowed here')
        return redirect("/")




def contactus(req):
    return render(req,"project/contactus.html")

def contactSubmit(req):
    email=req.POST.get("email")
    name=req.POST.get("name")
    tel=req.POST.get("phone")
    desc=req.POST.get("desc")
    File=req.POST.get("screenshot")
    newContact=Contact(email=email,name=name,desc=desc,phone=tel,screenshot=File)
    newContact.save()
    return HttpResponse("Thank You For your Feedback :)")