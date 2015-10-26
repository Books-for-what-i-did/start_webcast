from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from events.models import Event
from events.forms import EventForm
from dateutil.parser import parse #date parser
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

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
