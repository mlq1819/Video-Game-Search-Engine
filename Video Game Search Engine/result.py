class result(object):
    """result object containing a list of fields"""
    fields = []

    #takes in a list of tuples[2]
    def __init__(self, new_fields):
        self.fields = new_fields

    def Get(field):
        for tuple in fields:
            if tuple[0] == field:
                return tuple[1]
        return None

    def Has(field):
        for tuple in fields:
            if tuple[0] == field:
                return True
        return False