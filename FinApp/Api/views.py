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
import time
import datetime
import json
from dotenv import load_dotenv
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
    HTTP API request which returns a JOSN reposnse to allow a Link request to be estabilished

    :param str url: /api/send-link-request/.
    :param str method: 'GET'.
    :param dict headers: None.
    :param dict params: StartTime and StopTime in str formatted as YYYY-MM-DD.
    :param dict data: None.

    :return: Json response that is used with plaids account setup.
    :rtype: JOSN.Response
    :raises: requests.exceptions.RequestException if the request fails.
    """
    ## go to https://dashboard.plaid.com/developers/api and add a redirect URL needs HTTPS
    # request = LinkTokenCreateRequest(
    #         products=[Products("auth")],
    #         client_name="Plaid Test App",
    #         country_codes=[CountryCode('US')],
    #         redirect_uri='http://localhost:3000/',
    #         language='en',
    #         user=LinkTokenCreateRequestUser(
    #             client_user_id=str(time.time())
    #         )
    #     )
    # response = client.link_token_create(request)
    # return JsonResponse(response.to_dict())
    return JsonResponse({"not Ready":"Needs HTTPS"})
#receive and setup a new pulic acess token and save to database
def setupInstitution(request):
    """
    HTTP API request which returns a JOSN reposnse of the accounts Transaction for a given start and stop date.

    :param str url: /api/setup-institution/.
    :param str method: 'POST'.
    :param dict headers: None.
    :param dict params: None.
    :param dict data: None.

    :return: Json .
    :rtype: JOSN.Response that verifies the successful creation of an new instituation.
    :raises: requests.exceptions.RequestException if the request fails.
    """
    if(request.method=='POST'):
        response_data = {
            'message': 'Institution succesufully setup.'
        }
        return JsonResponse(response_data, status=201)
    else:
        # Return a Bad Request response for invalid HTTP method
        return HttpResponseBadRequest("Invalid request method")

def getTransactions(request):
    """
    HTTP API request which returns a JOSN reposnse of the accounts Transaction for a given start and stop date.

    :param str url: /api/get-transactions/.
    :param str method: 'GET'.
    :param dict headers: None.
    :param dict params: StartTime and StopTime in str formatted as YYYY-MM-DD.
    :param dict data: None.

    :return: Json reposne with Transactio data for the request acounts.
    :rtype: JOSN.Response
    :raises: requests.exceptions.RequestException if the request fails.
    """
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
    return HttpResponse(transactions,content_type='application/json')

def getBalance(request):
    """
    HTTP API request which returns a JOSN reposnse of the requested account balance

    :param str url: /api/get-balance/.
    :param str method: 'GET'.
    :param dict headers: None.
    :param dict params: StartTime and StopTime in str formatted as YYYY-MM-DD.
    :param dict data: None.

    :return: Json response with the account name and balance
    :rtype: JOSN.Response
    :raises: requests.exceptions.RequestException if the request fails.
    """
    Account = request.headers['account']
    request = plaid_api.AccountsGetRequest(access_token=private_token)
    response = client.accounts_get(request)
    accounts = response['accounts']
    AvailableBalance=accounts[int(Account)]['balances']['available']
    AccountName=accounts[int(Account)]['official_name']
    return JsonResponse({"AccountName":AccountName,
                         "Balance":AvailableBalance })