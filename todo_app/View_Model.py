from todo_app.data.item import Item

class ViewModel:
    def __init__(self, items: list[Item]):
        self._items = items
 
    @property
    def items(self):
        return self._items

    @property
    def complete_items(self):
        complete_items = [item for item in self._items if item.status =="Complete"]
        # complete_items = list(filter(lambda item: item.status == "Complete", self._items))
        return complete_items
    
    @property
    def todo_items(self):
        #todo_items = [item for item in self._items if item.status =="To do"]
        todo_items = list(filter(lambda item: item.status == "To Do", self._items))
        return todo_items

    @property
    def active_items(self):
        #todo_items = [item for item in self._items if item.status =="To do"]
        active_items = list(filter(lambda item: item.status == "Active", self._items))
        return active_items
