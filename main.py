import math
import numpy as np
import matplotlib.pyplot as plt

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

# Constants
g = 10  # gravity

# --- Projectile motion functions ---
def calculate_range(velocity, angle):
    angle_rad = math.radians(angle)
    return (velocity**2 * math.sin(2 * angle_rad)) / g

def calculate_time_of_flight(velocity, angle):
    angle_rad = math.radians(angle)
    return (2 * velocity * math.sin(angle_rad)) / g

def calculate_maximum_height(velocity, angle):
    angle_rad = math.radians(angle)
    return (velocity**2 * math.sin(angle_rad)**2) / (2 * g)

def calculate_trajectory(velocity, angle):
    angle_rad = math.radians(angle)
    t_flight = (2 * velocity * math.sin(angle_rad)) / g
    t = np.linspace(0, t_flight, num=500)
    x = velocity * np.cos(angle_rad) * t
    y = velocity * np.sin(angle_rad) * t - (0.5 * g * t**2)
    return x, y

# --- Main Kivy App ---
class ProjectileMotionApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Heading
        self.heading = Label(text="Projectile Motion Calculator",
                             font_size=24,
                             size_hint=(1, 0.2),
                             color=(1, 1, 1, 1))
        self.layout.add_widget(self.heading)

        # Velocity input
        self.vel_input = TextInput(hint_text="Enter velocity (m/s)",
                                   multiline=False,
                                   input_filter="float",
                                   size_hint=(1, 0.1),
                                   background_color=(0.2, 0.2, 0.2, 1),
                                   foreground_color=(1, 1, 1, 1))
        self.layout.add_widget(self.vel_input)

        # Angle input
        self.ang_input = TextInput(hint_text="Enter angle (degrees)",
                                   multiline=False,
                                   input_filter="float",
                                   size_hint=(1, 0.1),
                                   background_color=(0.2, 0.2, 0.2, 1),
                                   foreground_color=(1, 1, 1, 1))
        self.layout.add_widget(self.ang_input)

        # Buttons
        self.layout.add_widget(Button(text="Calculate Range", on_press=self.show_range, size_hint=(1, 0.1)))
        self.layout.add_widget(Button(text="Calculate Time of Flight", on_press=self.show_time, size_hint=(1, 0.1)))
        self.layout.add_widget(Button(text="Calculate Max Height", on_press=self.show_height, size_hint=(1, 0.1)))
        self.layout.add_widget(Button(text="Show Graph", on_press=self.show_graph, size_hint=(1, 0.1)))

        # Result label
        self.result = Label(text="Results will appear here",
                            font_size=18,
                            size_hint=(1, 0.2),
                            color=(1, 1, 1, 1))
        self.layout.add_widget(self.result)

        return self.layout

    # --- Utility ---
    def get_inputs(self):
        try:
            v = float(self.vel_input.text)
            a = float(self.ang_input.text)
            return v, a
        except:
            self.result.text = "⚠️ Enter valid numbers!"
            return None, None

    # --- Button callbacks ---
    def show_range(self, instance):
        v, a = self.get_inputs()
        if v is not None:
            r = calculate_range(v, a)
            self.result.text = f"Range: {r:.2f} m"

    def show_time(self, instance):
        v, a = self.get_inputs()
        if v is not None:
            t = calculate_time_of_flight(v, a)
            self.result.text = f"Time of Flight: {t:.2f} s"

    def show_height(self, instance):
        v, a = self.get_inputs()
        if v is not None:
            h = calculate_maximum_height(v, a)
            self.result.text = f"Max Height: {h:.2f} m"

    def show_graph(self, instance):
        v, a = self.get_inputs()
        if v is not None:
            x, y = calculate_trajectory(v, a)

            fig, ax = plt.subplots()
            ax.plot(x, y, "c-", linewidth=2)
            ax.set_title("Projectile Motion Trajectory")
            ax.set_xlabel("Distance (m)")
            ax.set_ylabel("Height (m)")
            ax.grid(True)

            popup = Popup(title="Trajectory Graph", size_hint=(0.9, 0.9))
            popup.add_widget(FigureCanvasKivyAgg(fig))
            popup.open()

# --- Run ---
if __name__ == "__main__":
    ProjectileMotionApp().run()
