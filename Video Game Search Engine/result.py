class tuplelist(object):
    """result object containing a list of fields"""

    #takes in a list of tuples[2]
    def __init__(self, fields):
        self.fields = fields

    def Get(self, field):
        for tuple in self.fields:
            if tuple[0] == field:
                return tuple[1]
        return None

    def Has(self, field):
        for tuple in self.fields:
            if tuple[0] == field:
                return True
        return False

    def GetFieldName(self, index):
        if index < len(self.fields):
            return self.fields[index][0]
        return None

class countset(object):
    """countset set containing a list of strings with counters applied to them; each object in countset.set is a (string,int) tuple"""

    #default constructor
    def __init__(self):
        self.set = []
        self.sorted = True

    #adds a new string to the set, or increases the occurance of the set
    def Add(self, word):
        i = 0
        word = word.upper()
        while i < len(self.set):
            tup = self.set[i]
            if word == tup[0][0]:
                self.set[i] = (tup[0], tup[1] + 1)
                if self.sorted:
                    if i > 0 and self.set[i][1] > self.set[i-1][1]:
                        self.sorted = False
                    if i+1 < len(self.set) and self.set[i][1] < self.set[i+1][1]:
                        self.sorted = False
                return True
            i += 1
        self.set.append(((word, []), 1))
        self.sorted = False
        return True

    #performs the Add function on a set of strings
    def AddSet(self, strset):
        count = 0
        for str in strset:
            if self.Add(str):
                count += 1
        return count

    #adds a given phrase to all words in the phrase
    def AddPhrase(self, phrase):
        words = countset.BreakTextBlock(phrase)
        count = 0
        for word in words:
            i = 0
            while i < len(self.set):
                tup = self.set[i]
                if word == tup[0][0]:
                    list = tup[0][1]
                    list.append(phrase)
                    self.set[i] = ((word, list), tup[1])
                    count += 1
                    break
                i+=1
        return count

    #decrements an object from the set, or deletes it entirely
    def Remove(self, word):
        i = 0
        word = word.upper()
        while i < len(self.set):
            tup = self.set[i]
            if word == tup[0][0]:
                if tup[1] > 1:
                    self.set[i] = (tup[0], tup[1] - 1)
                    if self.sorted:
                        if i > 0 and self.set[i][1] > self.set[i-1][1]:
                            self.sorted = False
                        if i+1 < len(self.set) and self.set[i][1] < self.set[i+1][1]:
                            self.sorted = False
                else:
                    self.set.pop(i)
                return True
            i += 1
        return False
    
    #performs the Remove function on a set of strings
    def RemoveSet(self, strset):
        count = 0
        for str in strset:
            if self.Remove(str):
                count += 1
        return count

    #removes a given phrase from all words in the phrase
    def RemovePhrase(self, phrase):
        words = countset.BreakTextBlock(phrase)
        count = 0
        for word in words:
            i = 0
            while i < len(self.set):
                tup = self.set[i]
                if word == tup[0][0]:
                    list = tup[0][1]
                    list.remove(phrase)
                    self.set[i] = ((word, list), tup[1])
                    count += 1
                    break
                i+=1
        return count

    #checks whether a particular object exists in the set
    def Has(self, word):
        word = word.upper()
        for tup in self.set:
            if word == tup[0]:
                return True
        return False
    
    #returns the number of occurances of an object in the set
    def Get(self, word):
        word = word.upper()
        for tup in self.set:
            if word == tup[0]:
                return tup[1]
        return 0

    #returns the subset of objects with at most the given number of occurances
    def DoubleSubset(self, num):
        output = []
        for tup in self.set:
            if tup[1] <= num:
                output.append((tup[0],tup[1]))
        return output
    
    #returns the subset of strings with at most the given number of occurances
    def Subset(self, num):
        output = []
        for tup in self.set:
            if tup[1] <= num:
                output.append(tup[0])
        return output

    def partition(self, arr, low, high):
        i = (low-1)         # index of smaller element
        pivot = arr[high][1]     # pivot
 
        for j in range(low, high):
 
            # If current element is smaller than or
            # equal to pivot
            if arr[j][1] <= pivot:
 
                # increment index of smaller element
                i = i+1
                arr[i], arr[j] = arr[j], arr[i]
 
        arr[i+1], arr[high] = arr[high], arr[i+1]
        return (i+1)

    def quickSort(self, arr, low, high):
        if len(arr) == 1:
            return
        if low < high:
 
            # pi is partitioning index, arr[p] is now
            # at right place
            pi = self.partition(arr, low, high)
 
            # Separately sort elements before
            # partition and after partition
            self.quickSort(arr, low, pi-1)
            self.quickSort(arr, pi+1, high)
        return

    def reverse(self):
        i = 0
        while i < int(len(self.set) / 2):
            j = -1 * (i + 1)
            self.set[i], self.set[j] = self.set[j], self.set[i]
            i += 1

    #sorts the set by occurance rate
    def Sort(self):
        print("\t\t\tSorting " + str(len(self.set)) + " words...")
        self.quickSort(self.set, 0, len(self.set)-1)
        self.reverse()
        self.sorted = True
        print("\t\t\tCompleted sorting")
        return

    #gets and returns the Average occurance number
    def Average(self):
        if len(self.set) == 0:
            return None
        sum = 0
        for item in self.set:
            sum += item[1]
        return sum / len(self.set)

    #gets and returns the Median occurance number
    def Median(self):
        if len(self.set) == 0:
            return None
        while not self.sorted:
            self.Sort()
        base_index = int(len(self.set) / 2)
        if len(self.set) % 2 == 0:
            return (self.set[base_index-1][1] + self.set[base_index][1]) / 2
        else:
            return self.set[base_index][1]

    #returns the occurance number at the given percentile (between 0 and 100)
    def Percentile(self, percentile):
        if percentile <= 0 or percentile > 100:
            return None
        while not self.sorted:
            self.Sort()
        fraction = percentile / 100
        index = int(fraction * len(self.set))
        if len(self.set) % int(100 / percentile) == 0 and index > 0:
            return (self.set[index-1][1] + self.set[index][1]) / 2
        else:
            return self.set[index][1]

    #extracts text from html code and converts it into a single string
    @staticmethod
    def ExtractFromHTML(block):
        output = ""
        index = 0
        start = 0
        while index < len(block):
            start = index
            if block[index] == '<':
                output += block[start:index]
                start = index
                folding = []
                first_loop = True
                inside_text = False
                while len(folding)>0 or first_loop:
                    if first_loop:
                        first_loop = False
                    else:
                        index+=1
                    if block[index] == '<':
                        html_start = index
                        while index+1 < len(block) and block[index] != '>':
                            index += 1
                        html_end = index
                        to_fold = block[html_start:html_end+1]
                        if len(folding) > 0 and to_fold == folding[-1]:
                            folding.pop(-1)
                            if inside_text:
                                if html_start > start + 1:
                                    output += block[start:html_start]
                                start = index + 1
                                if folding.count("<\\/p>") == 0:
                                    inside_text = False
                        elif to_fold[0] == '<' and len(to_fold) > 1 and to_fold[1] != '\\':
                            if to_fold[-3:-1] != "\\/":
                                expected = "<\\/" + to_fold[1:-1]
                                if ' ' in expected:
                                    expected = expected[:expected.index(' ')]
                                expected = expected + '>'
                                if expected != "<\\/img>" and expected != "<\\/area>" and expected != "<\\/base>" and expected != "<\\/br>" and expected != "<\\/col>" and expected != "<\\/command>" and expected != "<\\/embed>" and expected != "<\\/hr>" and expected != "<\\/input>" and expected != "<\\/keygen>" and expected != "<\\/link>" and expected != "<\\/meta>" and expected != "<\\/param>" and expected != "<\\/source>" and expected != "<\\/track>" and expected != "<\\/wbr>":
                                    folding.append(expected)
                                if inside_text:
                                    if html_start > start + 1:
                                        output += block[start:html_start]
                                else:
                                    if folding.count("<\\/p>") > 0:
                                        inside_text = True
                            start = index + 1
            index += 1
        output += block[start:index]
        return output

    #breaks a text block into words and adds each word to the set
    @staticmethod
    def BreakTextBlock(block):
        words = []
        current_word = ""
        i = 0
        while i < len(block):
            char = block[i]
            breaks_word = not char.isalpha() and not char.isdigit()
            if char == '\'':
                breaks_word = False
            if char == '-' and i+1 < len(block) and block[i+1].isdigit():
                breaks_word = False
            if char == '.' and i+1 < len(block) and block[i+1].isdigit():
                breaks_word = False
            if char == ',' and i+1 < len(block) and block[i+1].isdigit() and i-1 > 0 and block[i-1].isdigit():
                breaks_word = False
            
            if breaks_word:
                if current_word != "":
                    words.append(current_word)
                    current_word = ""
            else:
                current_word += char
            i+=1
        if current_word != "":
            words.append(current_word)
            current_word = ""
        return words

    #extracts a set of phrases from a set of strings
    @staticmethod
    def ExtractPhrases(strlist):
        output = []
        i = 0
        while i+2 < len(strlist):
            phrase = strlist[i] + ' ' + strlist[i+1] + ' ' + strlist[i+2]
            output.append(phrase)
            i+=1
        return output

    #parses a text block by dividing it into words and phrases and adds each word to the set
    def AddTextBlock(self, block):
        word_list = countset.BreakTextBlock(block)
        count = self.AddSet(word_list)
        phrase_list = countset.ExtractPhrases(word_list)
        for phrase in phrase_list:
            self.AddPhrase(phrase)
        word_str = "words"
        if count == 1:
            word_str = "word"
        print("\t\tAdded " + str(count) + ' ' + word_str + "; " + str(len(self.set)) + " total")
        self.Sort()

    #parses an html block and then calls AddTextBlock
    def AddHTMLBlock(self, html_block):
        return self.AddTextBlock(countset.ExtractFromHTML(html_block))