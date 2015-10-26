from django import template
from events.models import Attendance

def event(context, e):
	to_return = {
		'event': e,
		'reqeust': context['request'],
	}
	if context['user'].is_authenticated():
		try:
			Attendance.objects.get(event=e, user=context['user'])
			attending = True
		except Attendance.DoesNotExist:
			attending = False
		to_return.update({
			'attending': attending,
			'authenticated': True,
		})
	else:
		to_return['authenticated'] = False

	return to_return 
	
#access to all template using register
register = template.Library()

register.inclusion_tag('events/event.html', takes_context=True)(event)
