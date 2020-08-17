class result(object):
    """result object containing a list of fields"""
    fields = []

    def __init__(self, new_fields):
        self.fields = new_fields

    def Get(field):
        for tuple in fields:
            if tuple[0] == field:
                return tuple[1]
        return None