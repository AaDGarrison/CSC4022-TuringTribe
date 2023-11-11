#IMPORT MODULES AND CLASSES
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
import plaid
from plaid.api import plaid_api
from plaid.model import products
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.accounts_get_request_options import AccountsGetRequestOptions
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from Api.models import institution
from dotenv import load_dotenv
import time
import datetime
from django.contrib.auth.decorators import login_required
import os

#LOAD VARIABLES FROM ENVIRONMENT FILE
load_dotenv()

#CONFIGURE PLAID API SETTINGS
configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId' : os.getenv('client_ID'),
        'secret': os.getenv('SecretToken'),
    }
)

#CREATE PLAID API CLIENT
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

#FUNCTION DEFINITION - RETRIEVE ACCOUNT INFORMATION
def getAccountinfo(request):
    """
    :Returns a plaid list of accounts with the cardId account num
    :param django request: request from a valid view
    """
    #RETRIEVE INPUT FROM SESSION
    CardList = request.session.get('CardData', None)
    RequestedcardID= request.GET.get('CardId')
    accountNum=""
    institution_token=""
    try:    
        #INPUT VALIDATION CHECK - CHECK IF CARDLIST EXISTS
        if CardList==None:
            raise
        #PROCESS - ITERATE THROUGH CARDLIST TO FIND MATCHING REQUESTED CARD    
        for item in CardList:
            if int(RequestedcardID)== item["cardId"]:
                accountNum=item["accountNum"]
                test=institution.objects.filter(institutionID=item["instituion"])
                institution_token=test[0].access_token
                
        #PROCESS - CREATE PLAID API REQUEST FOR ACCOUNT INFORMATION
        plaidRequest = plaid_api.AccountsGetRequest(
            access_token=institution_token,
            options=AccountsGetRequestOptions(account_ids=[accountNum])
        )

        #PROCESS - REQUEST
        PlaidResponse = client.accounts_get(plaidRequest)
        #OUTPUT - RESULT
        return PlaidResponse['accounts']
    except Exception as e:
        #EXCEPTION HANDLING: RAISE FLAG
        raise e



#FUNCTION DEFINITION - SEND CLIENT LINK REQUEST TO PLAID FOR SETUP
@login_required
def sendLinkRequest(request):  
    """
    HTTPS API request which returns a JOSN reposnse to allow a Link request to be estabilished

    :param str url: /api/send-link-request/.
    :param str method: 'GET'.
    :param dict headers: None.
    :param dict params: StartTime and StopTime in str formatted as YYYY-MM-DD.
    :param dict data: None.

    :return: Json response that is used with plaids account setup.
    :rtype: JOSN.Response
    :raises: requests.exceptions.RequestException if the request fails.
    """
    # go to https://dashboard.plaid.com/developers/api and add a redirect URL needs HTTPS
    try:    
        request = LinkTokenCreateRequest(
                products=[Products("auth")],
                client_name="Plaid Test App",
                country_codes=[CountryCode('US')],
                redirect_uri='https://localhost:3000/dashboard',
                language='en',
                user=LinkTokenCreateRequestUser(
                    client_user_id=str(time.time())
                )
            )
        response = client.link_token_create(request)
        return JsonResponse(response.to_dict())
    except:
         return JsonResponse({'Error': 'Failed'})
        
