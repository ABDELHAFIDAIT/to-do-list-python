from tkinter import *
from tkinter import messagebox, ttk
from task_manager import TaskManager
from db import engine, tasks

task_manager = TaskManager(engine, tasks)





# Functions =============================================================================

# Add Task Function
def save():
    new_title = title_entry.get()
    new_description = description_text.get("1.0", END).strip()
    new_priority = priority_selected.get()
    new_status = status_selected.get()

    result = task_manager.store(new_title, new_description, new_priority, new_status)

    if "Successfully" in result:
        messagebox.showinfo("Success", result)
        title_entry.delete(0, END)
        description_text.delete("1.0", END)
        priority_selected.set("Low")
        status_selected.set("Doing")
        refresh_lists()

    else:
        return f"Error : {result}"


# Clear All Lists
def clear_list(list):
    for row in list.get_children():
        list.delete(row)


# Refresh All Lists
def refresh_lists():
    clear_list(doing_list)
    clear_list(done_list)

    show_tasks(doing_list, "Doing")
    show_tasks(done_list, "Done")


# Show Tasks on Lists
def show_tasks(list, status:str) :
    tasks = task_manager.index_by_status(status)
    for task in tasks :
            list.insert("", "end", iid=task[0], values=(task[0], task[1], task[2], task[3]))


# Toggling Selection of Tasks in Lists 
def toggle_selection(event):
    list = event.widget
    selected = list.selection()
    if hasattr(list, "last_selected") and list.last_selected in selected:
        list.selection_remove(list.last_selected)
        list.last_selected = None
    else:
        list.last_selected = selected[0] if selected else None


# Delete Tasks Function
def delete_selected():
    selected_doing = doing_list.selection()
    selected_done = done_list.selection()

    if not selected_doing and not selected_done:
        messagebox.showwarning("Warning", "Please select a task to delete.")
        return

    confirm = messagebox.askyesno("Confirm", "Do you really want to delete the selected task?")
    if not confirm:
        return

    for item in selected_doing:
        task_id = int(doing_list.item(item, "values")[0])
        task_manager.delete(task_id)

    for item in selected_done:
        task_id = int(done_list.item(item, "values")[0])
        task_manager.delete(task_id)

    refresh_lists()


# Mark as Done Function
def mark_as_done():
    selected_doing = doing_list.selection()
    if not selected_doing:
        messagebox.showwarning("Warning", "Please select a task from Doing to mark as Done.")
        return

    for item in selected_doing:
        task_id = int(doing_list.item(item, "values")[0])
        task_manager.update_status(task_id, "Done")

    refresh_lists()






fenetre = Tk()
fenetre.title("TaskFlow - Todo List")
# fenetre.geometry("500x400")
fenetre.state("zoomed")
fenetre.resizable(False, False)


# Welcome Frame =======================================================================
welcome_frame = Frame(fenetre)
welcome_frame.pack(fill="x", pady=10)

Label(
    welcome_frame,
    text="Welcome to TaskFlow, the ideal space to manage your Tasks",
    font=("Arial", 12),
    anchor="w",
    justify="left"
).pack()


# Main Frame ==========================================================================
main_frame = Frame(fenetre)
main_frame.pack(fill="both", pady=10, padx=10)



# Form Frame ==========================================================================
form_frame = Frame(main_frame, relief="groove", bd=2, padx=10, pady=10)
form_frame.pack(side="left",pady=20, padx=10, fill="y")

Label(
    form_frame,
    text="Add New Task",
    font=("Arial", 12, "bold"),
    fg="green"
).pack(padx=10)



# Title Frame ----------------------------------------------------
title_form_frame = Frame(form_frame)
title_form_frame.pack(pady=10)

Label(
    title_form_frame,
    text="Title : ",
    font=("Arial", 10)
).grid(row=0, column=0, pady=5, sticky="w")

# Title Entry
title_entry = Entry(
    title_form_frame,
    width=50,
    font=("Arial", 10)
)
title_entry.grid(row=1, column=0, ipady=3)



# Description Frame ----------------------------------------------
description_form_frame = Frame(form_frame)
description_form_frame.pack()

Label(
    description_form_frame,
    text="Description : ",
    font=("Arial", 10)
).grid(row=0, column=0, sticky="w", pady=5)

# Description Text
description_text = Text(
    description_form_frame,
    height=16,
    width=50,
    font=("Arial", 10),
    undo=True,
    spacing1=2,
    spacing2=2,
    spacing3=2,
    wrap="word"
)
description_text.grid(row=1, column=0, sticky="we")



