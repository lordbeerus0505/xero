"""Code which actually takes care of application API calls or other business logic"""


from yellowant.messageformat import MessageClass , MessageAttachmentsClass, AttachmentFieldsClass

from yellowant_xero_app import settings
from ..yellowant_message_builder.messages import items_message, item_message
import requests
import json
from ..yellowant_command_center.unix_epoch_time import convert_to_epoch
from urllib.parse import urljoin
from ..yellowant_command_center import command_center
from ..yellowant_api.models import Xero_Credentials,UserIntegration
from ..yellowant_api import views
import ast
import webbrowser
import time
import datetime


from django.http import HttpResponse
from xero.auth import PublicCredentials
from xero import Xero
import requests

from django.http import HttpResponse
import requests
#


flag=1

#-------------------------------------------------------CONTACTS--------------------------------------------------------------------

#--------------------------------------------------------Retrieve all contacts-------------------------------------------------------

def list_contacts(args,user_integration):
    xcr = Xero_Credentials.objects.get(user_integration_id=user_integration.id)
    token=xcr.XERO_OAUTH_TOKEN
    secret=xcr.XERO_OAUTH_SECRET
    expire=xcr.XERO_EXPIRE
    auth=xcr.XERO_AUTH_EXPIRE
    fmt = '%Y%m%d%H%M%S%f'
    expire = datetime.datetime.strptime(expire, fmt)
    auth=datetime.datetime.strptime(auth, fmt)


    print("user integration-" + str(xcr.user_integration_id))
    print(expire)

    saved_state={'consumer_key': 'BGJJ6JSSEAGIRWQ9SYKA1T3O7Y6IPF',
                 'consumer_secret': '2JRHWN0QQ1K0AHVDZVUPKCVIQKUUNB',
                 'callback_uri': 'http://127.0.0.1:8000/return/',
                 'verified': True,
                 'oauth_token': token,
                 'oauth_token_secret': secret,
                 'oauth_expires_at': expire,
                 'oauth_authorization_expires_at': auth
                 }




    print(saved_state)

    #xero = Xero(credentials)

    #state=xcr.XERO_STATE
    #state=ast.literal_eval(state[0])
    print("HELLO")
    new_credentials = PublicCredentials(**saved_state)
    print(new_credentials.state)
    xero = Xero(new_credentials)
    #print(new_credentials.state)
    #print(xero.contacts.all())
    x=''
    s=xero.contacts.all()
    for i in s:
        #print(i)
        print("CompanyName: " + i['Name'] + "\nFirst Name: " + i['FirstName'], " Last Name:",
              i['LastName'] + " \nEmail Address: " + i['EmailAddress'] + "  \nStreet Address: " +
              i['Addresses'][1]['AddressLine1'] + ", " + i['Addresses'][1]['AddressLine2'] + ", " + i['Addresses'][1][
                  'AddressLine3'] + "\n," + i['Addresses'][1]['City'] + ", " + i['Addresses'][1]['Region'] + ", " +
              i['Addresses'][1]['Country'], i['Addresses'][1]['PostalCode'] + "\nPhone: " +
              i['Phones'][1]['PhoneCountryCode'], i['Phones'][1]['PhoneNumber'], i['Phones'][3]['PhoneCountryCode'],
              i['Phones'][3]['PhoneNumber'] + "\n" + "Contact ID: " + i['ContactID'] + "\n")
        x=x+"CompanyName: " + str(i['Name']) + "\nFirst Name: " + str(i['FirstName'])+ " Last Name:"
        x+=i['LastName'] + " \nEmail Address: " + i['EmailAddress'] + "  \nStreet Address: "
        x+=i['Addresses'][1]['AddressLine1'] + ", " + i['Addresses'][1]['AddressLine2'] + ", " + i['Addresses'][1]['AddressLine3'] + "," + i['Addresses'][1]['City'] + ", " + i['Addresses'][1]['Region'] + ", "
        x+="\nPhone No:"+ i['Phones'][1]['PhoneCountryCode']+" "+ i['Phones'][1]['PhoneNumber']+"\n"+i['Phones'][3]['PhoneCountryCode']+" "
        x+=i['Phones'][3]['PhoneNumber'] + "\n" + "Contact ID: " + i['ContactID'] + "\n"

    m=MessageClass()
    field=AttachmentFieldsClass()
    field.title="Your list of contacts:"
    field.value=x
    attachment=MessageAttachmentsClass()
    attachment.attach_field(field)
    m.attach(attachment)
    return m
