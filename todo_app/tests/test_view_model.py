from View_Model import ViewModel
from todo_app.data.item import Item

def test_view_model_complete_property_only_provides_completed_items_and_nothing_else():
    
    # Arrange
    ## Pre work to do
    test_items = [
        Item(1, "New Todo", "To Do"),
        Item(2, "Completed Todo", "Complete")
    ]

    view_model = ViewModel(test_items)
    
    # Act
    ## filter items for complete.
    complete_items = view_model.complete_items

    # Assert
    ## Check the filtering for an expected quantity
    assert len(complete_items) == 1   # 6 complete in list

#def test_view_model_todo_property():
    # Arrange
    ## Pre work to do
    #view_model = ViewModel()

    # Act
    ## filter items for todo
    #todos = view_model.todo_items

    # Assert
    ## Check the filtering for an expected quantity
    #assert len(todos) == 7

