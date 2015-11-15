import datetime
import evaluation
import event
import sets
import re

class Scheduloo:
	def __init__(self, db):
		self.db = db

	def set_courses(self, courses): #{{{
		self.courses = courses
		self.opening_sections = []
		for course in courses:
			self.db.update_course(course[0], course[1])
			self.opening_sections.append(self.db.get_opening_sections(course[0], course[1]))
		for course in courses:
			self.db.update_course(course[0], course[1])
	#}}}

	def add_conflict(self, key1, key2): #{{{
		pair1 = [key1, key2]
		pair2 = [key2, key1]
		if pair1 in self.conflicts or pair2 in self.conflicts: return None
		self.conflicts.append(pair1)
	#}}}

	def set_solver(self, ratings): #{{{
		self.solver = evaluation.GraphSolver()
		self.total_component = 0
		all_sections = []
		self.conflicts = []
		for i in range(len(self.opening_sections)):
			course_name = self.courses[i][0] + self.courses[i][1]
			for j in range(len(self.opening_sections[i])):
				self.total_component += 1
				length = len(self.opening_sections[i][j])
				for k in range(length):
					all_sections.append([
						self.courses[i][0], self.courses[i][1], 
						self.opening_sections[i][j][k], ratings[i][j][k]])
					for l in range(k):
						self.add_conflict(
								course_name + self.opening_sections[i][j][k],
								course_name + self.opening_sections[i][j][l])

			for main_event in self.opening_sections[i][0]:
				related_sections = self.db.get_related_sections(
						self.courses[i][0], self.courses[i][1], main_event)
				print self.opening_sections
				print related_sections
				for j in range(1, len(self.opening_sections[i])):
					for section in self.opening_sections[i][j]:
						print j
						if section not in related_sections[j]:
							self.add_conflict(
									course_name + main_event,
									course_name + section)
		all_sections = sorted(all_sections, key = lambda section: - section[3])
		for section in all_sections:
			self.solver.add_event(section[0] + section[1] + section[2], section[3])
		for key in self.conflicts:
			self.solver.add_conflict(key[0], key[1])
			
		for i in range(len(all_sections)):
			for j in range(i):
				name1 = all_sections[i][0] + \
						all_sections[i][1] + \
						all_sections[i][2]
				name2 = all_sections[j][0] + \
						all_sections[j][1] + \
						all_sections[j][2]
				schedule1 = self.get_time_schedule(
						all_sections[i][0], 
						all_sections[i][1], 
						all_sections[i][2]) 
				schedule2 = self.get_time_schedule(
						all_sections[j][0], 
						all_sections[j][1], 
						all_sections[j][2]) 
				conflict_time = event.get_total_conflict(schedule1, schedule2)
				if conflict_time > 0:
					self.solver.add_conflict(name1, name2)

	#}}}

	def get_time_schedule(self, subject, catalog, section): #{{{
		result = self.db.get_time_schedule(subject, catalog, section)
		schedule = [[], []]
		for weekly in result[0]:
			schedule[0].append(
					event.weekly_event(weekly[0], weekly[1], weekly[2]))
		for onetime in result[1]:
			schedule[1].append(
					event.onetime_event(onetime[0], onetime[1], onetime[2]))
		return schedule
	#}}}

	def search_all(self, num_plans = 10):
		result = self.solver.search_all(self.total_component, num_plans)
		return result

	def generate_ics_file(self, result, numb):
		headers = ["BEGIN:VCALENDAR\n",
				"PRODID:-//Google Inc//Google Calendar 70.9054//EN\n",
				"VERSION:2.0\n"]
		big_string = ""
		for h in headers:
			big_string += h

		for component in result:
			name = component.name
			course = name[:name.find(" ") - 3]
			section = name[name.find(" ") - 3:]
			r = re.compile("([a-zA-Z]+)([0-9]+)")
			subject_catalog = r.match(course)
			subject = subject_catalog.group(1)
			catalog = subject_catalog.group(2)
			schedule = self.db.get_time_schedule(subject, catalog, section)
			for weekly_event in schedule[0]:
				big_string = self.add_weekly_event(big_string, weekly_event, subject, catalog, section)
			for onetime_event in schedule[1]:
				big_string = self.add_onetime_event(big_string, onetime_event, subject, catalog, section)

		big_string += "END:VCALENDAR\n"
		file = open("test_schedule" + str(numb) + ".ics", 'w')
		file.write(big_string)
		file.close()


	def add_weekly_event(self, s, event, subject, catalog, section):
		s += "BEGIN:VEVENT\n"
		start_datetime = "DTSTART:" + datetime.datetime(2016, 1, 3 + event[0][0], 0, 0).strftime('%Y%m%d') + "T" + event[1].strftime('%H%M%S') + "\n"
		end_datetime = "DTEND:" + datetime.datetime(2016, 1, 3 + event[0][0], 0, 0).strftime('%Y%m%d') + "T" + event[2].strftime('%H%M%S') + "\n"
		s += start_datetime
		s += end_datetime
		rule = "RRULE:FREQ=WEEKLY;UNTIL=20160430T153000Z;BYDAY="
		for i in event[0]:
			if (i == 1): rule += "MO,"
			elif (i == 2): rule += "TU,"
			elif (i == 3): rule += "WE,"
			elif (i == 4): rule += "TH,"
			elif (i == 5): rule += "FR,"
		rule = rule[:-1] + "\n"
		s += rule
		location = self.db.get_course_location(subject, catalog, section)
		s += "LOCARION:" + location[0] + " " + location[1] + "\n"
		s += "SUMMARY:" + subject + catalog + " " + section.replace(' ', '') + "\n"
		s += "TRANSP:OPAQUE\n"
		s += "END:VEVENT\n"
		return s

	def add_onetime_event(self, s, event, subject, catalog, section):
		s += "BEGIN:VEVENT\n"
		start_datetime = "DTSTART:" + event[0].strftime('%Y%m%d') + "T" + event[1].strftime('%H%M%S') + "\n"
		end_datetime = "DTEND:" + event[0].strftime('%Y%m%d') + "T" + event[2].strftime('%H%M%S') + "\n"
		s += start_datetime
		s += end_datetime
		location = self.db.get_course_location(subject, catalog, section)
		s += "LOCARION:" + location[0] + " " + location[1] + "\n"
		s += "SUMMARY:" + subject + catalog + " " + section.replace(' ', '') + "\n"
		s += "TRANSP:OPAQUE\n"
		s += "END:VEVENT\n"
		return s