#------------------------------------------------------Retrieve a specific contact-----------------------------------------------------------

def search_contact(args,user_integration):
    xcr = Xero_Credentials.objects.get(user_integration_id=user_integration.id)
    print("user integration-" + str(xcr.user_integration_id))
    token = xcr.XERO_OAUTH_TOKEN
    secret = xcr.XERO_OAUTH_SECRET
    expire = xcr.XERO_EXPIRE
    auth = xcr.XERO_AUTH_EXPIRE
    fmt = '%Y%m%d%H%M%S%f'
    expire = datetime.datetime.strptime(expire, fmt)
    auth = datetime.datetime.strptime(auth, fmt)

    print("user integration-" + str(xcr.user_integration_id))
    print(expire)

    saved_state = {'consumer_key': 'BGJJ6JSSEAGIRWQ9SYKA1T3O7Y6IPF',
                   'consumer_secret': '2JRHWN0QQ1K0AHVDZVUPKCVIQKUUNB',
                   'callback_uri': 'http://127.0.0.1:8000/return/',
                   'verified': True,
                   'oauth_token': token,
                   'oauth_token_secret': secret,
                   'oauth_expires_at': expire,
                   'oauth_authorization_expires_at': auth
                   }

    new_credentials = PublicCredentials(**saved_state)
    print(new_credentials.state)
    xero = Xero(new_credentials)
    #print(new_credentials.state)
    s = xero.contacts.all()
    x=''
    name=args['Name']
    print(name)
    for i in s:
        if i["FirstName"].find(name)!=-1 or i['LastName'].find(name)!=-1 or i['Name'].find(name)!=-1:
            print("CompanyName: " + i['Name'] +"\nFirst Name: "+i["FirstName"]," Last Name:",i['LastName'] +" \nEmail Address: " + i['EmailAddress'] + "  \nStreet Address: " +
                  i['Addresses'][1]['AddressLine1']+", "+i['Addresses'][1]['AddressLine2']+", "+
                  i['Addresses'][1]['AddressLine3'] + "\n," + i['Addresses'][1]['City'] + ", " + i['Addresses'][1]['Region'] + ", " +
                  i['Addresses'][1]['Country'],i['Addresses'][1]['PostalCode'] + "\nPhone: " +
                  i['Phones'][1]['PhoneCountryCode'], i['Phones'][1]['PhoneNumber'], i['Phones'][3]['PhoneCountryCode'],
                  i['Phones'][3]['PhoneNumber']+"\n"+"Contact ID: "+i['ContactID']+"\n")
            x+="CompanyName: " + i['Name'] +"\nFirst Name: "+i["FirstName"]+" Last Name:"+i['LastName'] +" \nEmail Address: " + i['EmailAddress'] + "  \nStreet Address: "
            x+=i['Addresses'][1]['AddressLine1']+", "+i['Addresses'][1]['AddressLine2']+", "
            x+=i['Addresses'][1]['AddressLine3'] + "\n," + i['Addresses'][1]['City'] + ", " + i['Addresses'][1]['Region'] + ", "
            x+="\nPhone No: "+i['Phones'][1]['PhoneCountryCode']+" "+ i['Phones'][1]['PhoneNumber']+" \n"+i['Phones'][3]['PhoneCountryCode'] +" "
            x+=i['Phones'][3]['PhoneNumber']+"\n"+"Contact ID: "+i['ContactID']+"\n"
    if x=='':
        x="Nothing Found matching your query"
    m=MessageClass()
    attachment=MessageAttachmentsClass()
    field=AttachmentFieldsClass()
    field.title="The Contacts retrieved are:"
    field.value=x
    attachment.attach_field(field)
    m.attach(attachment)
    return m

