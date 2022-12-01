"""
Views for ETF pages
"""
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import ETF
import yfinance as yf

def etf_browse(request):
    """
    Request for ETF browse page
    """
    context = {}
    
    etfs = ETF.objects.all()
    
    # for etf in etfs:
        # revenueGrowth / earningsGrowth
        
    
    context["etf_list"] = etfs
    
    return render(request, "etf_browse.html", context)

def etf_details(request, etf_symbol):
    """
    Request for ETF details page
    """
    context = {}

    try:
        requestedEtf = ETF.objects.get(symbol = etf_symbol)
        context["etf_symbol"] = requestedEtf.symbol
        
        # Dictionary containing up to date info on the passed ETF
        etf_details = yf.Ticker(etf_symbol).info
        
        context["etf_data"] = etf_details
        
        context["etf_long_name"] = etf_details["longName"]
        
        context["etf_price"] = etf_details["currentPrice"]
        
        context["etf_summary"] = etf_details["longBusinessSummary"]
        
        context["etf_website"] = etf_details["website"]
        
        context["etf_logo"] = etf_details["logo_url"]
        
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
        context["etf_symbol"] = requestedEtf.symbol
        
        etf_details = yf.Ticker(etf_symbol).info
        
        context["etf_long_name"] = etf_details["longName"]

        context["etf_price"] = etf_details["currentPrice"]
        
        context["etf_logo"] = etf_details["logo_url"]
        
        return render(request, "purchase_etf.html", context)
    # Not found; redirect to browse
    except ObjectDoesNotExist:
        return redirect(etf_browse)
