from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker

from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBody
from kivymd.uix.selectioncontrol import MDCheckbox


from database import Database
db = Database()


from datetime import datetime

# Dialog class for date picker
class DialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = datetime.now().strftime("%d/%m/%Y")
        
    # Shows the calendar to pick date
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()
        
    def on_save(self, instance, value, date_range):
        date = value.strftime("%d/%m/%Y")
        self.ids.date_text.text =str(date)
        
# List item action class
class ListItemWithCheckBox(TwoLineAvatarIconListItem):
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk
    
    # Complete a task
    def mark(self, check, the_list_item):
        if check.active == True:
            the_list_item.text = '[s]' + the_list_item.text + '[/s]'
            db.mark_as_completed(the_list_item.pk)
        else:
            the_list_item.text = str(db.mark_as_incompleted(the_list_item.pk))
        
    # Delete a task
    def delete_item(self, the_list_item):
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)
    
# A class for checkbox on the task
class LeftCheckbox(ILeftBody, MDCheckbox):
    pass
        
        
# Main Application
class MainApp(MDApp):
    task_list = None
    def build(self):
        self.theme_cls.primary_palette = ("Teal")
        
        
    # Show popup to add task
    def show_task_dialog(self):
        if not self.task_list:
            self.task_list = MDDialog(
                title="Add Task",
                type="custom",
                content_cls=DialogContent()
            )
            self.task_list.open()
    
    # Close the popup
    def close_task_dialog(self, *args):
        self.task_list.dismiss()

    # Add task to the list
    def add_task(self, task, task_date):
        # print(task.text, task_date)
        created_task = db.create_task(task.text, task_date)
        self.root.ids['container'].add_widget(ListItemWithCheckBox(pk = created_task[0], text = '[b]' + created_task[1] + '[/b]', secondary_text = task_date))
        task.text = ''
        
    def on_start(self):
        completed_tasks, incompleted_tasks  = db.get_tasks()
        if incompleted_tasks != []:
            for task in incompleted_tasks:
                add_task = ListItemWithCheckBox(pk = task[0], text = '[b]' + task[1] + '[/b]', secondary_text = task[2])
                self.root.ids['container'].add_widget(add_task)
                
        if completed_tasks != []:
            for task in completed_tasks:
                add_task = ListItemWithCheckBox(pk= task[0], text = '[s]' + task[1] + '[/s]', secondary_text = task[2])
                add_task.ids.check.active = True
                self.root.ids.container.add_widget(add_task)
    
if __name__ == "__main__":
    app = MainApp()
    app.run()