# #-----------------------------------------------------------UPDATE CONTACCT------------------------------------------------------
def update_contact(args,user_integration):
    #contact_id='u\''+contact_id+'\''
    xcr = Xero_Credentials.objects.get(user_integration_id=user_integration.id)
    token = xcr.XERO_OAUTH_TOKEN
    secret = xcr.XERO_OAUTH_SECRET
    expire = xcr.XERO_EXPIRE
    auth = xcr.XERO_AUTH_EXPIRE
    fmt = '%Y%m%d%H%M%S%f'
    expire = datetime.datetime.strptime(expire, fmt)
    auth = datetime.datetime.strptime(auth, fmt)

    print("user integration-" + str(xcr.user_integration_id))
    print(expire)

    saved_state = {'consumer_key': 'BGJJ6JSSEAGIRWQ9SYKA1T3O7Y6IPF',
                   'consumer_secret': '2JRHWN0QQ1K0AHVDZVUPKCVIQKUUNB',
                   'callback_uri': 'http://127.0.0.1:8000/return/',
                   'verified': True,
                   'oauth_token': token,
                   'oauth_token_secret': secret,
                   'oauth_expires_at': expire,
                   'oauth_authorization_expires_at': auth
                   }

    new_credentials = PublicCredentials(**saved_state)
    print(new_credentials.state)
    xero = Xero(new_credentials)
    #email ID compulsory
    name=''
    address_line1=''
    mobile=''
    address_line2=''

    s = xero.contacts.all()
    print("UPDATE CONTACT")
    if args.get("Name",None) is not None:
        name=args['Name']
    email=args['EmailID']
    if args.get('Mobile-Number',None) is not None:
        mobile=args['Mobile-Number']
    if args.get('Address-Line-1',None) is not None:
        address_line1=args['Address-Line-1']
    if args.get('Address-Line-2', None) is not None:
        address_line2=args['Address-Line-2']
    print("READ  EVERYTHING")
    print(email)
    count=0
    for i in s:
        if i['EmailAddress'].find(email) != -1:
            contact_id=i['ContactID']
            print(contact_id)
            c=xero.contacts.get(contact_id)
            #print(c)
            if name!='':
                c[count]['Name']=name
                print("NAME altered")
            if email!='':
                c[count]['EmailAddress']=email
            if mobile!='':
                c[count]['Phones'][3]['PhoneNumber']=mobile
            if address_line1!='':
                c[count]['Addresses'][1]['AddressLine1']=address_line1
            if address_line1!='':
                c[count]['Addresses'][1]['AddressLine2']=address_line2
            #Save updates
    xero.contacts.save(c)
    m = MessageClass()
    attachment = MessageAttachmentsClass()
    field = AttachmentFieldsClass()
    field.title = "Successfully updated the contact"
    attachment.attach_field(field)
    m.attach(attachment)
    return m


# #-------------------------------------------------------------INVOICES---------------------------------------------------------
#
# #-------------------------------------------------------------LIST INVOICE---------------------------------------------------

def list_invoices(args,user_integration):
    print("LIST INVOICES")
    xcr = Xero_Credentials.objects.get(user_integration_id=user_integration.id)
    token = xcr.XERO_OAUTH_TOKEN
    secret = xcr.XERO_OAUTH_SECRET
    expire = xcr.XERO_EXPIRE
    auth = xcr.XERO_AUTH_EXPIRE
    fmt = '%Y%m%d%H%M%S%f'
    expire = datetime.datetime.strptime(expire, fmt)
    auth = datetime.datetime.strptime(auth, fmt)

    print("user integration-" + str(xcr.user_integration_id))
    print(expire)

    saved_state = {'consumer_key': 'BGJJ6JSSEAGIRWQ9SYKA1T3O7Y6IPF',
                   'consumer_secret': '2JRHWN0QQ1K0AHVDZVUPKCVIQKUUNB',
                   'callback_uri': 'http://127.0.0.1:8000/return/',
                   'verified': True,
                   'oauth_token': token,
                   'oauth_token_secret': secret,
                   'oauth_expires_at': expire,
                   'oauth_authorization_expires_at': auth
                   }
    new_credentials = PublicCredentials(**saved_state)
    print(new_credentials.state)
    xero = Xero(new_credentials)
    print("The invoices present are:")
    print(xero.invoices.all())
    s=xero.invoices.all()
    x=''
    for i in s:
        print("Invoice Number:",i['InvoiceNumber'],"Reference: ",i['Reference'],"Payments: ",i['Payments'],"\nCredit Notes",i['CreditNotes'])
        print("Amount Due: ",i['AmountDue'],"Amount Paid: ",i['AmountPaid'],"Amount Credited ",i['AmountCredited'],"\nCurrency Rate: ",i['CurrencyRate'],
              "\nContact Details:\n Name:",i['Contact']['Name'],"Address:",i['Contact']['Addresses'],"Phone No: ",i['Contact']['Phones'])
        print("Subtotal:",i['SubTotal'],"Total Tax:",i['TotalTax'],"Total: ",i['Total'])
        date=str(i['DueDateString'])
        print(date)
        print("Due Date:",date)
        x+="Invoice Number: "+i['InvoiceNumber']+" Reference: "+i['Reference']
        x+=" Payments: "+str(i['Payments'])+"\nCredit Notes"+str(i['CreditNotes'])
        x+="Amount Due: "+str(i['AmountDue'])+" Amount Paid: "+str(i['AmountPaid'])+" Amount Credited "+str(i['AmountCredited'])+"\nCurrency Rate: "+str(i['CurrencyRate'])+"\nContact Details:\n Name:"
        x+=i['Contact']['Name']+" Address: "+str(i['Contact']['Addresses'])+" Phone No: "+str(i['Contact']['Phones'])
        x+="Subtotal: "+str(i['SubTotal'])+ " Total Tax:"+ str(i['TotalTax'])+ " Total: "+str(i['Total'])
        x+="\nDue Date: "+date+"\n\n"
    m=MessageClass()
    field=AttachmentFieldsClass()
    field.title="Your invoices are:"
    field.value=x
    attachment=MessageAttachmentsClass()
    attachment.attach_field(field)

    m.attach(attachment)
    return  m
