"""
Views for ETF pages
"""
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaulttags import register
from django.views.decorators.http import require_http_methods
from decimal import Decimal
from datetime import date
from accounts.models import ETF, ETF_instance, Account, CustomUser
import yfinance as yf

def buildDetailedContext(etf_details):
    context = {}
    # context["etf_data"] = etf_details
    
    context["etf_symbol"] = etf_details["symbol"]
    context["etf_long_name"] = etf_details["longName"]
    context["etf_summary"] = etf_details["longBusinessSummary"]
    context["etf_logo"] = etf_details["logo_url"]
    
    if(etf_details["quoteType"] == "ETF"):
        # Add ETF only data here
        context["etf_price"] = str(round(etf_details["regularMarketPrice"], 2)) + " " + etf_details["currency"] 
        context["etf_amount"] = etf_details["askSize"]
    else:    
        # Add stock only data here
        context["etf_price"] = str(round(etf_details["currentPrice"], 2)) + " " + etf_details["currency"] 
        context["etf_website"] = etf_details["website"]

    return context

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)

def etf_browse(request):
    """
    Request for ETF browse page
    """
    context = {}
    
    etfs = ETF.objects.all()
    
    etf_data = {}
    
    for etf in etfs:
        specific_etf_data = {}
        etf_info = yf.Ticker(etf.symbol).info
        
        # print("\n\n" + str(etf_info))

        specific_etf_data['company'] = etf_info["longName"]
        specific_etf_data['quoteType'] = etf_info["quoteType"]
        
        price_data = str()
        price = str()
        
        if(etf_info["quoteType"] == "ETF"):
            price_data = "regularMarketPrice"
            growth = round(etf_info[price_data] - etf_info["previousClose"], 2)
        else:
            price_data = "currentPrice"
            growth = etf_info["revenueGrowth"]
        
        if growth and growth > 0:
            growth = "+ " + str(growth)
        elif growth and growth < 0:
            growth = str(growth)[0] + " " + str(growth)[1:]
        
        price = str(round(etf_info[price_data], 2)) + " " + etf_info["currency"]
    
        specific_etf_data['growth'] = growth
        specific_etf_data['price'] = price
        
        etf_data[etf.symbol] = specific_etf_data

    context["etf_list"] = etfs
    context["etf_data"] = etf_data
    
    # print(context["etf_data"])
    
    return render(request, "etf_browse.html", context)

def etf_details(request, etf_symbol):
    """
    Request for ETF details page
    """
    try:
        requestedEtf = ETF.objects.get(symbol = etf_symbol)

        # Dictionary containing up to date info on the passed ETF
        etf_details = yf.Ticker(requestedEtf.symbol).info

        context = buildDetailedContext(etf_details)
        
        return render(request, "etf_details.html", context)
    # Not found; redirect to browse
    except ObjectDoesNotExist:
        return redirect(etf_browse)

@require_http_methods(["GET"])
def purchase_etf(request, etf_symbol):
    """
    Request for ETF purchase page
    """
    if request.method == "POST":
        return redirect(instantiate_etf, etf_symbol)
    
    context = {}
    
    try:
        requestedEtf = ETF.objects.get(symbol = etf_symbol)

        # Dictionary containing up to date info on the passed ETF
        etf_details = yf.Ticker(requestedEtf.symbol).info

        context = buildDetailedContext(etf_details)
        
        return render(request, "purchase_etf.html", context)
    # Not found; redirect to browse
    except ObjectDoesNotExist:
        return redirect(etf_browse)

@require_http_methods(["POST"])
def instantiate_etf(request, etf_symbol):
    """ POST request when buying an ETF. """
    if request.method != "POST":
        return redirect(etf_browse)
    
    # Find username from request (session data?)
    user_username = request.POST.dict()['username']
    
    try:
        # Find if user, their account, and ETF exist    
        user_obj = CustomUser.objects.get(username=user_username)
        user_account = Account.objects.get(user=user_obj)
        etf_obj = ETF.objects.get(symbol=etf_symbol)
        
        etf_info = yf.Ticker(etf_symbol).info
        
        etf_price = 0
        
        if etf_info["quoteType"] == "ETF":
            etf_price = round(Decimal(etf_info["regularMarketPrice"]), 2)
        else:
            etf_price = round(Decimal(etf_info["currentPrice"]), 2)
        
        # Create and save new instance
        ETF_instance.objects.create(user=user_obj, ETF=etf_obj, price_on_create=etf_price, date_created=date.today())
        
        # Change account balance
        user_account.update_balance(etf_price, '-')
        user_account.save()
        
        # request.session["success_msg"] = "Purchased " + etf_symbol + "! Click 'portfolio' to view."
        messages.success(request, "Purchased " + etf_symbol + "! Click 'portfolio' to view.")
    except ObjectDoesNotExist as e:    
        # If account does not exist, redirect to portfolio (or wherever they can create an account)
        # request.session["error_msg"] = e.__str__
        messages.error(request, 'Ran into a problem: ' + e + ' Transaction cancelled.')
    # Redirect to browse
    return redirect(etf_browse)