#FUNCTION DEFINITION - receive and setup a new pulic acess token and save to database
@login_required
def setupInstitution(request):
    """
    HTTPS API request which returns a JOSN reposnse of the accounts Transaction for a given start and stop date.

    :param str url: /api/setup-institution/.
    :param str method: 'POST'.
    :param dict headers: None.
    :param dict params: None.
    :param dict data: None.

    :return: Json .
    :rtype: JOSN.Response that verifies the successful creation of an new instituation.
    :raises: requests.exceptions.RequestException if the request fails.
    """
    #PROCESS - SETUP NEW INSTITUTION WITH PUBLIC TOKEN
    try:
        #INPUT VALIDATION - CHECK IF REQUEST METHOD IS POST
        if request.method != 'POST':
            return JsonResponse({'error': 'Invalid request method'}, status=405)
        #PROCESS - RETRIEVE PUBLIC TOKEN FROM THE POST REQUEST    
        link_public_token = request.POST.get('public_token')
        #AUTHENTICATION - EXCHANGE PUBLIC TOKEN FOR PRIVATE
        if link_public_token:
            exchange_request = plaid_api.ItemPublicTokenExchangeRequest(
                public_token= link_public_token
                )
            exchange_response = client.item_public_token_exchange(exchange_request)
            private_token=exchange_response['access_token']

            #PROCESS - institution name
            accountRequest = plaid_api.AccountsGetRequest(access_token=private_token)
            response=client.accounts_get(accountRequest)
            institutionId=response["item"]['institution_id']
            returnName=""
            plaidRequest = InstitutionsGetByIdRequest(
                institution_id=institutionId,
                country_codes=[CountryCode("US")]
            )
            instResponse = client.institutions_get_by_id(plaidRequest)
            institutionName=instResponse["institution"]["name"]
            if institutionName != None: 
                returnName=institutionName
            else:
                returnName="Unkown Institution Name"
            #PROCESS - SAVE THE NEW INSTITUTION TO DATABASE
            new_institution = institution(user=request.user, access_token=private_token)
            new_institution.save()

            #OUTPUT - RETURN SUCCESS JSON RESPONSE
            return JsonResponse({'Satus': 'Success',
                                 'Name': returnName
                                 })

    except:
         return JsonResponse({'Status': 'Failed'})

#FUNCTION DEFINITION - RETRIEVE TRANSACTIONS BASED ON ACCOUNT/DATE RANGE.
@login_required
def getTransactions(request):
    """
    HTTPS API request which returns a JOSN reposnse of the accounts Transaction for a given start and stop date.

    :param str url: /api/get-transactions/.
    :param str method: 'GET'.
    :param dict headers: None.
    :param dict params: StartTime and StopTime in str formatted as YYYY-MM-DD.
    :param dict data: None.

    :return: Json reposne with Transactio data for the request acounts.
    :rtype: JOSN.Response
    :raises: requests.exceptions.RequestException if the request fails.
    """
    #INPUT VALIDATION CHECK - CHECK IF THE REQUEST METHOD IS GET
    if request.method != 'GET':
        return HttpResponseBadRequest("Invalid request method")
    #PROCESS - RETRIEVE INPUT PARAMETERS FROM GET REQUEST    
    RequestedcardID= request.GET.get('CardId')
    start= request.GET.get('StartDate')
    end= request.GET.get('StopDate')
    
    accountNum=""
    institution_token=""
    try:    
        #PROCESS - RETRIEVE CARD INFORMATION FROM SESSION
        CardList = request.session.get('CardData', None)
        #INPUT VALIDATION CHECK - CHECK IF CARD EXISTS
        if CardList==None:
            raise
        #PROCESS - ITERATE THROUGH REQUESTED CARD 
        for item in CardList:
            if int(RequestedcardID)== item["cardId"]:
                accountNum=item["accountNum"]
                test=institution.objects.filter(institutionID=item["instituion"])
                institution_token=test[0].access_token
        #PROCESS - CREATE PLAID API REQUEST FOR ACCOUNT INFORMATION
        plaidRequest = plaid_api.TransactionsGetRequest(
            access_token=institution_token,
            options=TransactionsGetRequestOptions(account_ids=[accountNum]),
            start_date= datetime.datetime.strptime(start, '%Y-%m-%d').date(),
            end_date= datetime.datetime.strptime(end, '%Y-%m-%d').date()
        )
        #PROCESS - REQUEST
        response = client.transactions_get(plaidRequest)
        #DATA TRANSFORMATION - FORMAT TO BE USER READIBLE 
        transactions = response['transactions']
        transactionList=[]
        print(len(transactions))
        for transaction in transactions:
            source="Unkown"
            if transaction.merchant_name != None:
                source=transaction.merchant_name
        
            amount=0.0
            if transaction.amount>0:
                amount=-(transaction.amount)
            else:
                amount=abs(transaction.amount)

            transactionList.append({
                "merchant":source,
                "amount":amount,
                "date": transaction.date.strftime("%Y-%m-%d")    
            })
        #OUTPUT - RETURN THE FORMATTED TRANSACTION DATA AS A JSON RESPONSE    
        return JsonResponse(transactionList,safe=False)
    #EXCEPTION HANDLING - RAISE FLAG AND OUTPUT DESCRIPTION    
    except Exception as e:
        # Handle the exception
        return JsonResponse({'Error': 'Failed'})   

