from ast import Pass
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from datetime import date

# Create your views here.
def index(request):
    if request.method == 'POST':

        form = PasswordForm(request.POST)
        

        if form.is_valid():
            password = form.cleaned_data['password']  
            request.session['password'] = password
            return redirect(join)
        else:
            print(form.errors)
            return render(request, 'groups/index.html', {'form':form})
    else:
        form = PasswordForm()
        return render(request, 'groups/index.html', {'form':form})

def create(request):
    if request.method == 'POST':
        form = CreatePartyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            join_deadline = form.cleaned_data['join_deadline']
            exchange_date = form.cleaned_data['exchange_date']
            spending_limit = form.cleaned_data['spending_limit']
            password = form.cleaned_data['password']
            party = Party(name=name, password=password, join_deadline=join_deadline, exchange_date=exchange_date, spending_limit=spending_limit)
            party.save()
            request.session['password'] = party.password
            return redirect(join)  
    else:
        form = CreatePartyForm().as_p
    
    return render(request, 'groups/create.html', {'form':form})


def join(request):
    try:
        party = Party.objects.get(password=request.session['password'])
    except:
        return redirect(index) #create a template for bad pwd request

    if(party.join_deadline < date.today()):
        return HttpResponse(party.password) #should create template for
    if request.method=='POST':
        santa_form = CreateSantaForm(request.POST)
        if santa_form.is_valid():
            first_name = santa_form.cleaned_data['first_name']
            last_name = santa_form.cleaned_data['last_name']
            email_address = santa_form.cleaned_data['email_address']
            santa = Santa(first_name = first_name, last_name=last_name, email_address=email_address, party=party)
            santa.save()
            return redirect(partyview, party_id=party.id)
        else:
            return redirect(nothanks)
    else:
        form = CreateSantaForm()
        return render(request, 'groups/join.html', {'form':form, 'party_name':party.name})


def partyview(request, party_id):
    try:
        party = Party.objects.get(pk=party_id)
    except Party.DoesNotExist:
        raise Http404("Party Does Not Exist")
    return render(request, 'groups/party_info.html', {'party': party})
 
def thanks(request):
    return HttpResponse('Thanks!')

def nothanks(request):
    return HttpResponse('No Thanks!')