# #---------------------------------------------------------SEARCH INVOICE---------------------------------------------------------------------

def search_invoice(args,user_integration):#Search by contact name(company) or invoice number or due date
    xcr = Xero_Credentials.objects.get(user_integration_id=user_integration.id)
    token = xcr.XERO_OAUTH_TOKEN
    secret = xcr.XERO_OAUTH_SECRET
    expire = xcr.XERO_EXPIRE
    auth = xcr.XERO_AUTH_EXPIRE
    fmt = '%Y%m%d%H%M%S%f'
    expire = datetime.datetime.strptime(expire, fmt)
    auth = datetime.datetime.strptime(auth, fmt)
    string=args['Search-key']
    print("user integration-" + str(xcr.user_integration_id))
    print(expire)

    saved_state = {'consumer_key': 'BGJJ6JSSEAGIRWQ9SYKA1T3O7Y6IPF',
                   'consumer_secret': '2JRHWN0QQ1K0AHVDZVUPKCVIQKUUNB',
                   'callback_uri': 'http://127.0.0.1:8000/return/',
                   'verified': True,
                   'oauth_token': token,
                   'oauth_token_secret': secret,
                   'oauth_expires_at': expire,
                   'oauth_authorization_expires_at': auth
                   }

    new_credentials = PublicCredentials(**saved_state)
    print(new_credentials.state)
    xero = Xero(new_credentials)
    xero = Xero(new_credentials)
    #print("The invoices found are")
    s = xero.invoices.all()
    x=''
    print("The invoices that match are:")
    for i in s:
        date = str(i['DueDateString'])
        if i['Contact']['Name'].find(string)!=-1 or i['InvoiceNumber'].find(string)!=-1 or date.find(string)!=-1:
            print("Invoice Number:", i['InvoiceNumber'], "Reference: ", i['Reference'], "Payments: ", i['Payments'],
                  "\nCredit Notes", i['CreditNotes'])
            print("Amount Due: ", i['AmountDue'], "Amount Paid: ", i['AmountPaid'], "Amount Credited ",
                  i['AmountCredited'], "\nCurrency Rate: ", i['CurrencyRate'],
                  "\nContact Details:\n Name:", i['Contact']['Name'], "Address:", i['Contact']['Addresses'],
                  "Phone No: ", i['Contact']['Phones'])
            print("Subtotal:", i['SubTotal'], "Total Tax:", i['TotalTax'], "Total: ", i['Total'])

            print(date)
            print("Due Date:", date)
            x+="Invoice Number: "+ str(i['InvoiceNumber'])+" Reference: "+str(i['Reference'])+ " Payments: "+str(i['Payments'])+"\nCredit Notes "+ str(i['CreditNotes'])
            x+=" Amount Due: "+ str(i['AmountDue'])+" Amount Paid: "+ str(i['AmountPaid'])+ " Amount Credited "+ str(i['AmountCredited'])
            x+="\nCurrency Rate: "+ str(i['CurrencyRate'])+"\nContact Details:\n Name: "+ str(i['Contact']['Name'])+ " Address:"+str(i['Contact']['Addresses'])+" Phone No: "+str(i['Contact']['Phones'])
            x+=" Subtotal: "+ str(i['SubTotal'])+ " Total Tax: "+str(i['TotalTax'])+" Total: "+ str(i['Total']) +"\n\n"
    if x=='':
        x="Nothing Found matching your query"
    m=MessageClass()
    attachment = MessageAttachmentsClass()
    field = AttachmentFieldsClass()
    field.title = "The Invoices retrieved are:"
    field.value = x
    attachment.attach_field(field)
    m.attach(attachment)
    return m


