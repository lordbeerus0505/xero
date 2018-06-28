import json, uuid
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.conf import settings
import datetime
import webbrowser
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from yellowant import YellowAnt


from .models import YellowAntRedirectState, UserIntegration, Xero_Credentials
from ..yellowant_command_center.command_center import CommandCenter
from xero.auth import PublicCredentials
from xero import Xero
import time
integ_id=0
saved_state={}
customer_key=''
customer_secret=''
token=0

def xero_return(request):
    global token
    print("hellolololol")
    print("REQUEST"+str(request))
    print("Inside xero_return")
    token=request.GET.get("oauth_verifier")
    #state=request.GET.get("state")
    print(str(token) + 'code')
    customer_key='BGJJ6JSSEAGIRWQ9SYKA1T3O7Y6IPF'
    customer_secret='2JRHWN0QQ1K0AHVDZVUPKCVIQKUUNB'
    # oauth2URL = 'https://app.box.com/api/oauth2/token'
    # apiURL = 'https://api.box.com/2.0/'
    # authorizationCode = code
    #generateTokens(clientId,clientSecret,oauth2URL,apiURL,authorizationCode)
    return HttpResponseRedirect("/")

def request_yellowant_oauth_code(request):
    """Initiate the creation of a new user integration on YA
    
    YA uses oauth2 as its authorization framework. This method requests for an oauth2 code from YA to start creating a 
    new user integration for this application on YA.
    """
    # get the user requesting to create a new YA integration
    print(str(request.user.id)+"req")
    user = User.objects.get(id=request.user.id)
    print("Hello\n\n")
    # generate a unique ID to identify the user when YA returns an oauth2 code
    state = str(uuid.uuid4())
    print(state)

    # save the relation between user and state so that we can identify the user when YA returns the oauth2 code
    YellowAntRedirectState.objects.create(user=user.id, state=state)

    # Redirect the application user to the YA authentication page. Note that we are passing state, this app's client id,
    # oauth response type as code, and the url to return the oauth2 code at.
    return HttpResponseRedirect("{}?state={}&client_id={}&response_type=code&redirect_url={}".format(
        settings.YA_OAUTH_URL, state, settings.YA_CLIENT_ID, settings.YA_REDIRECT_URL))


def yellowant_oauth_redirect(request):
    """Receive the oauth2 code from YA to generate a new user integration
    
    This method calls utilizes the YA Python SDK to create a new user integration on YA.
    This method only provides the code for creating a new user integration on YA. Beyond that, you might need to 
    authenticate the user on the actual application (whose APIs this application will be calling) and store a relation
    between these user auth details and the YA user integration.
    """
    # oauth2 code from YA, passed as GET params in the url
    print('inside yellowant_oauth_redirect')
    code = request.GET.get("code")
    print(code)

    print("Hello\n\n")

    # the unique string to identify the user for which we will create an integration
    state = request.GET.get("state")
    print("statis is")
    print(state)
    # fetch user with the help of state
    yellowant_redirect_state = YellowAntRedirectState.objects.get(state=state)
    user = yellowant_redirect_state.user
    print("user is")
    print(user)

    # initialize the YA SDK client with your application credentials
    ya_client = YellowAnt(app_key=settings.YA_CLIENT_ID, app_secret=settings.YA_CLIENT_SECRET, access_token=None,
        redirect_uri=settings.YA_REDIRECT_URL)


    # get the access token for a user integration from YA against the code
    print ("here")
    access_token_dict = ya_client.get_access_token(code)
    print(str(access_token_dict)+" Accesstoken")
    print("Inside \n\n")
    access_token = access_token_dict["access_token"]

    # reinitialize the YA SDK client with the user integration access token
    ya_client = YellowAnt(access_token=access_token)

    # get YA user details
    ya_user = ya_client.get_user_profile()

    # create a new user integration for your application
    user_integration = ya_client.create_user_integration()

    # save the YA user integration details in your database
    ut=UserIntegration.objects.create(user=user, yellowant_user_id=ya_user["id"],
        yellowant_team_subdomain=ya_user["team"]["domain_name"],
        yellowant_integration_id=user_integration["user_application"],
        yellowant_integration_invoke_name=user_integration["user_invoke_name"],
        yellowant_integration_token=access_token)

    Xero_Credentials.objects.create(user_integration=ut,XERO_OAUTH_SECRET='0',XERO_OAUTH_TOKEN='0',XERO_EXPIRE='0',XERO_AUTH_EXPIRE='0' ,XERO_UPDATE_LOGIN_FLAG=False)
    
    # A new YA user integration has been created and the details have been successfully saved in your application's 
    # database. However, we have only created an integration on YA. As a developer, you need to begin an authentication 
    # process for the actual application, whose API this application is connecting to. Once, the authentication process 
    # for the actual application is completed with the user, you need to create a db entry which relates the YA user
    # integration, we just created, with the actual application authentication details of the user. This application
    # will then be able to identify the actual application accounts corresponding to each YA user integration.
    # return HttpResponseRedirect("to the actual application authentication URL")

    print(str(user_integration["user_application"])+"  integration ID")


    global integ_id
    global saved_state
    global token
    integ_id= UserIntegration.objects.get(yellowant_integration_id=user_integration["user_application"])


    #-------------------------------------------------------------------------------------------------
    credentials=PublicCredentials('BGJJ6JSSEAGIRWQ9SYKA1T3O7Y6IPF','2JRHWN0QQ1K0AHVDZVUPKCVIQKUUNB','http://127.0.0.1:8000/return/')
    print(credentials.url)
    webbrowser.open(credentials.url)
    time.sleep(15)
    #time.sleep(60) for the user
    credentials.verify(token)
    xero=Xero(credentials)
    saved_state=credentials.state
    print(str(saved_state)+"saved_state")
    s1=saved_state['oauth_expires_at']
    s2=saved_state['oauth_authorization_expires_at']
    print("\n\n")
    print(s1)
    print(s2)
    s1=s1.strftime('%Y%m%d%H%M%S%f')
    s2=s2.strftime('%Y%m%d%H%M%S%f')
    #new_date=datetime.datetime.strptime(s1,'%Y%m%d%H%M%S%f')
    #print(new_date)
    t1=saved_state['oauth_token']
    t2=saved_state['oauth_token_secret']
    obj=Xero_Credentials.objects.get(user_integration_id=integ_id.id)
    obj.XERO_OAUTH_TOKEN=t1
    obj.XERO_OAUTH_SECRET=t2
    obj.XERO_EXPIRE=s1
    obj.XERO_AUTH_EXPIRE=s2
    obj.XERO_UPDATE_LOGIN_FLAG=True
    print(str(obj.XERO_AUTH_EXPIRE)+"  helloooo")
    obj.save()

    new_credentials=PublicCredentials(**saved_state)
    xero=Xero(new_credentials)
    print("successful authentication")


    return HttpResponseRedirect("/")
    #-------------------------------------------------------------------------------------------
    #reverse ('/')


