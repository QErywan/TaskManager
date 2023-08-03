from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime

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
        print(task.text, task_date)
    
if __name__ == "__main__":
    app = MainApp()
    app.run()