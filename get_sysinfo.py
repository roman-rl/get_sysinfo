"""
Small script to get system information and 
make a HTML file with this info
"""

from pathlib import Path
import re

html_start="""
<!DOCTYPE html>
<html>
"""

html_header="""
	<head>
		<meta charset="utf-8">
		<title> </title>
	</head>
"""
html_body_start="""
	<body>
"""
	
html_body_end="""
	</body>
"""

html_end="""
</html>
"""

def main():
	
	text_html = ""

	def output_html(html_body):
		"""
		Joins all html parts,
		after join html will save it in output.html
		"""
		html_total = html_start + html_header + html_body_start + html_body + html_body_end + html_end
		with open("output.html","w") as file:
			file.write(html_total)

	def wrap_p(text):
		"""
		Wraps text inside of html paragraph tags
		"""
		return "<p>" + text + "</p>"
	

	def cpu_method(data):
		"""
		Method to get number of processors
		"""
		processors = re.findall(r'processor.*',data)
		num_processors = str(len(processors))
		return num_processors

	def version_method(data):
		"""
		Method to get first 3 words of version
		information
		"""
		return " ".join(data.split(" ")[0:3])

	def uptime_method(data):
		"""
		Method to get time system is up
		"""
		uptime = float(data.split(" ")[0])

		minute_counter = 60
		hour_counter = 60*minute_counter
		day_counter = 24*hour_counter

		days_reminder = int(uptime) % day_counter
		minutes_reminder = int(days_reminder) % hour_counter

		days = str(int(uptime/day_counter))
		hours = str(int(int(days_reminder)/hour_counter))
		minutes = str(int(int(minutes_reminder)/minute_counter))

		return "{} days and {} hours with {} minutes".format(days,hours,minutes) 

	#Main directory to get information in Linux System
	procDir = Path("/proc/")

	#Dicts with message to show in html and method where it
	#will get information 

	cpu_dict = {"message" : "Number of processors found in system is: ",
					"method" : cpu_method  }

	version_dict = {"message" : "Operative System Info: ",
						"method" : version_method }

	uptime_dict = {"message" : "System has been for: ",
							"method" : uptime_method }

	#Dict where it will store file to check as key,
	#as value will contain another dict with information
	#about message to display and a method to get
	#information from system
	info_dict = {"cpuinfo" : cpu_dict	,
					"version" : version_dict,
					"uptime" : uptime_dict}

	for key,value in info_dict.items():

		file_info = procDir / key

		with open(file_info) as file:
			data = file.read()

		#Get message to dislpay and apply method to
		#get information from system
		mensaje_info = value["message"]
		sys_info = value["method"](data) 

		#Wrap all information in HTML
		text_html = text_html + " " + wrap_p(mensaje_info + sys_info)

	#Save in HTML file
	output_html(text_html)
	
if __name__ == "__main__":
	main()
