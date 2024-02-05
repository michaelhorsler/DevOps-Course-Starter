from View_Model import ViewModel
from todo_app.data.item import Item

test_items = [
        Item(1, "New Todo", "To Do"),
        Item(2, "Completed Todo", "Complete"),
        Item(3, "Active Todo", "Active"),
        Item(4, "Active 2 Todo", "Active")
    ]

def test_view_model_complete_property_only_provides_completed_items_and_nothing_else():
    # Arrange
    ## Pre work to do
    view_model = ViewModel(test_items)
    
    # Act
    ## filter items for complete.
    complete_items = view_model.complete_items

    # Assert
    ## Check the filtering for an expected quantity
    assert len(complete_items) == 1   # 1 complete in test list

def test_view_model_todo_property_only_provides_todo_items_and_nothing_else():
    # Arrange
    ## Pre work to do
    view_model = ViewModel(test_items)
    
    # Act
    ## filter items for To Do.
    todo_items = view_model.todo_items

    # Assert
    ## Check the filtering for an expected quantity
    assert len(todo_items) == 1   # 1 todo in test list

def test_view_model_active_property_only_provides_active_items_and_nothing_else():
    # Arrange
    ## Pre work to do
    view_model = ViewModel(test_items)
    
    # Act
    ## filtered items for active.
    active_items = view_model.active_items

    # Assert
    ## Check the filtering for an expected quantity
    assert len(active_items) == 2   # 2 active in test list
