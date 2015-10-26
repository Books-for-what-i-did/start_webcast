from django.shortcuts import render

# Create your views here.

from django.http import *
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/events/archive')
	    else:
                context = {
			'stage':'User is inactive',
		}
	else:
	    context = {
		    'stage':'Wrong ID/PW',
	    }

    else:
        context = {
	    'stage':'First Login',
        }
    return render_to_response("login.html", context, 
   			 context_instance=RequestContext(request))

def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/events/archive')
