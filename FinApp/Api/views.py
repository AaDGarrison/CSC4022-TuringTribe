from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
import plaid
from plaid.api import plaid_api
from plaid.model import products
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from dotenv import load_dotenv
import time
import datetime
from django.contrib.auth.decorators import login_required
import os
load_dotenv()
configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId' : os.getenv('client_ID'),
        'secret': os.getenv('SecretToken'),
    }
)
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

pt_request = plaid_api.SandboxPublicTokenCreateRequest(
    institution_id="ins_109511",
    initial_products=[products.Products('transactions')]
)

pt_response = client.sandbox_public_token_create(pt_request)
# The generated public_token can now be
# exchanged for an access_token
exchange_request = plaid_api.ItemPublicTokenExchangeRequest(
    public_token=pt_response['public_token']
)
exchange_response = client.item_public_token_exchange(exchange_request)
private_token=exchange_response['access_token']

#Send the client a link to setup Plaid institution
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
    #return JsonResponse({"not Ready":"Needs HTTPS"})
#receive and setup a new pulic acess token and save to database
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
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    public_token = request.POST.get('public_token')
    if public_token:
        exchange_request = plaid_api.ItemPublicTokenExchangeRequest(
            public_token=pt_response['public_token']
            )
        exchange_response = client.item_public_token_exchange(exchange_request)
        private_token=exchange_response['access_token']
        
        # You should have a model for storing access tokens.
        # Replace AccessToken with your actual model.
        #access_token = AccessToken(public_token=public_token)
        #access_token.save()
        print(private_token)
        return JsonResponse({'public_token_exchange': 'complete'})


    

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
    if request.method != 'GET':
        return HttpResponseBadRequest("Invalid request method")
    start= request.GET.get('StartDate')
    end= request.GET.get('StopDate')
        
    plaidRequest = plaid_api.TransactionsGetRequest(
        access_token=private_token,
        #options=TransactionsGetRequestOptions(account_ids=['4WrXeaQZL3iJmxyNBa7xCyqXrQEbDnHJznx3n']),
        start_date= datetime.datetime.strptime(start, '%Y-%m-%d').date(),
        end_date= datetime.datetime.strptime(end, '%Y-%m-%d').date()
    )
    response = client.transactions_get(plaidRequest)
    transactions = response['transactions']
    transactionList=[]
    for item in transactions:
        source="Unkown"
        if item.merchant_name != None:
            source=item.merchant_name
        
        amount=0.0
        if item.amount>0:
            amount=-(item.amount)
        else:
            amount=abs(item.amount)

        transactionList.append({
            "merchant":source,
            "amount":amount,
            "date": item.date.strftime("%Y-%m-%d")
            
        })
    return JsonResponse(transactionList,safe=False)

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

    if(request.method!='GET'):
        return HttpResponseBadRequest("Invalid request method")

    Account = 0
    request = plaid_api.AccountsGetRequest(access_token=private_token)
    response = client.accounts_get(request)
    accounts = response['accounts']
    AvailableBalance=accounts[int(Account)]['balances']['available']
    AccountName=accounts[int(Account)]['official_name']
    return JsonResponse({"AccountName":AccountName,
                         "Balance":AvailableBalance })

def getCardName(request):
    if(request.method!='GET'):
        return HttpResponseBadRequest("Invalid request method")
    #add functions to get he account name for all accounts using the database
    cardID= request.GET.get('CardId')
    accountName="TestName:"+cardID
    return JsonResponse({"CardName":accountName})