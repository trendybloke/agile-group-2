from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.template.defaulttags import register
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from Login_SignUp_ResetPWEmail_HomePage import views as home_views
from Login_SignUp_ResetPWEmail_HomePage.forms import LoginForm, SignUpForm
from etfs import views as etf_views
from decimal import Decimal
import accounts.models as models
import yfinance as yf

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="accounts/login">login</a>.'
            success = True

            return redirect("/login")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)

@login_required
def portfolio(request, username):
    """ Request for a user's portfolio page """
    context = {}
    
    # Set template flag for showing sell columns
    context["user_owns_page"] = request.user.username == username
    
    # Determine if requested user exists
    try:
        user_obj = models.CustomUser.objects.get(username=username)    
        
        # User exists
        context["username"] = user_obj.username
        
        # Get all ETF_instances belonging to user
        users_etf_instances = models.ETF_instance.objects.filter(user = user_obj, is_deleted=False)
        
        # Get all ETFs inside ETF_instances
        etfs = {}
        for etf_instance in users_etf_instances:
                etfs[etf_instance.display_ETF().symbol] = (etf_instance.price_on_create, etf_instance.date_created, etf_instance.id)

        etf_data = {}
        
        total_portfolio_worth = 0
        total_portfolio_investment = 0
        
        # Get data for each ETF
        for etf_symbol, instance_data in etfs.items():
            specific_etf_data = {}
            etf_info = yf.Ticker(etf_symbol).info
            
            specific_etf_data['company'] = etf_info['longName']
            specific_etf_data['quoteType'] = etf_info['quoteType']
            
            price_data = str()
            price = str()
            
            if(etf_info['quoteType'] == 'ETF'):
                price_data = 'regularMarketPrice'
            else:
                price_data = 'currentPrice'
            
            growth = round(etf_info[price_data] - instance_data[0], 2)
            
            if growth and growth > 0:
                growth = '+ ' + str(growth) + etf_info["currency"]
            elif growth and growth < 0:
                growth = str(growth)[0] + " " + str(growth)[1:] + etf_info["currency"]
                
            price = str(round(etf_info[price_data], 2)) + " " + etf_info["currency"]
            
            total_portfolio_worth += etf_info[price_data]
            total_portfolio_investment += instance_data[0]
            
            specific_etf_data['growth'] = growth
            specific_etf_data['price'] = price
            specific_etf_data['bought_price'] = str(round(instance_data[0], 2)) + " " + etf_info["currency"]
            specific_etf_data['created_on'] = instance_data[1]
            specific_etf_data['instance_id'] = instance_data[2]
            
            etf_data[etf_symbol] = specific_etf_data
        
        # Generate breakdown statistics
        try:
            user_account = models.Account.objects.get(user=user_obj)
            context["account_balance"] = "Account balance: " + str(user_account.balance) + " USD"
        except ObjectDoesNotExist:
            context["account_balance"] = "Set up account"
        
        context["total_price"] = str(round(total_portfolio_worth, 2)) + " USD"
        context["total_spent"] = str(round(total_portfolio_investment, 2)) + " USD"
        
        total_net_growth = round(total_portfolio_worth - total_portfolio_investment, 2)
        
        if total_net_growth > 0:
            total_net_growth = "+ " + str(total_net_growth)
        elif total_net_growth < 0:
            total_net_growth = "- " + str(total_net_growth)[1:]
        
        total_net_growth = str(total_net_growth) + " USD"
        
        context["total_growth"] = total_net_growth
        
        context['etf_list'] = users_etf_instances
        context['etf_data'] = etf_data
    
        return render(request, "portfolio.html", context)
    except ObjectDoesNotExist:
        return redirect(etf_views.etf_browse)

@login_required
def sell_etf(request, username):
    """ POST request received when a user wants to sell an ETF instance """
    if request.method != "POST":
        return redirect(etf_views.etf_browse)
    
    try:
        # Find user's ETF instance from request
        request_dict = request.POST.dict()
               
        instance_id = request_dict['instance_id']
        
        # Will Throw DoesNotExist if fails
        etf_instance = models.ETF_instance.objects.get(id=instance_id)
        
        # etf_obj = models.ETF.objects.get(symbol=etf_symbol)
        etf_symbol = str(etf_instance.display_ETF())
        
        etf_info = yf.Ticker(etf_symbol).info
        
        etf_price = 0
        
        if etf_info["quoteType"] == "ETF":
            etf_price = round(Decimal(etf_info["regularMarketPrice"]), 2)
        else:
            etf_price = round(Decimal(etf_info["currentPrice"]), 2)
        
        user_obj = models.CustomUser.objects.get(username=username)
        
        
        # Add current price to account balance
        user_account = models.Account.objects.get(user=user_obj)
        
        user_account.update_balance(amount=etf_price, type="+")
        
        # Mark ETF instance as 'deleted'
        etf_instance.is_deleted = True
        
        # Save instance and account
        etf_instance.save()
        user_account.save()
        
        messages.success(request, 'Sold ' + etf_symbol + ' for ' + str(etf_price) + ' USD!')
    except Exception as e:
        print(str(e))
        messages.error(request, str('Ran into a problem: ' + e + ' Transaction canclled.'))
        return redirect(portfolio, username)
    
    return redirect(portfolio, username)
