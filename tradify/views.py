from django.http import HttpResponse, Http404
from django.shortcuts import render
import pandas as pd
from pandas_datareader import data as web
import plotly.graph_objects as go
from pandas import ExcelWriter
import os
import sys
from django.conf import settings
import requests
import json

from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController


def index(request):
    return render(request, 'index.html')


def charts(request):
    symbol = request.GET.get('sticker')
    start_date = request.GET.get('data_start')
    end_date = request.GET.get('data_end')
    if symbol:    
        df = web.DataReader(symbol, data_source='yahoo', start=start_date)
        df['Date'] = df.index
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        barData=df.to_dict(orient='record')
        return render(request, 'charts.html', {'data':barData})
    return render(request, 'charts.html')


def uvolume(request):
    url = "https://twelve-data1.p.rapidapi.com/stocks"
    querystring = {"exchange": "NASDAQ", "format": "json"}
    headers = {
        'x-rapidapi-key': "9c714f9a9fmsh22461f0b6d7e572p1bb1b3jsn9e2c7d195b1c",
        'x-rapidapi-host': "twelve-data1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)
    return render(request, 'unusualvolume.html', {'response': response['data'][1:100]})


def equity(request):
    symbol = request.GET.get('sticker')
    start_date = request.GET.get('data-start')
    strength = request.GET.get('MStrength')

    if symbol:
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-financials"
        querystring = {"symbol":symbol,"region":"US"}
        headers = {
            'x-rapidapi-key': "9c714f9a9fmsh22461f0b6d7e572p1bb1b3jsn9e2c7d195b1c",
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        response = json.loads(response.text)
        return render(request, 'equitylevel.html', {'response': response})
    return render(request, 'equitylevel.html')


def help(request):
    return render(request, 'help.html')


def exporttool(request):
    symbol = request.GET.get('sticker')
    start_date = request.GET.get('data-start')

    if symbol:
        df = web.DataReader(symbol, data_source='yahoo', start=start_date)
        writer = ExcelWriter('PythonExport.xlsx')
        df.to_excel(writer,'Sheet1')
        writer.save()
    return render(request, 'exporttool.html')


def download(request):
    print('download')
    file_path = './PythonExport.xlsx'
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response


def authorize_credit_card(request):
    """
    Authorize a credit card (without actually charging it)
    """

    # Create a merchantAuthenticationType object with authentication details
    # retrieved from the constants file
    import pdb; pdb.set_trace()
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = '6fVTC27yH'
    merchantAuth.transactionKey = '9P7y7hGmj268Ja5b'

    # Create the payment data for a credit card
    creditCard = apicontractsv1.creditCardType()
    creditCard.cardNumber = "4111111111111111"
    creditCard.expirationDate = "2035-12"
    creditCard.cardCode = "123"

    # Add the payment data to a paymentType object
    payment = apicontractsv1.paymentType()
    payment.creditCard = creditCard

    # Create order information
    order = apicontractsv1.orderType()
    order.invoiceNumber = "10101"
    order.description = "Golf Shirts"

    # Set the customer's Bill To address
    customerAddress = apicontractsv1.customerAddressType()
    customerAddress.firstName = "Ellen"
    customerAddress.lastName = "Johnson"
    customerAddress.company = "Souveniropolis"
    customerAddress.address = "14 Main Street"
    customerAddress.city = "Pecan Springs"
    customerAddress.state = "TX"
    customerAddress.zip = "44628"
    customerAddress.country = "USA"

    # Set the customer's identifying information
    customerData = apicontractsv1.customerDataType()
    customerData.type = "individual"
    customerData.id = "99999456654"
    customerData.email = "EllenJohnson@example.com"

    # Add values for transaction settings
    duplicateWindowSetting = apicontractsv1.settingType()
    duplicateWindowSetting.settingName = "duplicateWindow"
    duplicateWindowSetting.settingValue = "600"
    settings = apicontractsv1.ArrayOfSetting()
    settings.setting.append(duplicateWindowSetting)

    # setup individual line items
    line_item_1 = apicontractsv1.lineItemType()
    line_item_1.itemId = "12345"
    line_item_1.name = "first"
    line_item_1.description = "Here's the first line item"
    line_item_1.quantity = "2"
    line_item_1.unitPrice = "12.95"
    line_item_2 = apicontractsv1.lineItemType()
    line_item_2.itemId = "67890"
    line_item_2.name = "second"
    line_item_2.description = "Here's the second line item"
    line_item_2.quantity = "3"
    line_item_2.unitPrice = "7.95"

    # build the array of line items
    line_items = apicontractsv1.ArrayOfLineItem()
    line_items.lineItem.append(line_item_1)
    line_items.lineItem.append(line_item_2)

    # Create a transactionRequestType object and add the previous objects to it.
    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType = "authOnlyTransaction"
    transactionrequest.amount = 100
    transactionrequest.payment = payment
    transactionrequest.order = order
    transactionrequest.billTo = customerAddress
    transactionrequest.customer = customerData
    transactionrequest.transactionSettings = settings
    transactionrequest.lineItems = line_items

    # Assemble the complete transaction request
    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchantAuth
    createtransactionrequest.refId = "MerchantID-0001"
    createtransactionrequest.transactionRequest = transactionrequest
    # Create the controller
    createtransactioncontroller = createTransactionController(
        createtransactionrequest)
    createtransactioncontroller.execute()

    response = createtransactioncontroller.getresponse()

    if response is not None:
        # Check to see if the API request was successfully received and acted upon
        if response.messages.resultCode == "Ok":
            # Since the API request was successful, look for a transaction response
            # and parse it to display the results of authorizing the card
            if hasattr(response.transactionResponse, 'messages') is True:
                print(
                    'Successfully created transaction with Transaction ID: %s'
                    % response.transactionResponse.transId)
                print('Transaction Response Code: %s' %
                      response.transactionResponse.responseCode)
                print('Message Code: %s' %
                      response.transactionResponse.messages.message[0].code)
                print('Description: %s' % response.transactionResponse.
                      messages.message[0].description)
            else:
                print('Failed Transaction.')
                if hasattr(response.transactionResponse, 'errors') is True:
                    print('Error Code:  %s' % str(response.transactionResponse.
                                                  errors.error[0].errorCode))
                    print(
                        'Error message: %s' %
                        response.transactionResponse.errors.error[0].errorText)
        # Or, print errors if the API request wasn't successful
        else:
            print('Failed Transaction.')
            if hasattr(response, 'transactionResponse') is True and hasattr(
                    response.transactionResponse, 'errors') is True:
                print('Error Code: %s' % str(
                    response.transactionResponse.errors.error[0].errorCode))
                print('Error message: %s' %
                      response.transactionResponse.errors.error[0].errorText)
            else:
                print('Error Code: %s' %
                      response.messages.message[0]['code'].text)
                print('Error message: %s' %
                      response.messages.message[0]['text'].text)
    else:
        print('Null Response.')

    return response

def charge_credit_card(amount):
    """
    Charge a credit card
    """

    # Create a merchantAuthenticationType object with authentication details
    # retrieved from the constants file
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = '6fVTC27yH'
    merchantAuth.transactionKey = '9P7y7hGmj268Ja5b'

    # Create the payment data for a credit card
    creditCard = apicontractsv1.creditCardType()
    creditCard.cardNumber = "4111111111111111"
    creditCard.expirationDate = "2035-12"
    creditCard.cardCode = "123"

    # Add the payment data to a paymentType object
    payment = apicontractsv1.paymentType()
    payment.creditCard = creditCard

    # Create order information
    order = apicontractsv1.orderType()
    order.invoiceNumber = "10101"
    order.description = "Golf Shirts"

    # Set the customer's Bill To address
    customerAddress = apicontractsv1.customerAddressType()
    customerAddress.firstName = "Ellen"
    customerAddress.lastName = "Johnson"
    customerAddress.company = "Souveniropolis"
    customerAddress.address = "14 Main Street"
    customerAddress.city = "Pecan Springs"
    customerAddress.state = "TX"
    customerAddress.zip = "44628"
    customerAddress.country = "USA"

    # Set the customer's identifying information
    customerData = apicontractsv1.customerDataType()
    customerData.type = "individual"
    customerData.id = "99999456654"
    customerData.email = "EllenJohnson@example.com"

    # Add values for transaction settings
    duplicateWindowSetting = apicontractsv1.settingType()
    duplicateWindowSetting.settingName = "duplicateWindow"
    duplicateWindowSetting.settingValue = "600"
    settings = apicontractsv1.ArrayOfSetting()
    settings.setting.append(duplicateWindowSetting)

    # setup individual line items
    line_item_1 = apicontractsv1.lineItemType()
    line_item_1.itemId = "12345"
    line_item_1.name = "first"
    line_item_1.description = "Here's the first line item"
    line_item_1.quantity = "2"
    line_item_1.unitPrice = "12.95"
    line_item_2 = apicontractsv1.lineItemType()
    line_item_2.itemId = "67890"
    line_item_2.name = "second"
    line_item_2.description = "Here's the second line item"
    line_item_2.quantity = "3"
    line_item_2.unitPrice = "7.95"

    # build the array of line items
    line_items = apicontractsv1.ArrayOfLineItem()
    line_items.lineItem.append(line_item_1)
    line_items.lineItem.append(line_item_2)

    # Create a transactionRequestType object and add the previous objects to it.
    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType = "authCaptureTransaction"
    transactionrequest.amount = amount
    transactionrequest.payment = payment
    transactionrequest.order = order
    transactionrequest.billTo = customerAddress
    transactionrequest.customer = customerData
    transactionrequest.transactionSettings = settings
    transactionrequest.lineItems = line_items

    # Assemble the complete transaction request
    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchantAuth
    createtransactionrequest.refId = "MerchantID-0001"
    createtransactionrequest.transactionRequest = transactionrequest
    # Create the controller
    createtransactioncontroller = createTransactionController(
        createtransactionrequest)
    createtransactioncontroller.execute()

    response = createtransactioncontroller.getresponse()

    if response is not None:
        # Check to see if the API request was successfully received and acted upon
        if response.messages.resultCode == "Ok":
            # Since the API request was successful, look for a transaction response
            # and parse it to display the results of authorizing the card
            if hasattr(response.transactionResponse, 'messages') is True:
                print(
                    'Successfully created transaction with Transaction ID: %s'
                    % response.transactionResponse.transId)
                print('Transaction Response Code: %s' %
                      response.transactionResponse.responseCode)
                print('Message Code: %s' %
                      response.transactionResponse.messages.message[0].code)
                print('Description: %s' % response.transactionResponse.
                      messages.message[0].description)
            else:
                print('Failed Transaction.')
                if hasattr(response.transactionResponse, 'errors') is True:
                    print('Error Code:  %s' % str(response.transactionResponse.
                                                  errors.error[0].errorCode))
                    print(
                        'Error message: %s' %
                        response.transactionResponse.errors.error[0].errorText)
        # Or, print errors if the API request wasn't successful
        else:
            print('Failed Transaction.')
            if hasattr(response, 'transactionResponse') is True and hasattr(
                    response.transactionResponse, 'errors') is True:
                print('Error Code: %s' % str(
                    response.transactionResponse.errors.error[0].errorCode))
                print('Error message: %s' %
                      response.transactionResponse.errors.error[0].errorText)
            else:
                print('Error Code: %s' %
                      response.messages.message[0]['code'].text)
                print('Error message: %s' %
                      response.messages.message[0]['text'].text)
    else:
        print('Null Response.')

    return response
