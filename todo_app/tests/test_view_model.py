from View_Model import ViewModel

def test_view_model_complete_property(): # need to items collection
    # Arrange
    ## Pre work to do
    #view_model = ViewModel()
    
    # Act
    ## filter items for complete.
    #complete = view_model.completeitems
    complete = []

    # Assert
    ## Check the filtering for an expected quantity
    assert len(complete) == 0   # 7 complete in list

def test_view_model_todo_property(): # import items collection
    # Arrange
    ## Pre work to do
    view_model = ViewModel()

    # Act
    ## filter items for todo
    todos = view_model.todo_items

    # Assert
    ## Check the filtering for an expected quantity
    assert len(todos) == 6

