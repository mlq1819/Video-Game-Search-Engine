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
    """countset set containing a list of strings with counters applied to them"""

    #default constructor
    def __init__(self):
        self.set = []
        self.sorted = True

    #adds a new object to the set, or increases the occurance of the set
    def Add(self, str):
        i = 0
        while i < len(self.set):
            tup = self.set[i]
            if str == tup[0]:
                self.set[i] = (tup[0], tup[1] + 1)
                if i > 0 and self.set[i][1] > self.set[i-1][1]:
                    self.sorted = False
                if i+1 < len(self.set) and self.set[i][1] < self.set[i+1][1]:
                    self.sorted = False
                return True
        self.set.append((str, 1))
        self.sorted = False
        return True

    #decrements an object from the set, or deletes it entirely
    def Remove(self, str):
        i = 0
        while i < len(self.set):
            tup = self.set[i]
            if str == tup[0]:
                if tup[1] > 1:
                    self.set[i] = (tup[0], tup[1] - 1)
                    if i > 0 and self.set[i][1] > self.set[i-1][1]:
                        self.sorted = False
                    if i+1 < len(self.set) and self.set[i][1] < self.set[i+1][1]:
                        self.sorted = False
                else:
                    self.set.pop(i)
                return True
        return False
    
    #checks whether a particular object exists in the set
    def Has(self, str):
        for tup in self.set:
            if str == tup[0]:
                return True
        return False
    
    #returns the number of occurances of an object in the set
    def Get(self, str):
        for tup in self.set:
            if str == tup[0]:
                return tup[1]
        return 0

    #returns the subset of objects with at least the given number of occurances
    def Subset(self, num):
        output = []
        for tup in self.set:
            if tup[1] >= num:
                output.append((tup[0],tup[1]))
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
            pi = partition(arr, low, high)
 
            # Separately sort elements before
            # partition and after partition
            self.quickSort(arr, low, pi-1)
            self.quickSort(arr, pi+1, high)
        return

    #sorts the list
    def Sort(self):
        self.quickSort(self.set, 0, len(self.set)-1)
        self.sorted = True
        return

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

