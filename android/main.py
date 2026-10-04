from android.permissions import request_permissions, Permission
from jnius import autoclass
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.utils import platform
from datetime import date
from dateutil import relativedelta
import json
#from plyer import notification
# from kivy.clock import Clock
# import threading
#from kvdroid.jclass.android.graphics import Color
#from kvdroid.tools import get_resource
#from kvdroid.tools.notification import create_notification
import time
# ---------------------------- VARIABLES ------------------------------- #
now = date.today()
today = now.strftime("%m/%d/%y")
next_month_date = now + relativedelta.relativedelta(months=1)
formatted_next_month_date = next_month_date.strftime("%m/%d/%y")

class SubscriptionManagerApp(App):

    #def test_notification(self, instance):
        #notification.notify(
            #title="Gym Subscription Manager",
       	    #message="Android notifications are working!",
       	    #app_name="Gym Subscription Manager",
       	    #timeout=10
	  #)

    def send_notification(self, member_name):
        if platform == "android":
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Context = autoclass("android.content.Context")
            NotificationChannel = autoclass("android.app.NotificationChannel")
            NotificationManager = autoclass("android.app.NotificationManager")
            NotificationBuilder = autoclass("android.app.Notification$Builder")

            activity = PythonActivity.mActivity
            manager = activity.getSystemService(Context.NOTIFICATION_SERVICE)

            channel_id = "gym_expiry_channel"

            channel = NotificationChannel(
                channel_id,
                "Membership Expiry Notifications",
                NotificationManager.IMPORTANCE_DEFAULT
            )
            manager.createNotificationChannel(channel)

            notification = (
                NotificationBuilder(activity, channel_id)
                .setContentTitle("Membership Expired!")
                .setContentText(f"{member_name}'s gym membership expires today.")
                .setSmallIcon(activity.getApplicationInfo().icon)
                .setAutoCancel(True)
                .build()
            )

            manager.notify(1, notification)

    def build(self):
        if platform == "android":
            request_permissions([Permission.POST_NOTIFICATIONS])

        self.compare_dates()

        #if int(time.time()) % 1 == 0:
         #   self.compare_dates()
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Logo/Image placeholder
        logo_label = Image(source="xD.png", size_hint=(1, 0.3))
        layout.add_widget(logo_label)

        # Name input
        self.name_input = TextInput(hint_text="Name", multiline=False)
        layout.add_widget(self.name_input)

        # Date input
        self.date_input = TextInput(text=formatted_next_month_date, multiline=False)
        layout.add_widget(self.date_input)

        # Buttons
        button_layout = BoxLayout(size_hint=(1, 0.2))
        add_button = Button(text="Add", on_press=self.save_data)
        search_button = Button(text="Search", on_press=self.search_data)
        button_layout.add_widget(add_button)
        button_layout.add_widget(search_button)
        layout.add_widget(button_layout)

        # Schedule daily notification check
        return layout

    # def on_stop(self):
    #     self.service.stop()
    # ---------------------------- CREDENTIALS SEARCHER ------------------------------- #
    def search_data(self, instance):
        scroll_layout = GridLayout(cols=2, padding=10, spacing=10, size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        # Load data from JSON
        try:
            with open("user_data.json", "r") as data_file:
                data = json.load(data_file)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            data = {}

        for entry in data.values():
            name_label = Label(text=entry['name'], size_hint_y=None, height=30)
            date_label = Label(text=f"Valid until: {entry['date']}", size_hint_y=None, height=30)
            scroll_layout.add_widget(name_label)
            scroll_layout.add_widget(date_label)

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(scroll_layout)

        popup = Popup(title="Client Subscriptions", content=scroll_view, size_hint=(0.8, 0.8))
        popup.open()

    # ---------------------------- CHECK IF SUBSCRIPTION IS STILL VALID/NOTIFICATIONS ------------------------------- #
    def compare_dates(self):
        try:
            with open("user_data.json", mode="r") as data:
                # Reading old data
                data_xd = json.load(data)

        except (json.decoder.JSONDecodeError, FileNotFoundError):
            with open("user_data.json", mode="w") as data:
                pass
        else:
            for x in data_xd:
                if str(today) == str(data_xd[x]['date']):
                    self.send_notification(data_xd[x]['name'])

    # ---------------------------- SAVE DATA ------------------------------- #
    def save_data(self, instance):
        name = self.name_input.text
        valid_until = self.date_input.text
        if not name or not valid_until:
            popup = Popup(title="Error", content=Label(text="Please fill in all fields"), size_hint=(0.6, 0.4))
            popup.open()
            return

        # Load existing data
        try:
            with open("user_data.json", "r") as data_file:
                data = json.load(data_file)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            data = {}

        data[name] = {"name": name, "date": valid_until}

        # Save data back to JSON
        with open("user_data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)

        # Clear input fields
        self.name_input.text = ""
        # self.date_input.text = ""

# Run the Kivy app
if __name__ == "__main__":
    SubscriptionManagerApp().run()
