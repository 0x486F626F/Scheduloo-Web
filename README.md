# Scheduloo-Web

Life is tough — we always have problems to schedule an efficient calendar that
maximize our productivity and efficiency. That’s where our idea of scheduloo
came along.

Scheduloo is an online web application that can help students in University of
Waterloo to get a satisfied class schedule without much effort.

Students can type in their intended course numbers and then with a simply click
of “next”, this system will display all available sessions for each course on a
one page along with their time and ask students to rate them with sliders. After
that, click on “Scheduloo”, the system will automatically calculate 6 best
combinations of the courses entered based on their time conflicts and students’
intentions. 

Scheduloo is very easy to use and save students from lots of handwritten work
for scheduling courses.

	The data we use for Scheduloo comes from the University of Waterloo Open
	Data API ( check https://api.uwaterloo.ca/). The API provides large amount
	of information about the university’s services, including courses, food,
	weather, news, etc. The information is organized in a tree structure and it
	is easy for programmers to access it. In addition, we use Microsoft Azure
	Cloud service to host our website.

	The calculation algorithm is the core for this application and can be
	applied to more generalized scheduling in the future, for example, to
	schedule other university courses, company conferences, daily work, etc.
	However, we don’t have access to the data so so far we only built this very
	focused schedule application as a demonstration of our idea and algorithm.