@csrf_exempt
def yellowant_api(request):
    """Receive user commands from YA"""
    data = json.loads(request.POST.get("data"))
    print("Inside yellowant_api")
    #print(data)

    # verify whether the request is genuinely from YA with the help of the verification token
    if data["verification_token"] != settings.YA_VERIFICATION_TOKEN:
        return HttpResponseNotAllowed("Insufficient permissions.")
    
    # check whether the request is a user command, or a webhook subscription notice from YA
    if data["event_type"] == "command":
        # request is a user command
        #print("Command")
        # retrieve the user integration id to identify the user
        yellowant_integration_id = data.get("application")

        # invoke name of the command being called by the user
        command_name = data.get("function_name")

        # any arguments that might be present as an input for the command
        args = data.get("args")

        # create a YA Message object with the help of the YA SDK
        message = CommandCenter(yellowant_integration_id, command_name, args).parse()

        # return YA Message object back to YA
        return HttpResponse(message)
    elif data["event_type"] == "webhook_subscription":
        # request is a webhook subscription notice
        pass



#------------------------------------------------------------------------------------------------------------------------


@csrf_exempt
def api_key(request):
    """An object is created in the database using the request."""
    print("Inside api_key")
    data = json.loads(request.body)



    try:
        #print(1)
        abc=Xero_Credentials()
        x=data['user_integration']
        print(x)
        aby = Xero_Credentials.objects.get(user_integration_id=int(data["user_integration"]))
        print(2)
        aby.XERO_CONSUMER_KEY = data['XERO_CONSUMER_KEY']
        print("Consumer key="+aby.XERO_CONSUMER_KEY)
        aby.XERO_CONSUMER_SECRET = data['XERO_CONSUMER_SECRET']
        #print(4)
        #aby.AGILE_DOMAIN_NAME = data['AGILE_DOMAIN_NAME']
        # aby.AZURE_client_secret = data['AZURE_client_secret']
        aby.XERO_UPDATE_LOGIN_FLAG = True

        print("Hello"+aby.XERO_CONSUMER_KEY + "  " + aby.XERO_CONSUMER_SECRET + "  " )
        aby.save()
    except:
        return HttpResponse("Invalid credentials. Please try again")


    # else:
    #     #aby = Agile_Credentials.objects.get(user_integration_id=int(data["user_integration_id"]))
    #     aby=Agile_Credentials()
    #     aby.AGILE_API_KEY = data['AGILE_API_KEY']
    #     aby.AGILE_EMAIL_ID = data['AGILE_EMAIL_ID']
    #     aby.AGILE_DOMAIN_NAME = data['AGILE_DOMAIN_NAME']
    #     #aby.AZURE_client_secret = data['AZURE_client_secret']
    #     aby.AGILE_UPDATE_LOGIN_FLAG = True
    #     print(aby.AGILE_API_KEY + "  " + aby.AGILE_DOMAIN_NAME + "  " + aby.AGILE_EMAIL_ID)
    #     aby.save()


    return HttpResponse("Success", status=200)


# def get_credentials(tenant, client, subs, secret):
#     """Function to get credentials of the AZURE account"""
#     subscription_id = subs
#     credentials = ServicePrincipalCredentials(
#         client_id=client,
#         secret=secret,
#         tenant=tenant
#     )
#     return credentials, subscription_id
