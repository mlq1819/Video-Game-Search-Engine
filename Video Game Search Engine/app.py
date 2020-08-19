from result import tuplelist

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
	if len(str) == 0:
		return False
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
	if len(object)>=2 and object[0] == '"' and object[len(object)-1] == '"' and object.count('\"') == 2:
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
	end = 0
	index = 0
	print("Parsing game data...")
	toggle_print = False
	while index >= 0 and index < len(results):
		if results[index] == '[':
			index+=1
			while index < len(results) and results[index] != ']': #loop between game objects, within list of game objects
				if results[index] == '{': #found a game object
					output = []
					index+=1
					if toggle_print:
						if index + 50 < len(results):
							print("\tAt game starting with \"" + results[index:index+50] + "\"")
						elif index + 25 < len(results):
							print("\tAt game starting with \"" + results[index:index+25] + "\"")
						elif index + 10 < len(results):
							print("\tAt game starting with \"" + results[index:index+10] + "\"")
					while index < len(results) and results[index] != '}': #loop between fields of game object, within game object
						start = index
						middle = index
						end = index
						found_middle = False
						subobjects=[]
						if toggle_print:
							if index + 10 < len(results):
								print("\t\tAt section starting with \"" + results[index:index+10] + "\"")
							elif index + 6 < len(results):
								print("\t\tAt section starting with \"" + results[index:index+6] + "\"")
							elif index + 3 < len(results):
								print("\t\tAt section starting with \"" + results[index:index+3] + "\"")
							elif index < len(results):
								print("\t\tAt section starting with \"" + results[index] + "\"")
						while index < len(results) and results[index] != ',' and results[index] != '}': #loop within fields to find middle and end points
							if results[index] == '[' or results[index] == '{' or results[index] == '\"': #folder check; CURRENTLY BROKEN, somehow backtracks
								#print("\t\t\tOpened fold at index = " + str(index))
								folding = []
								if results[index] == '[':
									folding.append(']')
								elif results[index] == '\"':
									folding.append('\"')
								elif results[index] == '{':
									folding.append('}')	
								if index+1 < len(results) and results[index+1] == '<': #html folding loop
									while len(folding)>0:
										index+=1
										to_fold = results[index]
										if results[index] == '<':
											html_start = index
											while results[index] != '>':
												index += 1
											html_end = index
											to_fold = results[html_start:html_end+1]
										if to_fold == folding[-1]:
											folding.pop(-1)
										elif to_fold[0] == '<' and len(to_fold) > 1 and to_fold[1] != '\\':
											to_fold = "<\\/" + to_fold[1:]
											folding.append(to_fold)
								else:
									while len(folding)>0: #main folding loop
										index+=1
										if results[index] == folding[-1]:
											folding.pop(-1)
										elif len(folding) == 1 and (folding[-1] == ']' or folding[-1] == '}') and results[index] == ',':
											subobjects.append(index)
										else:
											if (results[index] == '\"' and index==0) or (results[index] == '\"' and results[index-1]!='\''):
												folding.append('\"')
											elif results[index] == '[':
												folding.append(']')
											elif results[index] == '{':
												folding.append('}')
								#print("\t\t\tClosed fold at index = " + str(index))
							elif results[index] == ':' and not found_middle:
								middle = index
								found_middle = True
								#print("\t\t\tFound Middle: \"" + results[start:middle] + "\"")
							index+=1
						#At end of field; results[index] is either ',' (still in game object) or '}' (end of game object)
						end = index
						if toggle_print:
							print("\t\t\tStepped indices from " + str(start) + " to " + str(middle) + " to " + str(end))
						if found_middle and index < len(results):
							name = convert_to_type(results[start:middle])
							if len(subobjects) == 0:
								data = convert_to_type(results[middle+1:end])
								t = (name,data)
								output.append(t)
								if toggle_print:
									print("\t\t\tFilled field \"" + name + "\" with datum: " + str(data))
							else:
								i2 = 1
								data = []
								data.append(convert_to_type(results[middle+2:subobjects[0]]))
								while i2 < len(subobjects):
									data.append(convert_to_type(results[subobjects[i2-1]+1:subobjects[i2]]))
									i2+=1
								data.append(convert_to_type(results[subobjects[-1]+1:end-1]))
								t = (name,data)
								output.append(t)
								if toggle_print:
									data_str = "["
									for datum in data:
										data_str = data_str + "\n\t\t\t\t" + str(datum)
									data_str = data_str + "\n\t\t\t]"
									print("\t\t\tFilled field \"" + name + "\" with data: " + data_str)
						if results[index] == ',':
							index+=1
					#At end of game; results[index] == '}'; note: most games will end with a "},{", though one will end with "}]"
					games.append(tuplelist(output))
					toggle_print = False
					if games[-1].Has("name") and isinstance(games[-1].Get("name"), str):
						print("\tCompleted parsing of game with name \"" + (games[-1].Get("name")) + "\"\t with " + str(len(games[-1].fields)) + " fields")
						if games[-1].Get("name") == "Faria: A World of Mystery and Danger!":
							toggle_print = True
					elif games[-1].Has("aliases"):
						if isinstance(games[-1].Get("aliases"), str):
							print("\tCompleted parsing of game with alias \"" + (games[-1].Get("aliases")) + "\"\t with " + str(len(games[-1].fields)) + " fields")
						else:
							print("\tCompleted parsing of game with alias \"" + (games[-1].Get("aliases"))[0] + "\"\t with " + str(len(games[-1].fields)) + " fields")
					else:
						print("\tCompleted parsing of game with " + str(games[-1].GetFieldName(0)) + "\t with " + str(len(games[-1].fields)) + " fields")
					while results[index] == '}' or results[index] == ',':
						index+=1
				if index < len(results) and results[index] != '{':
					index+=1
		#Possibly at end of list, results[index] either equals ']' or is out of range
		index+=1
	print("Completed parsing of game data")