# #-------------------------------------------------------UPDATE INVOICE-------------------------------------------------------

def update_invoice(args,user_integration):
    #update by invoice number
    xcr = Xero_Credentials.objects.get(user_integration_id=user_integration.id)
    token = xcr.XERO_OAUTH_TOKEN
    secret = xcr.XERO_OAUTH_SECRET
    expire = xcr.XERO_EXPIRE
    auth = xcr.XERO_AUTH_EXPIRE
    fmt = '%Y%m%d%H%M%S%f'
    expire = datetime.datetime.strptime(expire, fmt)
    auth = datetime.datetime.strptime(auth, fmt)

    print("user integration-" + str(xcr.user_integration_id))
    print(expire)

    saved_state = {'consumer_key': 'BGJJ6JSSEAGIRWQ9SYKA1T3O7Y6IPF',
                   'consumer_secret': '2JRHWN0QQ1K0AHVDZVUPKCVIQKUUNB',
                   'callback_uri': 'http://127.0.0.1:8000/return/',
                   'verified': True,
                   'oauth_token': token,
                   'oauth_token_secret': secret,
                   'oauth_expires_at': expire,
                   'oauth_authorization_expires_at': auth
                   }
    new_credentials = PublicCredentials(**views.saved_state)
    print(new_credentials.state)
    xero = Xero(new_credentials)
    s = xero.invoices.all()
    print(s)
    inv_number=0
    amount_due=0
    amount_paid=0
    subtotal=0
    total=0
    print("Updating invoice...")

    if args.get("Invoice-Number",None) is not None:
        inv_number=args['Invoice-Number']
    if args.get("Amount-Due",None) is not None:
        amount_due=args['Amount-Due']
    if args.get("Amount-Paid",None) is not None:
        amount_paid=args['Amount-Paid']
    if args.get("SubTotal",None) is not None:
        subtotal=args['SubTotal']
    if args.get("Total",None) is not None:
        total=args['Total']
    flag=0
    for i in s:
        if i['InvoiceNumber']==inv_number:
            print("inside")
            flag=1
            inv_id=i['InvoiceID']
            c=xero.invoices.get(inv_id)
            print("updating data...")
            #print(c)
            if amount_due!='':
                c[0]['AmountDue']=amount_due
            if amount_paid!='':
                c[0]['AmountPaid']=amount_paid
            if total!='':
                c[0]['Total']=total
            print(c)

    m = MessageClass()
    attachment = MessageAttachmentsClass()
    field = AttachmentFieldsClass()
    if flag==1:
        print("Updated successfully")
        xero.invoices.save(c)
        field.title = "Successfully updated the invoice"
    else:
        field.title = "Please Try again, Invalid Invoice Number"


    attachment.attach_field(field)
    m.attach(attachment)
    return m

