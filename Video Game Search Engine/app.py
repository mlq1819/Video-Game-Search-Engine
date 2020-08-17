from result import result
from game import game

parsed = []
key="6fe6fb576b0c7bef2364938b2248e1628759508d"
baseUrl="https://www.giantbomb.com/api/"
resource="games"
platforms = [21,9,43]
games = []

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
					if results[index] == '[':
						while results[index] != ']':
							if results[index] == ',':
								subobjects.append(index)
							index+=1
					if results[index] == '{':
						while results[index] != '}':
							index+=1
					if results[index] == ':':
						middle = index
					index+=1
				name = results[start:middle]
				data
				if len(subobjects) == 0:
					data = results[middle+1, end]
				else:
					i2 = 0
					data = []
					while i2 < len(subojects):
						if i2 == 0:
							data.append(results[middle+1:subobjects[i2]])
						else:
							data.append(results[subobjects[i2-1]+1:subobjects[i2]])
						i2+=1
				games.append(game(name, data))
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
					if response[index] == '[':
						while response[index] != ']':
							index+=1
					if response[index] == '{':
						while response[index] != '}':
							index+=1
					if response[index] == ':':
						middle = index
					index+=1
				name = response[start:middle]
				data = response[middle+1:end]
				output.append(result(name, data))
		index+=1
	return output

#Entry point into application; downloads and parses API data before starting the web application
if __name__ == '__main__':
	hasnt_failed = True
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like
	for platform in platforms:
		num_results = 100
		offset = 0
		while(num_results == 100):
			url = baseUrl + resource + "/?api_key=" + key + "&format=json"
			if offset > 0:
				url = url + "&offset=" + str(offset)
			url = url + "&platforms=" + str(platform)
			#https://www.giantbomb.com/api/games/?api_key=6fe6fb576b0c7bef2364938b2248e1628759508d&format=json&platforms=21
			print(url)
			response = requests.get(url, headers=headers)
			results = parse(response)
			num_results = len(results)
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