import dearpygui.dearpygui as dpg

category_windows = {}  # Tracks all category-specific UI metadata

def add_entry_callback(sender, app_data, user_data):
    category = user_data
    meta = category_windows[category]

    i = meta['entry_counter']
    table_tag = meta['table_tag']

    with dpg.table_row(parent=table_tag):
        inputTextTag = f"{category}_entry_{i}_inputText"
        inputFloatTag = f"{category}_entry_{i}_inputFloat"
        inputIntTag = f"{category}_entry_{i}_inputInt"

        dpg.add_input_text(label="", width=-1, default_value=f"Item {i+1}", tag=inputTextTag)
        dpg.add_input_float(label="", width=-1, default_value=0.0, format="%.2f", tag=inputFloatTag)
        dpg.add_input_int(label="", width=-1, default_value=1, tag=inputIntTag)

        meta['entries'][f"Entry_{i}"] = {
            "inputText_Tag": inputTextTag,
            "inputFloat_Tag": inputFloatTag,
            "inputInt_Tag": inputIntTag
        }

    meta['entry_counter'] += 1


def start(sender, app_data, user_data):
    category = user_data
    window_tag = f"{category}_window"
    child_tag = f"{category}_child"
    table_tag = f"{category}_table"

    if category in category_windows:
        dpg.configure_item(window_tag, show=True)
        return

    # Initialize data for new category
    category_windows[category] = {
        'window_tag': window_tag,
        'child_tag': child_tag,
        'table_tag': table_tag,
        'entry_counter': 0,
        'entries': {}
    }

    with dpg.window(label=f"{category} Inventory", tag=window_tag, width=660, height=500,
                    on_close=lambda: dpg.configure_item(window_tag, show=False), modal=True):
        dpg.add_text(f"{category}: Inventory Entry Sheet")

        with dpg.child_window(tag=child_tag, width=600, height=400, border=True):
            with dpg.table(tag=table_tag, header_row=True, resizable=True,
                           policy=dpg.mvTable_SizingStretchProp):
                dpg.add_table_column(label="Name")
                dpg.add_table_column(label="Cost")
                dpg.add_table_column(label="Quantity")
                # No rows yet!

        dpg.add_button(label="Add Entry", callback=add_entry_callback, user_data=category)
