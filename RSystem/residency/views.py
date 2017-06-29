from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.utils import timezone
from .forms import AuthorForm,RegisterForm
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.db.models import Sum

from django.contrib.auth.models import User

from django.http import JsonResponse

from django.template import RequestContext

from django.db.models import Q
def index(request):
    logout(request)
    global user
    user = None
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            try:
                print(form.cleaned_data['username'])
                print(form.cleaned_data.get('password'))
                author = authenticate(username = str(form.cleaned_data['username']),password=str(form.cleaned_data.get('password')))
                print(author)
                logg = login(request,author)
                print(request.user)
                if(request.user is not None):
                    print(request.user.has_perm('poll.change_poll'))
                    if (request.user.has_perm('poll.change_poll')):
                        return redirect('superuser')

            except:
                return render(request, 'index/index.html', {'AuthorForm': form, 'check': True})
    else:
        form = AuthorForm()

    return render(request, 'index/index.html' ,{'AuthorForm' : form,'check':False})

#-------------ADMIN------------------#
def super(request):
    return render(request, 'superuser/accountmanagement.html', {'users' : Acc.objects.all()})

def requestApproval(request):
    return render(request, 'superuser/AccountApproval.html', {'Acc': Acc.objects.all()})

def teamManagement(request):
    return render(request, 'superuser/TeamManagement.html', {'Acc': Acc.objects.all(),'Teams':Team.objects.all()})

def assignProject(request):
    return render(request, 'superuser/AssignProject.html', {'Acc': Acc.objects.all(),'Teams':Team.objects.all(), 'Projects':Project.objects.filter(team = None)})

def ProjectManagement(request):
    return render(request, 'superuser/ProjectManagement.html', {'Acc': Acc.objects.all(),'Projects': Project.objects.all()})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            author = User(username=form.cleaned_data['username'],password=form.cleaned_data.get('password'),first_name = form.cleaned_data['first_name'], last_name = form.cleaned_data['last_name'], email = form.cleaned_data['email'])

            try:
                if (User.objects.get(username = author.username)):
                    return render(request, 'index/Register.html',{'RegisterForm':form,'check':True})
            except:
                None
            author.save()
            newacc = Acc(user = author, valid = False, team = None)
            newacc.save()
            request.session['username'] = author.username
            request.session['seach'] = ''
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'index/Register.html' ,{'RegisterForm' : form,'check':False})



def viewProj(request,Project_id):
    try:
        proj = Project.objects.get(id = Project_id)
    except:
        proj = None

    if(proj is not None):
        if(request.method == "POST"):
            proj.specs = request.POST.get("SPECS")
            proj.stat = request.POST.get("STAT")
            proj.save()
        objectives = Objective.objects.filter(project = proj)
        totalPoints = Objective.objects.filter(project = proj).aggregate(Sum('points'))['points__sum']
        achievedPoints = Objective.objects.filter(project = proj, done = True).aggregate(Sum('points'))['points__sum']
        if(achievedPoints is None):
            achievedPoints = 0
        if(totalPoints is None):
            totalPoints = 0
            perc = 0
        else:
            perc = int((achievedPoints/totalPoints)*100)
        members = []
        if(proj.team is not None):
            members = Acc.objects.filter(team = proj.team)
        return render(request, 'superuser/ProjectView.html', {'proj':proj,'objectives': objectives,'TP':totalPoints,'AP':achievedPoints,'perc':perc, 'members':members})

    return render(request, 'superuser/ProjectManagement.html', {'Acc': Acc.objects.all(), 'Projects': Project.objects.all()})


#-----------AJAX METHODS-------------------#
def acceptu(request):

    if(request.method == "POST"):
        uname = request.POST['user']
        acc = Acc.objects.get(user__username = uname)
        acc.valid = True
        acc.save()
    return JsonResponse({'swag':'money'})
def rejectu(request):

    if(request.method == "POST"):
        uname = request.POST['user']
        acc = User.objects.get(username = uname)
        acc.delete()
    return JsonResponse({'swag':'money'})

def createp(request):
    idno = 9999
    if(request.method == "POST"):
        onames = request.POST.getlist('objectiveNames[]')
        opoints = request.POST.getlist('objectivePoints[]')
        proj = Project(name = request.POST.get("pname"), stat = "active")
        proj.save()
        idno = proj.id
        for i in range(0, len(onames)):
            quest = Objective(name = onames[i],points = opoints[i],done=False,project = proj)
            quest.save()
    print(idno)
    return JsonResponse({'name':request.POST.get("pname"),'id':idno})

def checkObject(request):
    if(request.method=="POST"):
        obj = Objective.objects.get(id = request.POST.get('id'))
        isdone = False
        if(request.POST.get('done') == 'true'):
            isdone = True
        obj.done = isdone
        obj.save()
    return JsonResponse({'done':'yes'})
def createt(request):
    name = ""
    id = 0
    if(request.method == "POST"):
        team = Team(name = request.POST.get("tname"))
        team.save()
        id = team.id
    return JsonResponse({'name':request.POST.get("tname"),'id':id})

def selectt(request):
    notlist = []
    yeslist = []
    tn = ""
    if(request.method == "POST"):
        leteam = Team.objects.get(id = int(request.POST.get("id")))
        tn = leteam.name
        for i in Acc.objects.filter(team =None):
            print('cool')
            addlist = []
            addlist.append(i.user.first_name +" "+i.user.last_name)
            addlist.append(i.id)
            notlist.append(addlist)
        for i in Acc.objects.exclude(team__isnull = True).exclude(team = leteam):
            print('cool')
            addlist = []
            addlist.append(i.user.first_name + " " + i.user.last_name)
            addlist.append(i.id)
            notlist.append(addlist)
        for i in Acc.objects.filter(team = leteam):
            addlist = []
            addlist.append(i.user.first_name + " " + i.user.last_name)
            addlist.append(i.id)
            yeslist.append(addlist)
    return JsonResponse({'id':request.POST.get("id"),'notlist':notlist,'yeslist':yeslist,'teamname':tn})

def joinrequest(request):
    if(request.method == "POST"):
        team = Team.objects.get(id = request.POST.get("teamid"));
        acc = Acc.objects.get(id = request.POST.get("id"))
        acc.team = team
        acc.save()
    return JsonResponse({'id': request.POST.get("id"),'name':acc.user.first_name})

def removerequest(request):
    if(request.method == "POST"):
        acc = Acc.objects.get(id = request.POST.get("id"))
        acc.team = None
        acc.save()
    return JsonResponse({'id': request.POST.get("id"),'name':acc.user.first_name})

def assignproj(request):
    if(request.method == "POST"):
        team = Team.objects.get(id = request.POST.get("teamid"))
        proj = Project.objects.get(id = request.POST.get("projid"))
        proj.team = team
        proj.save()
    return JsonResponse({'id': request.POST.get("projid")})