from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import os
import json
import sqlite3
import uwcoursedb
import uwaterlooapi
import scheduloo_core
import datetime

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

def convert_array(time):
	result = ""
	for day in time:
		if (day == 1): result = result + "Mon "
		elif (day == 2): result = result + "Tue "
		elif (day == 3): result = result + "Wed "
		elif (day == 4): result = result + "Thu "
		elif (day == 5): result = result + "Fri "
		elif (day == 6): result = result + "Sat "
		elif (day == 7): result = result + "Sun "
	return result


def make_rating_chart(course_list, courseDB):
	section_list = []
	time_list = []
	for course in course_list:
		section = courseDB.get_opening_sections(
				course['subject'], course['catalog'])
		print section
		time_comp = []
		for component in section:
			time = []
			for name in component:
				weekly_event = []
				schedule = courseDB.get_time_schedule(course['subject'], \
						course['catalog'], name)
				for event in schedule[0]:
					event_time = convert_array(event[0]) + ' ' + str(event[1]) + \
							'-' + str(event[2])
					weekly_event.append(event_time)
				time.append(weekly_event)
			time_comp.append(time)
		time_list.append(time_comp)
		section_list.append(section)
	result = [time_list, section_list]
	return json.dumps(result)

@csrf_exempt
def index(request):
	courseDB = uwcoursedb.UWCourseDB(
			1161, 
			uwaterlooapi.UWaterlooAPI(api_key = get_apikey()))
	tool = scheduloo_core.Scheduloo(courseDB)

	if request.method == "POST":
		post_data = request.body
		body = json.loads(post_data)
		if body['command'] == 'check_course':
			return HttpResponse(check_course(body['course']['subject'],
				body['course']['catalog'], courseDB))
		if body['command'] == 'submit_course_list':
			return HttpResponse(make_rating_chart(body['course'], courseDB))
		if body['command'] == 'search':
			courses = []
			ratings = []
			for course in body['courses']:
				courses.append([str(course['subject']), str(course['catalog'])])
			for course in body['ratings']:
				ratings.append([])
				for component in course:
					ratings[-1].append([])
					for section in component:
						ratings[-1][-1].append(int(section))
			tool.set_courses(courses)
			tool.set_solver(ratings)
			result = tool.search_all(1000)
			plan_list = []
			for i in range(min(6, len(result))):
				plan = result[i]
				plan_list.append({})
				plan_list[-1]['value'] = plan[1]
				plan_list[-1]['courses'] = []
				plan = sorted(plan[0], key = lambda Vertex: Vertex.name)
				for section in plan:
					plan_list[-1]['courses'].append(section.name)
			return HttpResponse(json.dumps(plan_list))
				

	return render(request, 'scheduloo.html')
