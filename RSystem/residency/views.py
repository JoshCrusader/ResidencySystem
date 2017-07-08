from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.utils import timezone
from .forms import AuthorForm,RegisterForm
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import User

from django.http import JsonResponse

from django.template import RequestContext

from django.db.models import Q
from django.contrib.auth.hashers import make_password

from django.http import HttpResponse
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
                author = authenticate(username = str(form.cleaned_data['username']),password=form.cleaned_data.get('password'))
                print(author)
                logg = login(request,author)
                if(request.user.is_authenticated()):
                    if (request.user.has_perm('poll.change_poll')):
                        return redirect('superuser')
                    elif(Acc.objects.get(user = request.user).valid ==False):
                        return redirect("errorlogin")
                    else:
                        request.session["userid"] = Acc.objects.get(user = request.user).id
                        request.session["startdate"] = str(timezone.now())
                        newdate = resident(acc = Acc.objects.get(user = request.user), cdate = request.session["startdate"])
                        newdate.save()
                        return redirect('homepage')

            except:
                return render(request, 'index/index.html', {'AuthorForm': form, 'check': True})
    else:
        form = AuthorForm()

    return render(request, 'index/index.html' ,{'AuthorForm' : form,'check':False})
def XD(request):
    return render(request, 'index/errorr.html')
def XD2(request):
    return render(request, 'index/errorr2.html')
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            author = User(username=form.cleaned_data['username'],password=make_password(form.cleaned_data.get('password')),first_name = form.cleaned_data['first_name'], last_name = form.cleaned_data['last_name'], email = form.cleaned_data['email'])

            try:
                if (User.objects.get(username = author.username)):
                    request.Session()
                    return render(request, 'index/Register.html',{'RegisterForm':form,'check':True})
            except:
                None
            author.save()
            newacc = Acc(user = author, valid = False, team = None)
            newacc.save()
            request.session['username'] = author.username
            request.session['seach'] = ''
            return redirect("errorlogin")
    else:
        form = RegisterForm()
    return render(request, 'index/Register.html' ,{'RegisterForm' : form,'check':False})

def checkadmin(request):
    if (request.user.is_authenticated() == True):
        print(request.user.has_perm('poll.change_poll') == False)
        if (request.user.has_perm('poll.change_poll') == False):
            return False
    else:
        return False
    return True

def checkuser(request):
    if (request.user.is_authenticated() == False):
            return "0"
    else:
        acc = Acc.objects.get(user = request.user)
        if(acc.valid == True):
            return "1"
        else:
            return "2"
#-------------ADMIN------------------#
def super(request):
    if(checkadmin(request) == False):
        return redirect("idontacceptu")
    return render(request, 'superuser/accountmanagement.html', {'users' : Acc.objects.all()})

def requestApproval(request):
    if (checkadmin(request) == False):
        return redirect("idontacceptu")
    return render(request, 'superuser/AccountApproval.html', {'Acc': Acc.objects.all()})

def teamManagement(request):
    if (checkadmin(request) == False):
        return redirect("idontacceptu")
    return render(request, 'superuser/TeamManagement.html', {'Acc': Acc.objects.filter(valid = True),'Teams':Team.objects.all()})

def assignProject(request):
    if (checkadmin(request) == False):
        return redirect("idontacceptu")
    return render(request, 'superuser/AssignProject.html', {'Acc': Acc.objects.all(),'Teams':Team.objects.all(), 'Projects':Project.objects.filter(team = None)})

def ProjectManagement(request):
    if (checkadmin(request) == False):
        return redirect("idontacceptu")
    return render(request, 'superuser/ProjectManagement.html', {'Acc': Acc.objects.all(),'Projects': Project.objects.all()})




def viewProj(request,Project_id):
    if (checkadmin(request) == False):
        return redirect("idontacceptu")
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

def cubehw(request):
    if (checkadmin(request) == False):
        return redirect("idontacceptu")
    return render(request, 'superuser/CubicleAssignment.html', {'Acc': Acc.objects.filter(valid = True),'Teams':Team.objects.all()})

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
        for i in Acc.objects.filter(team =None).filter(valid = True):
            print('cool')
            addlist = []
            addlist.append(i.user.first_name +" "+i.user.last_name)
            addlist.append(i.id)
            notlist.append(addlist)
        for i in Acc.objects.exclude(team__isnull = True).exclude(team = leteam).filter(valid = True):
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
    return JsonResponse({'id': request.POST.get("id"),'name':(acc.user.first_name+" "+acc.user.last_name)})

