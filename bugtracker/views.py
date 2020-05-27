from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django_bugtracker.settings import AUTH_USER_MODEL
from bugtracker.forms import NewCustomUser, LogInForm, SubmitTicket
from bugtracker.models import MyUser, Ticket
from django.template.defaultfilters import slugify


# Create your views here.
def index(request):
    html = "index.html" 
    filter_by = request.GET.get('filter_by', 'all')
    print(filter_by)
    if filter_by == "all":
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.all().filter(status=filter_by)
    order_by = request.GET.get('order_by', '-status')
    tickets = tickets.order_by(order_by)
    users = MyUser.objects.all()
    if request.user.is_authenticated:
        return render(request, html, {"tickets": tickets, "order_by": order_by, "users": users})
    return redirect("/login/")


def login_view(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data['username'],
                password=data['password']
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage')))

    form = LogInForm()
    return render(request, 'login_form.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))
        

def newuser_view(request):
    if request.method == 'POST':
        form = NewCustomUser(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            MyUser.objects.create(
                username=data['username'],
                password=data['password'],
                display_name=data['display_name'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email']
            )
            new_user = MyUser.objects.last()
            new_user.set_password(raw_password=data['password'])
            new_user.save()
            # login(request, new_user)
            content = "User successfully added"
            return HttpResponseRedirect(
                request.GET.get('next', reverse('homepage')), {'content': content})
        return render(request, "newuser_form.html", {"form": form})
    if request.user.is_authenticated:
        form = NewCustomUser()
        return render(request, "newuser_form.html", {"form": form})
    return redirect("/login/")


def submit_ticket_view(request):
    if request.method == "POST":
        form = SubmitTicket(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Ticket.objects.create(
                title=data['title'],
                description=data['description'],
                reported_by=request.user,
                status='New',
            )
            content = "Ticket successfully added"
            return HttpResponseRedirect(
                request.GET.get('next', reverse('homepage')), {'content: content'})
        return render(request, "submit_ticket_form.html", {"form": form})
    if request.user.is_authenticated:
        form = SubmitTicket()
        return render(request, "submit_ticket_form.html", {"form": form})
    return redirect("/login")
    

def ticket_detail(request, slug):
    if request.user.is_authenticated:
        ticket = Ticket.objects.get(slug=slug)
        return render(request, "ticket_detail.html", {"ticket": ticket})
    return redirect("/login")


def newuser_detail(request, pk):
    if request.user.is_authenticated:
        user = MyUser.objects.get(pk=pk)
        completed_tickets = Ticket.objects.filter(completed_by=user)
        assigned_tickets = Ticket.objects.filter(assigned_to=user)
        authored_tickets = Ticket.objects.filter(reported_by=user)
        return render(request, "newuser_detail.html", {
            "user": user,
            "completed_tickets": completed_tickets,
            "assign_tickets": assigned_tickets,
            "authored_tickets": authored_tickets
        })


def edit_ticket(request, slug):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = SubmitTicket(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                print(data)
                ticket = Ticket.objects.get(slug=slug)
                ticket.title = data['title']
                ticket.description = data['description']
                ticket.slug = slugify(ticket.title)
                ticket.save()
                return HttpResponseRedirect(
                            request.GET.get('next', reverse('homepage'))                              
                )

        old_ticket = Ticket.objects.get(slug=slug)
        form = SubmitTicket(initial={"title":old_ticket.title, "description":old_ticket.description})
        return render(request, "edit_ticket_form.html", {"form": form})
    return redirect("/login/")


def assign(request, slug):
    if request.user.is_authenticated:
        ticket = Ticket.objects.get(slug=slug)
        ticket.assigned_to = request.user
        ticket.status = "In Process"
        ticket.save()
        return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))                   
        )
    return redirect("/login/")

def done(request, slug):
    if request.user.is_authenticated:
        ticket = Ticket.objects.get(slug=slug)
        ticket.assigned_to = None
        ticket.completed_by = request.user
        ticket.completed_date = datetime.now()
        ticket.status = "Done"
        ticket.save()
        return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))                   
        )
    return redirect("/login/")   

def invalidate(request, slug):
    if request.user.is_authenticated:
        ticket = Ticket.objects.get(slug=slug)
        ticket.assigned_to = None
        ticket.completed_by = None
        ticket.status = "Invalid"
        ticket.save()
        return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))
        )
    return redirect("/login/")
