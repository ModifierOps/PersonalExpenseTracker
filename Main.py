#Description:
from dearpygui import dearpygui as dpg

dpg.create_context()

#-----------------------------------------------------------------------------------------
def _add_category_name(sender, app_data, user_data):
    button_container = user_data

    if dpg.is_item_shown(input_field):
        category_name = dpg.get_value(input_field).strip()
        if category_name:
            with dpg.group(horizontal=True, parent=button_container):
                dpg.add_spacer(width=padding)
                dpg.add_button(label=f"{category_name}", width=button_width, height=100)
            dpg.hide_item(input_field)
            dpg.set_value(input_field, "")
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
        with dpg.child_window(width=380, height=400, border=False):
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=150)
                dpg.add_text("Categories")

            button_width = 200
            child_width = 380
            padding = (child_width - button_width) // 2

            input_field = dpg.add_input_text(label="Enter a category name:")
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
