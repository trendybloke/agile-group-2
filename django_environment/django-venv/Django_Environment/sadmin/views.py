from django.shortcuts import render,redirect
from django.views import generic
from accounts.models import CustomUser,User_Details
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from sadmin import views as sadminViews

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
        user = CustomUser.objects.get(pk = pk)
        context = {'user': user, 'user_details' : user_details}
        return render(request, "sadmin/customuser_detail.html", context)
    # Not found; redirect to browse
    except ObjectDoesNotExist:
        return redirect('/sadmin/users')