# #----------------------------------------------------------PURCHASE ORDERS---------------------------------------------------
#
# #----------------------------------------------------------LIST PURCHASE ORDERS----------------------------------------------
def list_purchase_orders(args,user_integration):
    xcr = Xero_Credentials.objects.get(user_integration_id=user_integration.id)
    token = xcr.XERO_OAUTH_TOKEN
    secret = xcr.XERO_OAUTH_SECRET
    expire = xcr.XERO_EXPIRE
    auth = xcr.XERO_AUTH_EXPIRE
    fmt = '%Y%m%d%H%M%S%f'
    expire = datetime.datetime.strptime(expire, fmt)
    auth = datetime.datetime.strptime(auth, fmt)

    print("user integration-" + str(xcr.user_integration_id))
    print(expire)

    saved_state = {'consumer_key': 'BGJJ6JSSEAGIRWQ9SYKA1T3O7Y6IPF',
                   'consumer_secret': '2JRHWN0QQ1K0AHVDZVUPKCVIQKUUNB',
                   'callback_uri': 'http://127.0.0.1:8000/return/',
                   'verified': True,
                   'oauth_token': token,
                   'oauth_token_secret': secret,
                   'oauth_expires_at': expire,
                   'oauth_authorization_expires_at': auth
                   }
    new_credentials = PublicCredentials(**saved_state)
    print(new_credentials.state)
    xero = Xero(new_credentials)
    s = xero.purchaseorders.all()
    print(str(s) + "BILLS")
    x=''
    m = MessageClass()
    attachment = MessageAttachmentsClass()
    for i in s:
        ddate=str(i['DeliveryDateString'])
        pdate=str(i['DateString'])
        print("Purchase Order No.:",i['PurchaseOrderNumber'],"Purchase Date: ",pdate,"Delivery Date: ",ddate,"\nDelivery Address: ",i['DeliveryAddress']+
              " Telephone: ",i['Telephone'])
        print("Contact Name: ",i['Contact']['Name'],"Contact Address: ",i['Contact']['Addresses'])
        print("Items: ",i['LineItems'][0]['Description'])
        print("Unit amount: ",i['LineItems'][0]['UnitAmount'],"Quantity: ",i['LineItems'][0]['Quantity'],
               "Discount Rate:",i['LineItems'][0]['DiscountRate'])
        print("Subtotal: ",i['SubTotal'],"Total:",i['Total'])
        x+="Purchase Order No.: "+str(i['PurchaseOrderNumber'])+ " Purchase Date: "+pdate+" Delivery Date: "+ddate+"\nDelivery Address: "+str(i['DeliveryAddress'])+" Telephone: "+str(i['Telephone'])
        x+=" Contact Name: "+str(i['Contact']['Name'])+" Contact Address: "+str(i['Contact']['Addresses'][1]["AddressLine1"])
        if str(i['Contact']['Addresses'][1]["AddressLine2"])!='':
            x+=str(i['Contact']['Addresses'][1]["AddressLine2"])
        if str(i['Contact']['Addresses'][1]["AddressLine3"])!='':
            x+=str(i['Contact']['Addresses'][1]["AddressLine3"])
        if str(i['Contact']['Addresses'][1]["AddressLine4"])!='':
            x+=str(i['Contact']['Addresses'][1]["AddressLine4"])
        x+="\nItems: "+str(i['LineItems'][0]['Description'])
        x+=" Unit amount: "+str(i['LineItems'][0]['UnitAmount'])+" Quantity: "+str(i['LineItems'][0]['Quantity'])+" Discount Rate: "+str(i['LineItems'][0]['DiscountRate'])
        x+="Subtotal: "+str(i['SubTotal'])+"Total:"+str(i['Total'])


        field=AttachmentFieldsClass()
        field.title="The purchase orders are:"
        field.value=x
        x=''
        attachment.attach_field(field)
    m.attach(attachment)
    return m