#FUNCTION DEFINITION - GET ACCOUNT BALANCE
@login_required
def getBalance(request):
    """
    HTTPS API request which returns a JOSN reposnse of the requested account balance

    :param str url: /api/get-balance/.
    :param str method: 'GET'.
    :param dict headers: None.
    :param dict params: StartTime and StopTime in str formatted as YYYY-MM-DD.
    :param dict data: None.

    :return: Json response with the account name and balance
    :rtype: JOSN.Response
    :raises: requests.exceptions.RequestException if the request fails.
    """
    try:
        #INPUT VALIDATION CHECK - CHECK IF THE REQUEST METHOD IS GET
        if(request.method!='GET'):
            return HttpResponseBadRequest("Invalid request method")
        #PROCESS - RETRIEVE ACCOUNT INFORMATION USING GETACCOUNTINFO FUNC()
        accounts=getAccountinfo(request)
        AvailableBalance=accounts[int(0)]['balances']["available"]
        AccountName=accounts[int(0)]['official_name']
        #DATA TRANSFORMATION - FORMAT TO BE USER READIBLE 
        if AvailableBalance== None:
            AvailableBalance="Not available"
        else:
            AvailableBalance="$"+str(AvailableBalance)
        return JsonResponse({"AccountName":AccountName,
                            "Balance":AvailableBalance })
    #EXCEPTION HANDLING - RAISE FLAG AND OUTPUT DESCRIPTION   
    except Exception as e:
        return JsonResponse({'Error': 'Failed'})

@login_required
def getCardName(request):
    """
    HTTPS API request which returns a JOSN reposnse of the requested account name

    :param str url: /api/get-card-name/.
    :param str method: 'GET'.
    :param dict headers: None.
    :param dict params: None.
    :param dict data: CardID

    :return: Json Response with CardName variable
    :rtype: JOSN.Response
    :raises: requests.exceptions.RequestException if the request fails.
    """
    
    try:
        #INPUT VALIDATION CHECK - CHECK IF THE REQUEST METHOD IS GET
        if(request.method!='GET'):
            return HttpResponseBadRequest("Invalid request method")
        #PROCESS - RETRIEVE INPUT PARAMETERS FROM GET REQUEST  
        RequestedcardID= request.GET.get('CardId')
        #PROCESS - RETRIEVE ACCOUNT INFORMATION USING GETACCOUNTINFO FUNC()
        accounts=getAccountinfo(request)
        accountName=accounts[0]["name"]
        #PROCESS - APPEND ADDITIONAL INFO BASED ON CARDID
        if int(RequestedcardID) >=1000 and int(RequestedcardID)<2000:
            accountName+=" Transactions"
        elif int(RequestedcardID) >=2000 and int(RequestedcardID)<3000:
            accountName+=" Balance"
        #DATA TRANSFORMATION - FORMAT TO BE USER READIBLE 
        return JsonResponse({"CardName":accountName})
    #EXCEPTION HANDLING - RAISE FLAG AND OUTPUT DESCRIPTION   
    except Exception as e:
        # Handle the exception
        return JsonResponse({'Error': 'Failed'})
