#Description: Responsible for providing category operations in regards to the Home UI.
from dearpygui import dearpygui as dpg
import View_CategoryUI

NON_EXISTENT_CATEGORY_WINDOW_TAG = "non_existent_category_window"
NON_EXISTENT_CATEGORY_HANDLER_TAG = "non_existent_category_handler"
ALREADY_EXISTENT_CATEGORY_WINDOW_TAG = "already_existent_category_window"
ALREADY_EXISTENT_CATEGORY_HANDLER_TAG = "already_existent_category_handler"
categories = dict()


dpg.create_context()


#-----------------------------------------------------------------------------------------
def _add_category(sender, app_data, user_data):
    button_container = user_data[0]
    input_field = user_data[1]
    button_width = 200
    child_width = 380
    padding = (child_width - button_width) // 2

    if dpg.is_item_shown(input_field):
        category_name = str(dpg.get_value(input_field).strip())

        if category_name and categories.get(category_name, "doesNotExist") == "doesNotExist":
            
            categories[category_name] = {"category_button_tag": category_name}

            with dpg.group(horizontal=True, parent=button_container):
                dpg.add_spacer(width=padding)
                dpg.add_button(label=f"{category_name}", width=button_width, height=100, tag=category_name, callback=View_CategoryUI.start, user_data=category_name)

            dpg.hide_item(input_field)
            dpg.set_value(input_field, "")

        else:
            if dpg.get_value(input_field).strip() == "": 
                _popup_add_category_failed(isInputEmpty = True)
            else:
                _popup_add_category_failed(isInputEmpty = False)
            dpg.set_value(input_field, "")

    else:
        dpg.show_item(input_field)


#-----------------------------------------------------------------------------------------
def _remove_category(sender, app_data, user_data):
    input_field = user_data[1]

    if dpg.is_item_shown(input_field):
        category_name = dpg.get_value(input_field).strip()

        if category_name and categories.get(str(category_name), "doesNotExist") != "doesNotExist":
            
            categoryButtonToRemove = categories.pop(str(category_name))

            dpg.delete_item(categoryButtonToRemove["category_button_tag"])

            dpg.hide_item(input_field)
            dpg.set_value(input_field, "")

        else:
            if dpg.get_value(input_field).strip() == "":
                _popup_remove_category_failed(isInputEmpty = True)
            else:
                _popup_remove_category_failed(isInputEmpty = False)
            dpg.set_value(input_field, "")

    else:
        dpg.show_item(input_field)


#-----------------------------------------------------------------------------------------
def _nuke_categories(sender, app_data, user_data):
    for category in list(categories):       
        categoryButtonToRemove = categories.pop(str(category))
        dpg.delete_item(categoryButtonToRemove["category_button_tag"])


#-----------------------------------------------------------------------------------------
def _popup_remove_category_failed(isInputEmpty):
# First so the old corresponding window/handler instances are cleaned preventing leaks.
    if dpg.does_item_exist(NON_EXISTENT_CATEGORY_WINDOW_TAG):
        dpg.delete_item(NON_EXISTENT_CATEGORY_WINDOW_TAG)
    if dpg.does_item_exist(NON_EXISTENT_CATEGORY_HANDLER_TAG):
        dpg.delete_item(NON_EXISTENT_CATEGORY_HANDLER_TAG)

    if isInputEmpty == False:
        # Then so a window is created that gets deleted upon clicking x.
        with dpg.window(label="Category Doesn't Exist", modal=True, no_collapse=True,
                        tag=NON_EXISTENT_CATEGORY_WINDOW_TAG, width=300, height=100):
            dpg.add_text("Category Doesn't exist")
            viewport_width, viewport_height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
            dpg.set_item_pos(NON_EXISTENT_CATEGORY_WINDOW_TAG, [viewport_width // 2 - 150, viewport_height // 2 - 50])
    else:
        # Then so a window is created that gets deleted upon clicking x.
        with dpg.window(label="Please enter valid input", modal=True, no_collapse=True,
                        tag=NON_EXISTENT_CATEGORY_WINDOW_TAG, width=300, height=100):
            dpg.add_text("Please enter valid input")
            viewport_width, viewport_height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
            dpg.set_item_pos(NON_EXISTENT_CATEGORY_WINDOW_TAG, [viewport_width // 2 - 150, viewport_height // 2 - 50])

    with dpg.item_handler_registry(tag=NON_EXISTENT_CATEGORY_HANDLER_TAG):
        dpg.add_item_clicked_handler(callback=lambda s, a, u: dpg.delete_item(NON_EXISTENT_CATEGORY_WINDOW_TAG))

    # So the exception "<built-in function bind_item_handler_registry>"" 
    # due to the occasional bind before the window has been fully registered, doesn't cause a crash or flood the terminal.
    try:
        dpg.bind_item_handler_registry(NON_EXISTENT_CATEGORY_WINDOW_TAG, NON_EXISTENT_CATEGORY_HANDLER_TAG)
    except Exception as e:
        pass  # Silently ignore binding errors


#-----------------------------------------------------------------------------------------
def _popup_add_category_failed(isInputEmpty):
# First so the old corresponding window/handler instances are cleaned preventing leaks.
    if dpg.does_item_exist(ALREADY_EXISTENT_CATEGORY_WINDOW_TAG):
        dpg.delete_item(ALREADY_EXISTENT_CATEGORY_WINDOW_TAG)
    if dpg.does_item_exist(ALREADY_EXISTENT_CATEGORY_HANDLER_TAG):
        dpg.delete_item(ALREADY_EXISTENT_CATEGORY_HANDLER_TAG)

    if isInputEmpty == False:
        # Then so a window is created that gets deleted upon clicking x.
        with dpg.window(label="Category Exists", modal=True, no_collapse=True,
                        tag=ALREADY_EXISTENT_CATEGORY_WINDOW_TAG, width=300, height=100):
            dpg.add_text("Category Already Exists")
            viewport_width, viewport_height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
            dpg.set_item_pos(ALREADY_EXISTENT_CATEGORY_WINDOW_TAG, [viewport_width // 2 - 150, viewport_height // 2 - 50])
    else:
        # Then so a window is created that gets deleted upon clicking x.
        with dpg.window(label="Enter a valid category", modal=True, no_collapse=True,
                        tag=ALREADY_EXISTENT_CATEGORY_WINDOW_TAG, width=300, height=100):
            dpg.add_text("Enter a valid category")
            viewport_width, viewport_height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
            dpg.set_item_pos(ALREADY_EXISTENT_CATEGORY_WINDOW_TAG, [viewport_width // 2 - 150, viewport_height // 2 - 50])

    with dpg.item_handler_registry(tag=ALREADY_EXISTENT_CATEGORY_HANDLER_TAG):
        dpg.add_item_clicked_handler(callback=lambda s, a, u: dpg.delete_item(ALREADY_EXISTENT_CATEGORY_WINDOW_TAG))

    # So the exception "<built-in function bind_item_handler_registry>"" 
    # due to the occasional bind before the window has been fully registered, doesn't cause a crash or flood the terminal.
    try:
        dpg.bind_item_handler_registry(ALREADY_EXISTENT_CATEGORY_WINDOW_TAG, ALREADY_EXISTENT_CATEGORY_HANDLER_TAG)
    except Exception as e:
        pass  # Silently ignore binding errors