# #----------------------------------------------------SEARCH PURCHASE ORDERS------------------------------------------------------
#
def search_purchase_orders(args,user_integration):#search with purchasedate deliverydate or total cost or purchase order number or Company name
    xcr = Xero_Credentials.objects.get(user_integration_id=user_integration.id)
    token = xcr.XERO_OAUTH_TOKEN
    secret = xcr.XERO_OAUTH_SECRET
    expire = xcr.XERO_EXPIRE
    auth = xcr.XERO_AUTH_EXPIRE
    fmt = '%Y%m%d%H%M%S%f'
    expire = datetime.datetime.strptime(expire, fmt)
    auth = datetime.datetime.strptime(auth, fmt)

    print("user integration-" + str(xcr.user_integration_id))
    print(expire)

    saved_state = {'consumer_key': 'BGJJ6JSSEAGIRWQ9SYKA1T3O7Y6IPF',
                   'consumer_secret': '2JRHWN0QQ1K0AHVDZVUPKCVIQKUUNB',
                   'callback_uri': 'http://127.0.0.1:8000/return/',
                   'verified': True,
                   'oauth_token': token,
                   'oauth_token_secret': secret,
                   'oauth_expires_at': expire,
                   'oauth_authorization_expires_at': auth
                   }

    new_credentials = PublicCredentials(**saved_state)
    print(new_credentials.state)
    xero = Xero(new_credentials)
    string=args['Search-key']
    s=xero.purchaseorders.all() #YYYYMMDD
    m=MessageClass()
    attachment=MessageAttachmentsClass()
    x=''
    flag=0
    for i in s:
        ddate = str(i['DeliveryDateString'])
        pdate = str(i['DateString'])
        if str(i['Total'])==string!=-1 or ddate==string or pdate==string or i['PurchaseOrderNumber'].find(string)!=-1 or i['Contact']['Name'].find(string)!=-1:
            flag=1
            print("Purchase Order No.:", i['PurchaseOrderNumber'], "Purchase Date: ", pdate, "Delivery Date: ", ddate,
                  "\nDelivery Address: ", i['DeliveryAddress'] +
                  " Telephone: ", i['Telephone'])
            print("Contact Name: ", i['Contact']['Name'], "Contact Address: ", i['Contact']['Addresses'])
            print("Items: ", i['LineItems'][0]['Description'])
            print("Unit amount: ", i['LineItems'][0]['UnitAmount'], "Quantity: ", i['LineItems'][0]['Quantity'],
                  "Discount Rate:", i['LineItems'][0]['DiscountRate'])
            print("Subtotal: ", i['SubTotal'], "Total:", i['Total'])
            x += "Purchase Order No.: " + str(i['PurchaseOrderNumber']) + " Purchase Date: " + pdate + " Delivery Date: " + ddate + "\nDelivery Address: " + str(i['DeliveryAddress']) + " Telephone: " + str(i['Telephone'])
            x += " Contact Name: " + str(i['Contact']['Name']) + " Contact Address: " + str(i['Contact']['Addresses'][1]["AddressLine1"])

            if str(i['Contact']['Addresses'][1]["AddressLine2"]) != '':
                x += str(i['Contact']['Addresses'][1]["AddressLine2"])
            if str(i['Contact']['Addresses'][1]["AddressLine3"]) != '':
                x += str(i['Contact']['Addresses'][1]["AddressLine3"])
            if str(i['Contact']['Addresses'][1]["AddressLine4"]) != '':
                x += str(i['Contact']['Addresses'][1]["AddressLine4"])
            x += "\nItems: " + str(i['LineItems'][0]['Description'])
            x += " Unit amount: " + str(i['LineItems'][0]['UnitAmount']) + " Quantity: " + str(
                i['LineItems'][0]['Quantity']) + " Discount Rate: " + str(i['LineItems'][0]['DiscountRate'])
            x += " Subtotal: " + str(i['SubTotal']) + "Total:" + str(i['Total'])
            field = AttachmentFieldsClass()
            field.title = "The purchase orders are:"
            field.value = x
            x = ''
            attachment.attach_field(field)
        if flag==0:
            m.message_text="Nothing found"
            return m
        m.attach(attachment)
        return m

# #----------------------------------------------UPDATE PURCHASE ORDER-----------------------------------------------------
def update_purchase_orders(args,user_integration):#purchase order no used to update

    xcr = Xero_Credentials.objects.get(user_integration_id=user_integration.id)
    token = xcr.XERO_OAUTH_TOKEN
    secret = xcr.XERO_OAUTH_SECRET
    expire = xcr.XERO_EXPIRE
    auth = xcr.XERO_AUTH_EXPIRE
    fmt = '%Y%m%d%H%M%S%f'
    expire = datetime.datetime.strptime(expire, fmt)
    auth = datetime.datetime.strptime(auth, fmt)

    print("user integration-" + str(xcr.user_integration_id))
    print(expire)

    saved_state = {'consumer_key': 'BGJJ6JSSEAGIRWQ9SYKA1T3O7Y6IPF',
                   'consumer_secret': '2JRHWN0QQ1K0AHVDZVUPKCVIQKUUNB',
                   'callback_uri': 'http://127.0.0.1:8000/return/',
                   'verified': True,
                   'oauth_token': token,
                   'oauth_token_secret': secret,
                   'oauth_expires_at': expire,
                   'oauth_authorization_expires_at': auth
                   }
    new_credentials = PublicCredentials(**saved_state)
    print(new_credentials.state)
    xero = Xero(new_credentials)
    s = xero.purchaseorders.all()
    #print(s)
    p_no = 0
    p_no=args['PurchaseNumber']

    discount=0
    tax_amt=0
    quantity=0
    if args.get("DiscountRate",None) is not None:
        discount=args['DiscountRate']
    if args.get("Quantity",None) is not None:
        quantity=args['Quantity']
    if args.get("Tax-Amount",None) is not None:
        tax_amt=args['Tax-Amount']
    flag=0
    c=''
    print("Updating purchase orders..."+str(p_no)+" "+str(discount))
    for i in s:
        if i['PurchaseOrderNumber'] == p_no:
            flag=1
            po_id = i['PurchaseOrderID']
            #print(po_id)
            c = xero.purchaseorders.get(po_id)
            print(c)
            if discount !='':
                c[0]['DiscountRate'] = discount
            if quantity != '':
                c[0]['LineItems'][0]['Quantity'] = quantity
                print(c[0]['LineItems'][0]['Quantity'])
                line_total=float(c[0]['LineItems'][0]['LineAmount'])
                c[0]['LineItems'][0]['LineAmount']=str(float(quantity)*float(c[0]['LineItems'][0]['UnitAmount']*(100-c[0]['LineItems'][0]['DiscountRate'])/100))
                c[0]['Total']=str(float(c[0]['Total'])-line_total+float(c[0]['LineItems'][0]['LineAmount']))
                c[0]['SubTotal']=c[0]['Total']

            if tax_amt!='':
                c[0]['TotalTax']=tax_amt
                c[0]['Total']=str(float(tax_amt)+float(c[0]['SubTotal']))
            #print(c)


    m=MessageClass()
    attachment=MessageAttachmentsClass()
    field=AttachmentFieldsClass()
    if flag==1:
        print(c)
        field.title='Updated Purchase Order successfully'
        xero.purchaseorders.save(c)
    else:
        field.title="Please try again, Invalid ID"
    attachment.attach_field(field)
    m.attach(attachment)
    return m

