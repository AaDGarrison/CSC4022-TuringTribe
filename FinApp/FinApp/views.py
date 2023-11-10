"""
views.py

View methods for FinApp.
"""



# ----------------------------------------------------------------------------
# Django Imports
# ----------------------------------------------------------------------------

from json import dumps
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from Api.models import institution
import plaid
from plaid.api import plaid_api
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
from plaid.model.country_code import CountryCode
from dotenv import load_dotenv
import os
import datetime
# ----------------------------------------------------------------------------
# View Methods/Classes
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Signup
def verifyTransaction(client, institution_token, accountNum):
    plaidRequest = plaid_api.TransactionsGetRequest(
            access_token=institution_token,
            options=TransactionsGetRequestOptions(account_ids=[accountNum]),
            start_date= datetime.datetime.strptime('2020-03-25', '%Y-%m-%d').date(),
            end_date= datetime.datetime.strptime('2023-12-25', '%Y-%m-%d').date()
        )
    response = client.transactions_get(plaidRequest)
    transactions = response['transactions']
    if len(transactions)>0:
        return True
    else:
        return False

def verifyBalance(account):
    if account == None:
        return False
    AvailableBalance=account['balances']["available"]
    if AvailableBalance==None:
        return False
    return True

def setUpCards(RequestUser):
    load_dotenv()
    configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId' : os.getenv('client_ID'),
        'secret': os.getenv('SecretToken'),
    })
    api_client = plaid.ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)
    userInstituations= institution.objects.filter(user=RequestUser)
    cardData=[]
    cardCount=1
    for query in userInstituations:
        plaidRequest = plaid_api.AccountsGetRequest(access_token=query.access_token)
        response=client.accounts_get(plaidRequest)
        accounts=response["accounts"]
        for account in accounts:
            if verifyTransaction(client,query.access_token,account["account_id"]):
                cardData.append({"cardId":cardCount+1000,"instituion":query.institutionID,"accountNum":account["account_id"]})
            if verifyBalance(account):
                cardData.append({"cardId":cardCount+2000,"instituion":query.institutionID,"accountNum":account["account_id"]})
            cardCount+=1
    return cardData

def signupPage(request):

    message = ''
 
    if request.user.is_authenticated:
        return redirect('/dashboard')
     
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
 
        if form.is_valid():

            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('/dashboard')
         
        else:
            message = 'FAILURE TO REGISTER'
            return render(request,'registration/signup.html', {'form': form, 'message': message})
     
    else:

        form = UserCreationForm()
        return render(request,'registration/signup.html', {'form': form, 'message': message})

# ----------------------------------------------------------------------------
# Login
def loginPage(request):

    if request.user.is_authenticated:
        return redirect('/dashboard')

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        else:
            form = AuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        
    else:

        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

# ----------------------------------------------------------------------------
# Logout
@login_required(login_url='/')
def logoutPage(request):

    logout(request)
    return redirect('/')

# ----------------------------------------------------------------------------
# Dashboard
@login_required(login_url='/')
def dashboard(request):
    print("dashboard")
    CardList = request.session.get('CardData', None)
    if CardList==None:
        request.session["CardData"]=setUpCards(request.user)
        CardList = request.session.get('CardData', None)
    cardIds=[]
    for item in CardList:
        cardIds.append(item["cardId"])
    data = {
        "TotalCards":range(len(cardIds)), #dashboardCardCount.objects.get(user=request.user),
        "CardIDJSON": dumps(cardIds),
        "CardID": cardIds
    }

    return render(request, 'dashboard.html', {"data": data})

# ----------------------------------------------------------------------------
# Settings
@login_required(login_url='/')
def settings(request):
    try:    
        load_dotenv()
        configuration = plaid.Configuration(
        host=plaid.Environment.Sandbox,
        api_key={
            'clientId' : os.getenv('client_ID'),
            'secret': os.getenv('SecretToken'),
        })
        api_client = plaid.ApiClient(configuration)
        client = plaid_api.PlaidApi(api_client)
        userInstituations= institution.objects.filter(user=request.user)
        cardData=[]    
        institutionIDList=[]
        institutionNameList=[]
        cardCount=1
        for query in userInstituations:
            plaidRequest = plaid_api.AccountsGetRequest(access_token=query.access_token)
            response=client.accounts_get(plaidRequest)
            institutionId=response["item"]['institution_id']
            plaidRequest = InstitutionsGetByIdRequest(
                institution_id=institutionId,
                country_codes=[CountryCode("US")]
            )
            instResponse = client.institutions_get_by_id(plaidRequest)
            institutionName=instResponse["institution"]["name"]
            if institutionName != None: 
                institutionNameList.append(institutionName)
            else:
                institutionNameList.append("Unkown Institution Name")
            institutionIDList.append(institution.institutionID)
        data={
            "institutionName":institutionNameList,
            #"institutionID":institutionIDList,
            #"range":range(len(institutionIDList))
        }
        return render(request, 'settings.html', {"data": data})
    except:
        return render(request, 'settings.html', {"data": {"institutionName":[]}})
