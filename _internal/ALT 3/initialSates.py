from typing import Union, Tuple, Optional

from customtkinter.windows.widgets import CTkLabel
from customtkinter.windows.widgets import CTkEntry
from customtkinter.windows.widgets import CTkSlider
from customtkinter.windows.widgets import CTkButton
from customtkinter.windows.widgets.theme import ThemeManager
from customtkinter.windows.ctk_toplevel import CTkToplevel
from customtkinter.windows.widgets import CTkFrame
import customtkinter
import tkinter


class R0I0(CTkToplevel):
    def __init__(self,
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_text_color: Optional[Union[str, Tuple[str, str]]] = None,

                 show: str = "",
                 title: str = "CTkDialog",
                 text: str = "CTkDialog"):
        super().__init__(fg_color=fg_color)

        self._fg_color = ThemeManager.theme["CTkToplevel"]["fg_color"] if fg_color is None else self._check_color_type(
            fg_color)
        self._text_color = ThemeManager.theme["CTkLabel"][
            "text_color"] if text_color is None else self._check_color_type(button_hover_color)
        self._button_fg_color = ThemeManager.theme["CTkButton"][
            "fg_color"] if button_fg_color is None else self._check_color_type(button_fg_color)
        self._button_hover_color = ThemeManager.theme["CTkButton"][
            "hover_color"] if button_hover_color is None else self._check_color_type(button_hover_color)
        self._button_text_color = ThemeManager.theme["CTkButton"][
            "text_color"] if button_text_color is None else self._check_color_type(button_text_color)
        self._entry_fg_color = ThemeManager.theme["CTkEntry"][
            "fg_color"] if entry_fg_color is None else self._check_color_type(entry_fg_color)
        self._entry_border_color = ThemeManager.theme["CTkEntry"][
            "border_color"] if entry_border_color is None else self._check_color_type(entry_border_color)
        self._entry_text_color = ThemeManager.theme["CTkEntry"][
            "text_color"] if entry_text_color is None else self._check_color_type(entry_text_color)

        self.title(title)
        self.lift()
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.after(10, self._create_widgets)
        self.grab_set()
        self.resizable(False, False)
        self.grid_columnconfigure((1), weight=1)

        self.initStates = [
            {"name": "Initial Infected", "from_": 1, "to": 1000, "steps": 1000, "default": 500},
            {"name": "Initial Exposed", "from_": 1, "to": 1000, "steps": 1000, "default": 100},
            {"name": "Initial Recovered", "from_": 1, "to": 1000, "steps": 1000, "default": 1},
            {"name": "Initial Asymptomatic", "from_": 1, "to": 1000, "steps": 1000, "default": 100},
            {"name": "Initial Symptomatic", "from_": 1, "to": 1000, "steps": 1000, "default": 100},
            {"name": "Initial Hospitalized", "from_": 1, "to": 1000, "steps": 1000, "default": 100},
            {"name": "Initial Deceased", "from_": 1, "to": 1000, "steps": 1000, "default": 100}
        ]

    def _create_widgets(self):
        for i, rate_info in enumerate(self.initStates):
            frame = customtkinter.CTkFrame(master=self)
            frame.grid(row=i, column=0, padx=10, pady=10, sticky="ew")

            label = CTkLabel(master=frame, text=rate_info["name"], width=125)
            label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            slider = CTkSlider(master=frame, from_=rate_info["from_"], to=rate_info["to"],
                               number_of_steps=rate_info["steps"],
                               command=lambda value, name=rate_info["name"]: self._update_value(name, value))
            slider.grid(row=0, column=1, padx=10, pady=10)
            slider.set(rate_info["default"])

            value_label = CTkLabel(master=frame, text=f'{rate_info["default"]}')
            value_label.grid(row=0, column=2, padx=10, pady=10)
            setattr(self, f"_value_label_{rate_info['name'].replace(' ', '_')}", value_label)

        self._button_frame = CTkFrame(master=self)
        self._button_frame.grid(row=100, column=0, columnspan=2, pady=(0, 10))

        self._cancel_button = CTkButton(master=self._button_frame, text_color=self._button_text_color,
                                        fg_color=self._button_fg_color, hover_color=self._button_hover_color,
                                        text="Cancel", command=self._cancel_event, width=100)
        self._cancel_button.grid(row=0, column=0, padx=(10, 20), sticky="w", pady=10)
        self._done_button = CTkButton(master=self._button_frame, text_color=self._button_text_color,
                                      fg_color=self._button_fg_color, hover_color=self._button_hover_color, text="Done",
                                      command=self._done_event, width=100)
        self._done_button.grid(row=0, column=1, padx=(20, 10), pady=10, sticky="ew")

    def _update_value(self, name, value):
        label_name = f"_value_label_{name.replace(' ', '_')}"
        if hasattr(self, label_name):
            getattr(self, label_name).configure(text=f"{int(value)}")

    def get_input(self):
        self.master.wait_window(self)
        return {rate_info["name"]: getattr(self, f"_value_label_{rate_info['name'].replace(' ', '_')}").cget("text") for
                rate_info in self.initStates}

    def _done_event(self, event=None):
        self.grab_release()
        self.destroy()

    def _cancel_event(self):
        self.destroy()

    def _on_closing(self):
        self.grab_release()
        self.destroy()