#--------------------------------------------------------REAUTHENTICATE------------------------------------------------


def reauthenticate(args,user_integration):
    xcr = Xero_Credentials.objects.get(user_integration_id=user_integration.id)
    print("user integration-" + str(xcr.user_integration_id))
    credentials = PublicCredentials('BGJJ6JSSEAGIRWQ9SYKA1T3O7Y6IPF', '2JRHWN0QQ1K0AHVDZVUPKCVIQKUUNB','http://127.0.0.1:8000/return/')
    print(credentials.url)
    webbrowser.open(credentials.url)
    time.sleep(30)
    # time.sleep(60) for the user
    credentials.verify(views.token)
    xero = Xero(credentials)
    saved_state = credentials.state
    print(str(saved_state) + "saved_state")
    s1 = saved_state['oauth_expires_at']
    s2 = saved_state['oauth_authorization_expires_at']
    print("\n\n")
    print(s1)
    print(s2)
    s1 = s1.strftime('%Y%m%d%H%M%S%f')
    s2 = s2.strftime('%Y%m%d%H%M%S%f')
    # new_date=datetime.datetime.strptime(s1,'%Y%m%d%H%M%S%f')
    # print(new_date)
    t1 = saved_state['oauth_token']
    t2 = saved_state['oauth_token_secret']
    obj = Xero_Credentials.objects.get(user_integration_id=user_integration.id)
    obj.XERO_OAUTH_TOKEN = t1
    obj.XERO_OAUTH_SECRET = t2
    obj.XERO_EXPIRE = s1
    obj.XERO_AUTH_EXPIRE = s2
    obj.XERO_UPDATE_LOGIN_FLAG = True
    print(str(obj.XERO_AUTH_EXPIRE) + "  helloooo")
    obj.save()



    # global flag
    # global saved_state
    # credentials = PublicCredentials(consumer_key, consumer_secret)
    m = MessageClass()
    m.message_text="Your account has been authenticated"
    # if flag == 0:
    #     code=args['7-Digit-Code']
    #     print(code)
    #     print(credentials.url)
    #     credentials.verify(input("enter"))
    #     saved_state = credentials.state
    #     new_credentials=PublicCredentials(**saved_state)
    #     xero=Xero_Credentials(new_credentials)
    #     flag = 1
    #     print("Your account has been authenticated")
    #     attachment=MessageAttachmentsClass()
    #     field=AttachmentFieldsClass()
    #     field.title="Your account is now authenticated"
    #     attachment.attach_field(field)
    #     m.attach(attachment)
    return m

#---------------------------------------------------AUTHENTICATE------------------------------------------------------


# #list_contacts()
# #search_contact("Abhiram")
# #update_contact("YellowAnhdsgjst10","Hello@testing.com","9886051850","#402,CirrusMino, 13th cross, new tipps")
# #list_invoices()
# #search_invoice("Abhiram")
# #list_purchase_orders()
# #update_invoice('INV-0001','252.5','10.0','262.5')
# #search_purchase_orders('2018-06-21')
# #update_purchase_orders("PO-0001","2018-06-21","2018-06-30","")
#
