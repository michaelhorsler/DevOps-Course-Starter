from todo_app.data.item import Item


class ViewModel:
    def __init__(self, items: list[Item]):
        self._items = items
 
    @property
    def items(self):
        return self._items

    @property
    def complete_items(self):
        #completeitems=items
        complete_items = [item for item in self._items if item.status =="Complete"]
        # complete_items = list(filter(lambda item: item.status == "Complete", self._items))
        # filter and retrieve complete items
        return complete_items
        #return items 
    
    @property
    def todo_items(self):
       # filter and retrieve todo items
        return [] 