def removerequest(request):
    if(request.method == "POST"):
        acc = Acc.objects.get(id = request.POST.get("id"))
        acc.team = None
        acc.save()
    return JsonResponse({'id': request.POST.get("id"),'name':(acc.user.first_name+" "+acc.user.last_name)})

def assignproj(request):
    if(request.method == "POST"):
        team = Team.objects.get(id = request.POST.get("teamid"))
        proj = Project.objects.get(id = request.POST.get("projid"))
        proj.team = team
        proj.save()
    return JsonResponse({'id': request.POST.get("projid")})

def selectc(request):
    yeslist = []
    countlist = []
    tn = ""
    times = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    cuname = "cubicle"
    if(request.method == "POST"):
        leteam = Team.objects.get(id = int(request.POST.get("id")))
        otherScheds = teamSched.objects.filter(team__cubes=leteam.cubes)
        tn = leteam.name
        cuname = leteam.cubes
        for i in otherScheds:
            day = i.day
            if("07:30" >= i.start and "07:30" <= i.end or "09:00" >= i.start and "09:00" <= i.end):
                times[0][day-1] = times[0][day-1] + 1
            if ("09:15" >= i.start and "09:15" <= i.end or "10:45" >= i.start and "10:45" <= i.end):
                times[1][day - 1] = times[1][day - 1] + 1
            if ("11:00" >= i.start and "11:00" <= i.end or "12:30" >= i.start and "12:30" <= i.end):
                times[2][day - 1] = times[2][day - 1] + 1
            if ("12:45" >= i.start and "12:45" <= i.end or "14:15" >= i.start and "14:15" <= i.end):
                times[3][day - 1] = times[3][day - 1] + 1
            if ("14:30" >= i.start and "14:30" <= i.end or "16:00" >= i.start and "16:00" <= i.end):
                times[4][day - 1] = times[4][day - 1] + 1
            if ("16:15" >= i.start and "16:15" <= i.end or "17:45" >= i.start and "17:45" <= i.end):
                times[5][day - 1] = times[5][day - 1] + 1
            start1,end1 = i.start.split(":")
            start2,end2 = i.end.split(":")

        for i in teamSched.objects.filter(team = leteam):
            addlist = []
            addlist.append(i.day)
            addlist.append(i.start)
            addlist.append(i.end)
            yeslist.append(addlist)

    return JsonResponse({'id':request.POST.get("id"),'yeslist':yeslist,'teamname':tn,'cubes':times, 'cuname':cuname})

def change_cub(request):
    if (request.method == "POST"):
        leteam = Team.objects.get(id=int(request.POST.get("id")))
        leteam.cubes = request.POST.get("cub")
        leteam.save()
    return JsonResponse({"None":"None"})
#------- USER METHODS------#
def home(request):

    if(request.user.is_authenticated()):
        user = request.user
        myAcc = Acc.objects.get(user = user)
        leteam = myAcc.team
        projs = Project.objects.filter(team = leteam)
        listofprojs = []
        listofall = []
        for i in projs:
            templist = []
            listofprojs.append(i)
            objectives = Objective.objects.filter(project=i)
            totalPoints = Objective.objects.filter(project=i).aggregate(Sum('points'))['points__sum']
            achievedPoints = Objective.objects.filter(project=i, done=True).aggregate(Sum('points'))['points__sum']
            if (achievedPoints is None):
                achievedPoints = 0
            if (totalPoints is None):
                totalPoints = 0
                perc = 0
            else:
                perc = int((achievedPoints / totalPoints) * 100)
            templist.append(i)
            templist.append(totalPoints)
            templist.append(achievedPoints)
            templist.append(perc)
            listofall.append(templist)
        objs = Objective.objects.filter(project__in = listofprojs)
        return render(request, 'normuser/UserDashboard.html',{'me':user,'myacc':myAcc,'leteam':leteam,'projects':projs,'objectives':objs,'allProjects':listofall})

    else:
        return redirect('index')