#Should convert information from response into a list of result objects
#response should be formatted as such: {"Name":Data,"Name":Data,"Name":Data}
def parse(response):
	start = 0
	middle = 0
	end = 0
	index = 0
	output = []
	print("Parsing response data...")
	while index >= 0 and index < len(response):
		if response[index] == '{':
			index+=1
			while index < len(response) and response[index] != '}' and response[index] != ']':
				start = index
				if start + 10 < len(response):
					print("\tAt section starting with \"" + response[start:start+10] + "\"")
				found_middle = False
				while response[index] != ',' and response[index] != '}': #loop within fields to find middle and end points
					if response[index] == '[' or response[index] == '{': #folder loop
						folding = []
						if response[index] == '[':
							folding.append(']')
						elif response[index] == '{':
							folding.append('}')
						while len(folding)>0:
							index+=1
							if response[index] == folding[-1]:
								folding.pop(-1)
							else:
								if response[index] == '[':
									folding.append(']')
								elif response[index] == '{':
									folding.append('}')
					elif response[index] == ':' and not found_middle:
						middle = index
						found_middle = True
					index+=1
				end = index
				name = convert_to_type(response[start:middle])
				data = convert_to_type(response[middle+1:end])
				t = (name,data)
				output.append(t)
				index+=1
		index+=1
	print("Completed parsing of data")
	return tuplelist(output)

#Entry point into application; downloads and parses API data before starting the web application
if __name__ == '__main__':
	hasnt_failed = True
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like
	batch_number = 1
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
			if offset > 0:
				print(resource + " : platform " + str(platform) + " : offset " + str(offset))
			else:
				print(resource + " : platform " + str(platform))
			print("Retrieving data batch " + str(batch_number) + " from API...")
			response = requests.get(url, headers=headers)
			print("... Retrieved data batch " + str(batch_number) + " from API")
			batch_number += 1
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