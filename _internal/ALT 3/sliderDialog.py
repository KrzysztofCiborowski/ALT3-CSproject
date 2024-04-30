import tkinter
from typing import Union, Tuple, Optional
from customtkinter.windows.widgets import CTkLabel
from customtkinter.windows.widgets import CTkButton
from customtkinter.windows.widgets.theme import ThemeManager
from customtkinter.windows.ctk_toplevel import CTkToplevel
import customtkinter
from tkinter import messagebox


class CTkSliderDialog(CTkToplevel):
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
                 text: str = "CTkDialog",
                 sliderMin: int = 0,
                 sliderMax: int = 100,
                 curr_val: int = None,
                 multiplier: int = 1):
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

        self._user_input: Union[str, None] = None
        self._userpassword_input: Union[str, None] = None
        self._running: bool = False
        self._text = text
        self._show = show
        self._sliderMin = sliderMin
        self._sliderMax = sliderMax
        self._curr_val = curr_val
        self._multiplier = multiplier

        self.title(title)
        self.lift()
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.after(10,
                   self._create_widgets)
        self.resizable(False, False)
        self.grab_set()

        if curr_val is None:
            tkinter.messagebox.showerror("Error 3", "Current value is None or no simulation is running")

    def _create_widgets(self):
        self._title_label = CTkLabel(master=self, text=self._text, fg_color=self._fg_color, text_color=self._text_color)
        self._title_label.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="ew")
        self._slider = customtkinter.CTkSlider(master=self, from_=self._sliderMin, to=self._sliderMax,
                                               command=self._slider_command, number_of_steps=100)
        self._slider.grid(row=1, column=0, padx=(20, 5), pady=(0, 20), sticky="ew")
        self._slider_label = CTkLabel(master=self, fg_color=self._fg_color,
                                      text_color=self._text_color, width=60,
                                      text=str(int(self._curr_val * self._multiplier)))
        self._slider_label.grid(row=1, column=1, padx=(10, 20), pady=(0, 20), sticky="ew")
        self._slider.set(self._curr_val)

        self._frame_buttons = customtkinter.CTkFrame(master=self, width=200)
        self._frame_buttons.grid(row=2, column=0, columnspan=2, padx=(20, 20), pady=(0, 20), sticky="ew")
        self._frame_buttons.grid_rowconfigure(0, weight=1)
        self._frame_buttons.grid_columnconfigure(0, weight=1)
        self._frame_buttons.grid_columnconfigure(1, weight=1)

        self._ok_button = CTkButton(master=self._frame_buttons,
                                    width=100,
                                    border_width=0,
                                    fg_color=self._button_fg_color,
                                    hover_color=self._button_hover_color,
                                    text_color=self._button_text_color,
                                    text='Ok',
                                    command=self._ok_event)
        self._ok_button.grid(row=3, column=1, padx=10, pady=(10, 10), sticky="ew")

        self._cancel_button = CTkButton(master=self._frame_buttons,
                                        width=100,
                                        border_width=0,
                                        fg_color=self._button_fg_color,
                                        hover_color=self._button_hover_color,
                                        text_color=self._button_text_color,
                                        text='Cancel',
                                        command=self._cancel_event)
        self._cancel_button.grid(row=3, column=0, columnspan=1, padx=10, pady=(10, 10), sticky="we")

        self._cancel_button.focus()

    def _slider_command(self, *args):
        self._slider_label.configure(text=int(self._slider.get()))

    def _ok_event(self, event=None):
        self._slider_value = self._slider.get()
        self.grab_release()
        self.destroy()

    def _on_closing(self):
        self.grab_release()
        self.destroy()

    def _cancel_event(self):
        self.destroy()

    def get_input(self):
        self.master.wait_window(self)
        return self._slider.get()