# Priority Frame ----------------------------------------------
priority_status_frame = Frame(form_frame)
priority_status_frame.pack(pady=20)

Label(
    priority_status_frame,
    text="Priority : ",
    font=("Arial", 10)
).grid(row=0, column=0, pady=5, padx=5)


priority_options = ["Low", "Medium", "High"]
priority_selected = StringVar(value=priority_options[0])
priority_dropdown = OptionMenu(
    priority_status_frame,
    priority_selected,
    *priority_options
)
priority_dropdown.config(
    width=8,
    font=("Arial", 10),
    pady=3
)
priority_dropdown.grid(row=0, column=1, padx=5)



# Status Frame ------------------------------------------------

Label(
    priority_status_frame,
    text="Status : ",
    font=("Arial", 10)
).grid(row=0, column=3, pady=5, padx=5)


status_options = ["Doing", "Done"]
status_selected = StringVar(value=status_options[0])
status_dropdown = OptionMenu(
    priority_status_frame,
    status_selected,
    *status_options
)
status_dropdown.config(
    width=8,
    font=("Arial", 10),
    pady=3
)
status_dropdown.grid(row=0, column=4, padx=5)



# Button Frame ------------------------------------------------
btn_form_frame = Frame(form_frame)
btn_form_frame.pack(pady=10)

add_btn = Button(
    btn_form_frame,
    font=("Arial", 10, "bold"),
    text="Add Task",
    bg="green",
    fg="white",
    width=42,
    pady=3,
    cursor="hand2",
    command=save
)
add_btn.grid(row=0, column=0)







#_______________________________________________________________________________________________________________


# Display Frame ==============================================================
display_frame = Frame(main_frame, relief="groove", bd=2, padx=10, pady=10)
display_frame.pack(side="right", padx=10, pady=20, expand=True, fill="x")



# Doing Tasks ================================================================

doing_frame = LabelFrame(
    display_frame, 
    text="Doing Tasks",
    font=("Arial", 12, "bold"),
    fg="blue",
    padx=5,
    pady=5
)
doing_frame.pack(padx=10, expand=True, fill="x")


doing_list = ttk.Treeview(doing_frame, columns=("id", "title", "description", "priority"), show="headings")

doing_list.heading("id", text="ID")
doing_list.heading("title", text="Title")
doing_list.heading("description", text="Description")
doing_list.heading("priority", text="Priority")

doing_list.column("id", width=10)
doing_list.column("title", width=80)
doing_list.column("description", width=150)
doing_list.column("priority", width=50)

doing_list.pack(fill="both", expand=True)


# Done Tasks ================================================================

done_frame = LabelFrame(
    display_frame, 
    text="Done Tasks",
    font=("Arial", 12, "bold"),
    fg="orange",
    padx=5,
    pady=5
)
done_frame.pack(padx=10, pady=10, expand=True, fill="x")

done_list = ttk.Treeview(done_frame, columns=("id", "title", "description", "priority"), show="headings")

done_list.heading("id", text="ID")
done_list.heading("title", text="Title")
done_list.heading("description", text="Description")
done_list.heading("priority", text="Priority")

done_list.column("id", width=10)
done_list.column("title", width=50)
done_list.column("description", width=150)
done_list.column("priority", width=50)

done_list.pack(fill="both", expand=True)



# Delete & Mark_as_Done Buttons ===================================================
buttons_frame = Frame(display_frame)
buttons_frame.pack(pady=10, expand=True, fill="both")

delete_btn = Button(
    buttons_frame,
    text="Delete Task",
    font=("Arial", 10, "bold"),
    fg="black",
    bg="red",
    pady=3,
    cursor="hand2",
    command=delete_selected
)
delete_btn.pack(side="left", expand="True", fill="x", padx=10)

mark_as_done_btn = Button(
    buttons_frame,
    text="Mark as Done",
    font=("Arial", 10, "bold"),
    fg="black",
    bg="lightgrey",
    pady=3,
    cursor="hand2",
    command=mark_as_done
)
mark_as_done_btn.pack(side="right", expand="True", fill="x", padx=10)


show_tasks(doing_list, "Doing")
show_tasks(done_list, "Done")


def toggle_selection(event):
    tree = event.widget
    selected = tree.selection()

    if hasattr(tree, "last_selected") and tree.last_selected in selected:
        tree.selection_remove(tree.last_selected)
        tree.last_selected = None
    else:
        tree.last_selected = selected[0] if selected else None


doing_list.last_selected = None
doing_list.bind("<<TreeviewSelect>>", toggle_selection)

done_list.last_selected = None
done_list.bind("<<TreeviewSelect>>", toggle_selection)


fenetre.mainloop()