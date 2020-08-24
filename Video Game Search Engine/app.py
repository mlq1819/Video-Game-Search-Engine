from result import tuplelist

parsed = []
key="6fe6fb576b0c7bef2364938b2248e1628759508d"
baseUrl="https://www.giantbomb.com/api/"
resource="games"
non_plural="game"
platforms = [21,9,43]
games = []
max_elements = 100
expected_fields = []
force_start = True
force_platform = 9
force_offset = 700
parse_blocks = []

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

#Either adds a new data field to expected_fields, or increments the element sharing the same name
def add_data_field(name):
	i = 0
	while i < len(expected_fields):
		datum = expected_fields[i]
		if datum[0] == name:
			expected_fields[i] = (datum[0], datum[1]+1)
			return
		i += 1
	t = (name, 1)
	expected_fields.append(t)
	return

#checks whether a particular field is a common field
def common_field(name):
	unsorted = []
	count = 0
	for datum in expected_fields:
		unsorted.append((datum[0],datum[1]))
		if datum[0] == name:
			count = datum[1]
	sorted = []
	while len(unsorted) > 0:
		max = 0
		for datum in unsorted:
			max = max(max, datum[1])
		for datum in unsorted:
			if datum[1] == max:
				sorted.append((datum[0], datum[1]))
				unsorted.remove(datum)
				break
	return count >= max(sorted[int(len(sorted) * 3 / 4)][1] - 1, 1)

#Gets a list of the common fields as tuples with the second index set to False
def common_fields_list():
	unsorted = []
	for datum in expected_fields:
		unsorted.append((datum[0],datum[1]))
	sorted = []
	while len(unsorted) > 0:
		max_value = 0
		for datum in unsorted:
			max_value = max(max_value, datum[1])
		for datum in unsorted:
			if datum[1] == max_value:
				sorted.append((datum[0], datum[1]))
				unsorted.remove(datum)
				break
	check = max(sorted[int(len(sorted) * 3 / 4)][1] - 1, 1)
	output = []
	for datum in sorted:
		if datum[1] >= check:
			output.append((datum[0], False))
	return output

#checks whether the data has not been added to the fields_list yet, and that if it is added, that it has not been marked True
def check_fields_list(list, name):
	i = 0
	while i < len(list):
		datum = list[i]
		if datum[0] == name:
			output = datum[1] == False
			list[i] = (datum[0], True)
			return output
		i += 1
	list.append((name, True))
	return True


