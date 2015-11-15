import datetime

class onetime_event:
	def __init__(self, date, start_time, end_time):
		self.date = date
		self.start_time = start_time
		self.end_time = end_time

class weekly_event:
	def __init__(self, weekdays, start_time, end_time):
		self.weekdays = weekdays
		self.start_time = start_time
		self.end_time = end_time

def time_conflict(event1, event2):
	today = datetime.date.today()
	combine = datetime.datetime.combine
	zero = datetime.timedelta(seconds = 0)

	start_time1 = combine(today, event1.start_time)
	end_time1 = combine(today, event1.end_time)
	start_time2 = combine(today, event2.start_time)
	end_time2 = combine(today, event2.end_time)
	if (start_time1 < start_time2):
		return max(zero, end_time1 - start_time2).seconds / 60
	else:
		return max(zero, end_time2 - start_time1).seconds / 60

def weekly_weekly_conflict(schedule1, schedule2):
	total = 0
	for event1 in schedule1:
		for event2 in schedule2:
			for day in range(1, 6, 1):
				if day in event1.weekdays and day in event2.weekdays:
					total += time_conflict(event1, event2)
	return total

def onetime_onetime_conflict(schedule1, schedule2):
	total = 0
	for event1 in schedule1:
		for event2 in schedule2:
			if event1.date == event2.date:
				total += time_conflict(event1, event2)
	return total

def onetime_weekly_conflict(schedule1, schedule2):
	total = 0
	for event1 in schedule1:
		for event2 in schedule2:
			if event1.date.isoweekday() % 7 in event2.weekdays:
				total += time_conflict(event1, event2)
	return total

def get_total_conflict(schedule1, schedule2, num_weeks = 12):
	return weekly_weekly_conflict(schedule1[0], schedule2[0]) * num_weeks + \
			onetime_onetime_conflict(schedule1[1], schedule2[1]) + \
			onetime_weekly_conflict(schedule1[1], schedule2[0]) + \
			onetime_weekly_conflict(schedule2[1], schedule1[0])