def myproj(request, Project_id):
    print('lolXD')
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
        members2 = []
        for i in members:
            empty = []
            empty.append(i)
            try:
                role = Role.objects.get(acc = i, proj = proj)
                role_title = role.content
                if(role_title == ""):
                    role_title = "None"
            except:
                role = Role(acc=i, proj=proj)
                role_title = "None"
            empty.append(role_title)
            members2.append(empty)
        acc = Acc.objects.get(user = request.user)
        myprog = Progress.objects.filter(project = proj)
        return render(request, 'normuser/ViewProject.html', {'me':request.user,'proj':proj,'objectives': objectives,'TP':totalPoints,'AP':achievedPoints,'perc':perc, 'members':members2,'account':acc, 'myprogs':myprog})

    return render(request, 'normuser/ViewProject.html', {'me':request.user,'Acc': Acc.objects.all(), 'Projects': Project.objects.all()})

def ManageSched(request):
    acc = Acc.objects.get(user = request.user)
    scheds = teamSched.objects.filter(team = acc.team)
    print(len(scheds))
    return render(request, 'normuser/ManageSched.html', {'me': request.user,'scheds':scheds})


#------AJAX USER METHODS ----#
def addprogress(request):

    if(request.method == "POST"):
        print("XD")
        leid = request.POST.get("myId")
        leprojid = request.POST.get("projid")
        leprog = request.POST.get("prog_content")
        print(leprojid)
        leproj = Project.objects.get(id=leprojid)
        leacc = Acc.objects.get(id=leid)
        leuser = leacc.user
        prog = Progress(value = leprog, cdate = timezone.now(),user = leuser, project = leproj)
        prog.save()
        return JsonResponse({'content': request.POST.get("prog_content"),'name':(leacc.user.first_name)})
    return JsonResponse({'None': 'None'})

def changerole(request):
    if(request.method == "POST"):

        leid = request.POST.get("myId")
        acc = Acc.objects.get(id = leid)
        leprojid = request.POST.get("projid")
        proj = Project.objects.get(id = leprojid)
        try:
            role = Role.objects.get(acc = acc, proj = proj)
        except:
            role = Role(acc = acc, proj = proj)
        content = request.POST.get("content")
        role.content = content
        role.save()
    return JsonResponse({'None': 'None'})

def addsched(request):
    if(request.method == "POST"):
        user = request.user
        acc = Acc.objects.get(user = user)

        sched = teamSched(team = acc.team,day = request.POST.get("day"), start = request.POST.get("sched1"), end = request.POST.get("sched2"))
        sched.save()
    return JsonResponse({'None': 'None'})
def user_cub(request):
    times = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    if(request.method == "POST"):
        otherScheds = teamSched.objects.filter(team__cubes=request.POST.get("cubicle"))
        for i in otherScheds:
            day = i.day
            if("07:30" >= i.start and "07:30" <= i.end or "09:00" >= i.start and "09:00" <= i.end):
                times[0][day-1] = times[0][day-1] + 1
            if ("09:15" >= i.start and "09:15" <= i.end or "10:45" >= i.start and "10:45" <= i.end):
                times[1][day - 1] = times[1][day - 1] + 1
            if ("11:00" >= i.start and "11:00" <= i.end or "12:30" >= i.start and "12:30" <= i.end):
                times[2][day - 1] = times[2][day - 1] + 1
            if ("12:45" >= i.start and "12:45" <= i.end or "14:15" >= i.start and "14:15" <= i.end):
                times[3][day - 1] = times[3][day - 1] + 1
            if ("14:30" >= i.start and "14:30" <= i.end or "16:00" >= i.start and "16:00" <= i.end):
                times[4][day - 1] = times[4][day - 1] + 1
            if ("16:15" >= i.start and "16:15" <= i.end or "17:45" >= i.start and "17:45" <= i.end):
                times[5][day - 1] = times[5][day - 1] + 1


    return JsonResponse({'id':request.POST.get("id"),'cubes':times, 'cuname':request.POST.get("cubicle")})

def request_logout(request):
    if(request.method == "POST"):
        acc = Acc.objects.get(user = request.user )
        res = resident.objects.get(acc = acc, cdate = request.session["startdate"])
        if((timezone.now() - res.cdate).seconds//3600 <= 4):
            res.edate = timezone.now()
            res.save()
        else:
            res.delete()
