class game(object):
    """game object containing a set of fields"""

    fields = []

    def __init__(self, new_fields):
        self.fields = new_fields

    def Get(field):
        for tuple in fields:
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

    def Has(field):
        for tuple in fields:
            if tuple[0] == field:
                return True
        return False