#takes a string of results and adds games from the generated list
#results should be formatted as such: [{"Name":Data,"Name":Data,"Name":Data},{"Name":Data,"Name":Data,"Name":Data},{"Name":Data,"Name":Data,"Name":Data}]
def add_games(results):
	start = 0
	middle = 0
	end = 0
	index = 0
	at_bad = False
	print("Parsing " + non_plural + " data...")
	while index >= 0 and index < len(results):
		if results[index] == '[':
			index+=1
			while index < len(results) and results[index] != ']': #loop between game objects, within list of game objects
				if results[index] == '{': #found a game object
					output = []
					index+=1
					fields_list = []
					if len(games) > 5:
						fields_list = common_fields_list()
					while index < len(results) and results[index] != '}': #loop between fields of game object, within game object
						start = index
						middle = index
						end = index
						found_middle = False
						subobjects=[]
						while index < len(results) and results[index] != ',' and results[index] != '}': #loop within fields to find middle and end points
							if results[index] == '[' or results[index] == '{' or results[index] == '\"': #folder check
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
											while index+1 < len(results) and results[index] != '>':
												index += 1
											html_end = index
											to_fold = results[html_start:html_end+1]
										if to_fold == folding[-1] and (to_fold != '\"' or (to_fold == '\"' and index > 0 and results[index-1] != '\\')):
											folding.pop(-1)
										elif to_fold[0] == '<' and len(to_fold) > 1 and to_fold[1] != '\\':
											if to_fold[-3:-1] != "\\/":
												expected = "<\\/" + to_fold[1:-1]
												if ' ' in expected:
													expected = expected[:expected.index(' ')]
												expected = expected + '>'
												if expected != "<\\/img>" and expected != "<\\/area>" and expected != "<\\/base>" and expected != "<\\/br>" and expected != "<\\/col>" and expected != "<\\/command>" and expected != "<\\/embed>" and expected != "<\\/hr>" and expected != "<\\/input>" and expected != "<\\/keygen>" and expected != "<\\/link>" and expected != "<\\/meta>" and expected != "<\\/param>" and expected != "<\\/source>" and expected != "<\\/track>" and expected != "<\\/wbr>":
													folding.append(expected)
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
							elif results[index] == ':' and not found_middle:
								middle = index
								found_middle = True
							index+=1
						#At end of field; results[index] is either ',' (still in game object) or '}' (end of game object)
						end = index
						if found_middle and index < len(results):
							name = convert_to_type(results[start:middle])
							if check_fields_list(fields_list, name): #ensures that duplicate data is not found
								add_data_field(name)
								if len(subobjects) == 0:
									data = convert_to_type(results[middle+1:end])
									t = (name,data)
									output.append(t)
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
							else: #duplicate data has been found; need to double back and find the end of the current game
								print("Data glitch detected; attempting to rewind to end of last element...")
								print("\tData rewind started at index == " + str(index))
								index = start
								while index > 0 and index+2 < len(results) and results[index] != '}' and results[index+1] != ',' and results[index+2] != '{':
									index -= 1 #backtracking to probable end of last game; might cause some glitches but should prevent issues
								print("\tData rewind ended at index == " + str(index) + ": \"" + results[index:index+2] + '\"')
								if index > 0 and index + 2 < len(results):
									break
						if results[index] == ',':
							index+=1
					#At end of game; results[index] == '}'; note: most games will end with a "},{", though one will end with "}]"
					games.append(tuplelist(output))
					if games[-1].Has("name") and isinstance(games[-1].Get("name"), str):
						num_spaces = max(1, 64 - len(games[-1].Get("name")))
						spaces = ""
						while num_spaces > 0:
							spaces = spaces + ' '
							num_spaces -= 1
						print("\tCompleted parsing of " + non_plural + " with name \t\"" + (games[-1].Get("name")) + "\"" + spaces + " with " + str(len(games[-1].fields)) + " data fields")
						if games[-1].Get("name") == "A Week of Garfield":
							at_bad = True
					elif games[-1].Has("aliases"):
						if isinstance(games[-1].Get("aliases"), str):
							print("\tCompleted parsing of " + non_plural + " with alias \"" + (games[-1].Get("aliases")) + "\"\t with " + str(len(games[-1].fields)) + " data fields")
						else:
							print("\tCompleted parsing of " + non_plural + " with alias \"" + (games[-1].Get("aliases"))[0] + "\"\t with " + str(len(games[-1].fields)) + " data fields")
					else:
						print("\tCompleted parsing of game with " + str(games[-1].GetFieldName(0)) + "\t with " + str(len(games[-1].fields)) + " data fields")
					while results[index] == '}' or results[index] == ',':
						index+=1
				if index < len(results) and results[index] != '{':
					index+=1
		#Possibly at end of list, results[index] either equals ']' or is out of range
		index+=1
	print("Completed parsing of " + non_plural + " data")

