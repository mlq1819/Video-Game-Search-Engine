class game(object):
    """game object containing a set of fields"""

    #takes in a list of tuples[>=2]
    def __init__(self, fields):
        self.fields = fields

    def Get(self, field):
        for tuple in self.fields:
            if tuple[0] == field:
                if len(tuple) == 2:
                    return tuple[1]
                output = []
                index = 1
                while index < len(tuple):
                    output.append(tuple[index])
                    index+=1
                return output
        return None

    def Has(self, field):
        for tuple in self.fields:
            if tuple[0] == field:
                return True
        return False


