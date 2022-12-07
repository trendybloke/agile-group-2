"""
Views for ETF pages
"""
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import ETF
import yfinance as yf

def buildContext(etf_details):
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

def etf_browse(request):
    """
    Request for ETF browse page
    """
    context = {}
    
    etfs = ETF.objects.all()
    etf_companies = {}
    etf_growths = {}
    etf_prices = {}
    etf_quotetypes = {}
    
    for etf in etfs:
        etf_info = yf.Ticker(etf.symbol).info
        
        # print("\n\n" + str(etf_info))

        etf_companies[etf.symbol] = etf_info["longName"]
        
        price_data = str()
        price = str()

        etf_quotetypes[etf.symbol] = etf_info["quoteType"]
        
        if(etf_info["quoteType"] == "ETF"):
            price_data = "regularMarketPrice"
            growth = round(etf_info[price_data] - etf_info["previousClose"], 2)
        else:
            price_data = "currentPrice"
            growth = etf_info["revenueGrowth"]
    
        # growth = etf_info[growth_data]
        
        if growth and growth > 0:
            growth = "+ " + str(growth)
        
        price = str(round(etf_info[price_data], 2)) + " " + etf_info["currency"]
    
        etf_growths[etf.symbol] =  growth
        etf_prices[etf.symbol] = price

    context["etf_list"] = etfs
    context["etf_companies"] = etf_companies.items()
    context["etf_growths"] = etf_growths.items()
    context["etf_prices"] = etf_prices.items()
    context["etf_quotetypes"] = etf_quotetypes.items()
    
    return render(request, "etf_browse.html", context)

def etf_details(request, etf_symbol):
    """
    Request for ETF details page
    """
    try:
        requestedEtf = ETF.objects.get(symbol = etf_symbol)

        # Dictionary containing up to date info on the passed ETF
        etf_details = yf.Ticker(requestedEtf.symbol).info

        context = buildContext(etf_details)
        
        return render(request, "etf_details.html", context)
    # Not found; redirect to browse
    except ObjectDoesNotExist:
        return redirect(etf_browse)

def purchase_etf(request, etf_symbol):
    """
    Request for ETF purchase page
    """
    context = {}
    
    try:
        requestedEtf = ETF.objects.get(symbol = etf_symbol)

        # Dictionary containing up to date info on the passed ETF
        etf_details = yf.Ticker(requestedEtf.symbol).info

        context = buildContext(etf_details)
        
        return render(request, "purchase_etf.html", context)
    # Not found; redirect to browse
    except ObjectDoesNotExist:
        return redirect(etf_browse)
