from result import resultitem
from game import game

parsed = []
key="6fe6fb576b0c7bef2364938b2248e1628759508d"
baseUrl="https://www.giantbomb.com/api/"
resource="games"
platforms = [21,9,43]
games = []
max_elements = 100

import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title="Welcome")

@app.route('/result', methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		result = request.form
		#TODO - perform actions on result and/or define items to match the search keywords
		return render_template("result.html", items = result)
	else:
		return index()

def is_numeric(str):
	dot=False
	first=True
	for c in str:
		if not c.isdigit():
			if c == '.':
				if dot:
					return False
				else:
					dot = True
			elif not first or c != '-':
				return False
		first = False
	return True

	
#either removes quotation marks and returns a string, or attempts to convert to an int
def convert_to_type(object):
	if object[0] == '"' and object[len(object)-1] == '"':
		return object[1:len(object)-1]
	else:
		if is_numeric(object):
			return int(object)
		else:
			return object

#takes a string of results and adds games from the generated list
#results should be formatted as such: [{"Name":Data,"Name":Data,"Name":Data},{"Name":Data,"Name":Data,"Name":Data},{"Name":Data,"Name":Data,"Name":Data}]
def add_games(results):
	start = 0
	middle = 0
	subobjects=[]
	end = 0
	index = 0
	while index >= 0 and index < len(results):
		if results[index] == '[':
			index+=1
			while results[index] != ']':
				start = index
				while results[index] != ',':
					if response[index] == '[' or response[index] == '{':
						folding = []
						if response[index] == '[':
							folding.append(']')
						else:
							folding.append('}')
						while len(folding)>0:
							index+=1
							if response[index] == folding[-1]:
								del folding[-1]
							elif len(folding) == 1 and folding[-1] == ']' and response[index] == ',':
								subobjects.append(index)
							else:
								if response[index] == '[':
									folding.append(']')
								elif response[index] == '{':
									folding.append('}')
					if results[index] == ':':
						middle = index
					index+=1
				end = index
				name = convert_to_type(results[start:middle])
				data
				if len(subobjects) == 0:
					data = convert_to_type(results[middle+1, end])
				else:
					i2 = 0
					data = []
					while i2 < len(subojects):
						if i2 == 0:
							data.append(convert_to_type(results[middle+1:subobjects[i2]]))
						else:
							data.append(convert_to_type(results[subobjects[i2-1]+1:subobjects[i2]]))
						i2+=1
				t = (name,data)
				games.append(game(t))
		index+=1

#Should convert information from response into a list of result objects
#response should be formatted as such: {"Name":Data,"Name":Data,"Name":Data}
def parse(response):
	start = 0
	middle = 0
	end = 0
	index = 0
	output = []
	while index >= 0 and index < len(response):
		if response[index] == '{':
			index+=1
			while response[index] != '}':
				start = index
				while response[index] != ',':
					if response[index] == '[' or response[index] == '{':
						folding = []
						if response[index] == '[':
							folding.append(']')
						else:
							folding.append('}')
						while len(folding)>0:
							index+=1
							if response[index] == folding[-1]:
								del folding[-1]
							else:
								if response[index] == '[':
									folding.append(']')
								elif response[index] == '{':
									folding.append('}')
					if response[index] == ':':
						middle = index
					index+=1
				end = index
				name = convert_to_type(response[start:middle])
				data = convert_to_type(response[middle+1:end])
				t = (name,data)
				output.append(resultitem(t))
				index+=1
		index+=1
	return output

#Entry point into application; downloads and parses API data before starting the web application
if __name__ == '__main__':
	hasnt_failed = True
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like
	for platform in platforms:
		num_results = max_elements
		offset = 0
		while(num_results == max_elements):
			url = baseUrl + resource + "/?api_key=" + key + "&format=json"
			if offset > 0:
				url = url + "&offset=" + str(offset)
			url = url + "&platforms=" + str(platform)
			#https://www.giantbomb.com/api/games/?api_key=6fe6fb576b0c7bef2364938b2248e1628759508d&format=json&platforms=21
			print(url)
			response = requests.get(url, headers=headers)
			results = parse(response.text)
			num_results = results.Get("number_of_page_results")
			if response.status_code == 200 or response.status_code == 301:
				add_games(results.Get("results"))
			else:
				hasnt_failed = False
				print("Error code " + str(response.status_code))
				print(response.reason)
			offset = offset + num_results
	if hasnt_failed:
		app.run('localhost',5050) #5050 is what is currently set in the project Debug port number settings; both must be changed if either is
	else:
		print("Failed to run application")