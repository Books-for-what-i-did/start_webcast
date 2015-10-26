from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

#pip install python-dateutil
from dateutil.parser import parse #date parser
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# ours
from events.forms import EventForm
from events.models import Event, Attendance

# Create your views here.

def tonight(request):
	events = Event.objects.today().filter(latest=True)
	#create dictionary
	context = {
		'events': events,
	}
	return render_to_response(
		'events/tonight.html',#template
		context, #user variable
		context_instance = RequestContext(request)
	)

@login_required
def create(request):
	form = EventForm(request.POST or None)
	if form.is_valid():
		#creator should be declared
		event = form.save(commit=False)
		event.creator = request.user
		guessed_date = None
		for word in event.description.split():
			try:
				guessed_date = parse(word)
				break
			except ValueError:
				continue
		event.start_date = guessed_date
		event.save()
		#request.user.message_set.create(message='Your event was posted')
		messages.success(request, ("Your event was posted."))
		if 'next' in request.POST:
			next = request.POST['next']
		else:
			next = reverse('ev_tonight')
		return HttpResponseRedirect(next)
	return render_to_response(
		'events/create.html',
		{'form': form},
		context_instance = RequestContext(request)
	)
#create = login_required(create)

@login_required
def toggle_attendance(request):
	try:
		event_id = int(request.POST['event_id'])
	except (KeyError, ValueError):
		raise Http404 #couldn't be found
	
	event = get_object_or_404(Event, id=event_id)
	attendance, created = Attendance.objects.get_or_create(user=request.user, 
		event=event)
	if created:
		messages.success(request, ('You are now attending "%s"' % event))
	else:
		attendance.delete()
		messages.success(request, ('You are no longer attending "%s"' % event))
	
	next = request.POST.get('next', '')
	if not next:
		next = reverse('ev_tonight')
	return HttpResponseRedirect(next)

def archive(request):
	events = Event.objects.filter()
	context = {
		'events': events, 
	}
	return render_to_response(
		'events/archive.html',#template
		context, #user variable
		context_instance = RequestContext(request)
	)
