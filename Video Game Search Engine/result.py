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