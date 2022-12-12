from django.shortcuts import render,redirect
from django.views import generic
from accounts.models import CustomUser,User_Details,ETF,ETF_instance
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from sadmin import views as sadminViews
import yfinance as yf

class Users(generic.ListView):
    model = CustomUser
    context_object_name = "users"
    template_name = 'sadmin/users.html'
    
    def get_queryset(self):
        #print(CustomUser.objects.all())
        return CustomUser.objects.all()

def UserDetailView(request, pk):
    """
    Request for ETF details page
    """
    try:
        user_details = User_Details.objects.get(user_id = pk)
    except ObjectDoesNotExist:
        user_details = {}
    
    try:
        user_etf = ETF_instance.objects.filter(user_id = pk)
        user_etf_data  = []
        for etf in user_etf:
            etf_data = yf.Ticker(etf.ETF.symbol).info
            this_etf = {
                'id' : etf.pk,
                'symbol' : etf.ETF.symbol,
                'quoteType': etf_data['quoteType'],
                'company': etf_data['longName'],
                'history': '--chart--',
                'price' : str(round(etf_data['regularMarketPrice'], 2)) + " " + etf_data["currency"],
                'growth' : round(etf_data['regularMarketPrice'] - etf_data["previousClose"], 2)
            }
            user_etf_data.append(this_etf)
    except ObjectDoesNotExist:
        user_etf = {}    

    try:
        user = CustomUser.objects.get(pk = pk)
        context = {'user': user, 'user_details' : user_details,'user_etf': user_etf_data}
        return render(request, "sadmin/customuser_detail.html", context)
    # Not found; redirect to browse
    except ObjectDoesNotExist:
        return redirect('/sadmin/users')