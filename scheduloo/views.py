from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

def check_course(subject, catalog):
	print subject, catalog
	if len(subject) < 6 and len(catalog) < 5:
		return 'True'
	return 'False'

@csrf_exempt
def scheduloo(request):
	if request.method == "POST":
		post_data = request.body
		body = json.loads(post_data)
		if body['command'] == 'check_course':
			return HttpResponse(check_course(body['course']['subject'],
				body['course']['catalog']))
		return HttpResponse('POOOOOOOOOOOOOST!')

	return render(request, 'scheduloo.html')
