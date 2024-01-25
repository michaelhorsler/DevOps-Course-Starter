class ViewModel:
    def __init__(self, items):
        self._items = items
 
    @property
    def items(self):
        return self._items

    @property
    def complete_items(items):
        completeitems=items
        # completeitems = items.filter(status="Complete")
        # filter and retrieve complete items
        return completeitems
    
    @property
    def todo_items():
       # filter and retrieve todo items
        return [] 

