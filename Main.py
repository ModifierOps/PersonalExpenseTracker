#Description:
from dearpygui import dearpygui as dpg


categories = dict()


dpg.create_context()

#-----------------------------------------------------------------------------------------
def _add_category_name(sender, app_data, user_data):
    button_container = user_data

    if dpg.is_item_shown(input_field):
        category_name = dpg.get_value(input_field).strip()

        if category_name and categories.get(str(category_name), "doesNotExist") == "doesNotExist":
            
            categories[str(category_name)] = None

            with dpg.group(horizontal=True, parent=button_container):
                dpg.add_spacer(width=padding)
                dpg.add_button(label=f"{category_name}", width=button_width, height=100)

            dpg.hide_item(input_field)
            dpg.set_value(input_field, "")

        elif categories.get(str(category_name), "doesNotExist") != "doesNotExist":
            # First so the old corresponding window/handler instances are cleaned preventing leaks.
            if dpg.does_item_exist("tag_categoryAlreadyexists_window"):
                dpg.delete_item("tag_categoryAlreadyexists_window")
            if dpg.does_item_exist("tag_categoryAlreadyexists_handler"):
                dpg.delete_item("tag_categoryAlreadyexists_handler")

            # Then so a window is created that gets deleted upon clicking x.
            with dpg.window(label="Category Exists", modal=True, no_collapse=True,
                            tag="tag_categoryAlreadyexists_window", width=300, height=100):
                dpg.add_text("Category Already Exists")
                viewport_width, viewport_height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
                dpg.set_item_pos("tag_categoryAlreadyexists_window", [viewport_width // 2 - 150, viewport_height // 2 - 50])

            with dpg.item_handler_registry(tag="tag_categoryAlreadyexists_handler"):
                dpg.add_item_clicked_handler(callback=lambda s, a, u: dpg.delete_item("tag_categoryAlreadyexists_window"))

            # So the exception "<built-in function bind_item_handler_registry>"" 
            # due to the occasional bind before the window has been fully registered, doesn't cause a crash or flood the terminal.
            try:
                dpg.bind_item_handler_registry("tag_categoryAlreadyexists_window", "tag_categoryAlreadyexists_handler")
            except Exception as e:
                pass  # Silently ignore binding errors

        else:
            pass #TODO do window saying enter valid name...
    else:
        dpg.show_item(input_field)


#-----------------------------------------------------------------------------------------
with dpg.window(label="Two Vertical Panes", width=800, height=500):
    with dpg.group(horizontal=True):

        # === Left Pane ===
        with dpg.child_window(width=380, height=400, border=True):
            dpg.add_text("Left Pane")
            for i in range(50):
                dpg.add_text(f"Left Item {i + 1}")

        # === Middle Pane ===
        with dpg.child_window(width=380, height=400, border=False, tag="tag_middle_pane"):
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=150)
                dpg.add_text("Categories")

            button_width = 200
            child_width = 380
            padding = (child_width - button_width) // 2

            input_field = dpg.add_input_text(parent="tag_middle_pane",label="Enter a category name:")
            dpg.hide_item(input_field)

            button_container = dpg.add_child_window(width=-1, height=-1, border=False)

        # === Right Pane ===
        with dpg.child_window(width=150, height=400, border=False):
            dpg.add_spacer(height=280)

            def _remove_category_name():
                pass

            def _nuke_categories():
                pass

            with dpg.group(horizontal=False):
                dpg.add_button(label="+", callback=_add_category_name, user_data=button_container)
                dpg.add_button(label="-", callback=_remove_category_name)
                dpg.add_button(label="!", callback=_nuke_categories)

            


#-----------------------------------------------------------------------------------------
dpg.create_viewport(title="Vertical Panes Example", width=820, height=540)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