def recurse_tuple1(tuple, depth):
	output = ""
	tab_string = "\t"
	i = depth
	while i > 0:
		tab_string = tab_string + '\t'
		i -= 1
	if len(tuple[1]) > 0:
		output = output + tab_string + '[' + '\n'
		do_divider = False
		for item in tuple[1]:
			if do_divider:
				output = output + tab_string + ',' + '\n'
			else:
				do_divider = True
			output = output + recurse_tuple1(item, depth+1) + '\n'
		output = output + tab_string + ']' + '\n'
	else:
		output += tab_string
		max_len = 128
		if len(tuple[0]) >= max_len:
			output += "~len=" + str(len(tuple[0])) + "~ " + tuple[0][:max_len]
		else:
			output += tuple[0]
		output += '\n'
	return output

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
						folding_indices = []
						folding_blocks = [] #list of block tuples on the current level
						saved_lists = [] #list of lists of block tuples
						root = ("",[])
						if response[index] == '[':
							folding.append(']')
						elif response[index] == '{':
							folding.append('}')
						folding_indices.append(index)
						while len(folding)>0:
							index+=1
							temp = ""
							if force_start and len(response) == index + 1:
								for block in folding_blocks:
									temp = temp + recurse_tuple1(block, 0)
								print(temp)
								break
							if response[index] == folding[-1]:
								folding.pop(-1)
								if force_start:
									current = (response[folding_indices[-1]:index+1], folding_blocks)
									folding_blocks = []
									if len(saved_lists) > 1:
										folding_blocks = saved_lists[-1]
										saved_lists.pop(-1)
										folding_blocks.append(current)
									else:
										root = current
								folding_indices.pop(-1)
							else:
								if response[index] == '[':
									folding.append(']')
									folding_indices.append(index)
									saved_lists.append(folding_blocks)
									folding_blocks = []
								elif response[index] == '{':
									folding.append('}')
									folding_indices.append(index)
									saved_lists.append(folding_blocks)
									folding_blocks = []
					elif response[index] == ':' and not found_middle:
						middle = index
						found_middle = True
					index+=1
				end = index
				name = convert_to_type(response[start:middle])
				print("\tCompleted section with name \"" + name + "\"")
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
	if force_start:
		print("Forced start is on: platform=" + str(force_platform) + "; offset=" + str(force_offset))
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like
	batch_number = 0
	print("Requires batches for " + str(len(platforms)) + " platforms:")
	plat_num = 0
	for platform in platforms:
		print("\t> " + str(platform))
	for platform in platforms:
		plat_num += 1
		num_results = max_elements
		offset = 0
		base_batch_number = batch_number
		expected_batches = -1
		if (not force_start) or force_platform == platform:
			if force_start and not force_offset == "any":
				offset = force_offset
			while num_results == max_elements and ((not force_start) or (offset == force_offset) or (force_offset == "any")):
				base_percent = (plat_num - 1) / len(platforms)
				extra_percent = 0.0
				if offset > 0 and expected_batches > 0:
					extra_percent = ((batch_number - base_batch_number) / expected_batches) / len(platforms)
				final_percent = round((base_percent + extra_percent) * 100, 2)
				batch_number += 1
				print(str(final_percent) + "% Completed")
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
				if offset > 0 and expected_batches > 0:
					print("Retrieving data batch " + str(batch_number) + " of " + str(int(expected_batches + base_batch_number)) + " from API...", )
				else:
					print("Retrieving data batch " + str(batch_number) + " from API...")
				response = requests.get(url, headers=headers)
				print("... Retrieved data batch " + str(batch_number) + " from API")
				results = parse(response.text)
				if offset == 0:
					expected_batches = results.Get("number_of_total_results")
					expected_batches = round(expected_batches / max_elements + 0.4999, 0)
					print("Expecting " + str(expected_batches) + " batches for platform " + str(platform))
				num_results = results.Get("number_of_page_results")
				if response.status_code == 200 or response.status_code == 301:
					add_games(results.Get("results"))
				else:
					hasnt_failed = False
					print("Error code " + str(response.status_code))
					print(response.reason)
				offset = offset + num_results
	print("100% Completed!")
	if hasnt_failed:
		app.run('localhost',5050) #5050 is what is currently set in the project Debug port number settings; both must be changed if either is
	else:
		print("Failed to run application")