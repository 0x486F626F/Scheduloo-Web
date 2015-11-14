from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import os
import json
import sqlite3
import uwaterlooapi
import uwcoursedb

def get_apikey(path = 'db/'):
	if not os.path.exists(path):
		os.makedirs(path)
	sql = sqlite3.connect(path + 'apikey.db')
	db = sql.cursor()
	db.execute("CREATE TABLE IF NOT EXISTS apikey (key TEXT);")
	db.execute("SELECT key FROM apikey;")
	result = db.fetchall()
	if result == []:
		key = raw_input("Please set a UWAPI key: ");
		db.execute("INSERT INTO apikey (key) VALUES('" + key + "');")
		sql.commit()
		return key
	else:
		print "Use key: " + str(result[0][0])
		return str(result[0][0])

def check_course(subject, catalog, courseDB):
	if not(courseDB.course_opening(subject, catalog)):
		return 'The course is not offered this term'
	else:
		return 'True'

def make_rating_chart(course_list, courseDB):
	section_list = []
	for course in course_list:
		section = courseDB.get_opening_sections(
				course['subject'], course['catalog'])
		section_list.append(section)
	return json.dumps(section_list)

@csrf_exempt
def scheduloo(request):
	courseDB = uwcoursedb.UWCourseDB(
			1161, 
			uwaterlooapi.UWaterlooAPI(api_key = get_apikey()))

	if request.method == "POST":
		post_data = request.body
		body = json.loads(post_data)
		if body['command'] == 'check_course':
			return HttpResponse(check_course(body['course']['subject'],
				body['course']['catalog'], courseDB))
		if body['command'] == 'submit_course_list':
			return HttpResponse(make_rating_chart(body['course'], courseDB))

	return render(request, 'scheduloo.html')
