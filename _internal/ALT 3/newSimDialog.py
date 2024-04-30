from typing import Union, Tuple, Optional

from customtkinter.windows.widgets import CTkLabel
from customtkinter.windows.widgets import CTkEntry
from customtkinter.windows.widgets import CTkSlider
from customtkinter.windows.widgets import CTkButton
from customtkinter.windows.widgets.theme import ThemeManager
from customtkinter.windows.ctk_toplevel import CTkToplevel
import customtkinter
import tkinter


class NewSimulation(CTkToplevel):
    def __init__(self,
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 title: str = "CTkDialog"):
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
        self._slider_populationSize_value: str = None
        self.cityName: str = None
        self.population: int = 10000

    def _create_widgets(self):
        populationSize = customtkinter.IntVar()
        self.grid_columnconfigure(0, weight=1)

        self._frame_populationSize = customtkinter.CTkFrame(master=self)
        self._frame_populationSize.grid(row=0, column=0, padx=20, pady=(10, 5))
        self._label_populationSize = CTkLabel(master=self._frame_populationSize,
                                              width=100,
                                              wraplength=300,
                                              fg_color="transparent",
                                              text_color=self._text_color,
                                              text="City Population Size")
        self._label_populationSize.grid(row=0, column=0, pady=10, padx=20, sticky='we', columnspan=2)
        self._slider_populationSize = CTkSlider(master=self._frame_populationSize,
                                                width=200,
                                                from_=10000,
                                                to=25000000, variable=populationSize,
                                                command=self._label_slider_populationSize_getValue, number_of_steps=100)
        self._slider_populationSize.grid(row=1, column=0, pady=0, padx=10, sticky='w')
        self._label_slider_populationSize_value = CTkLabel(master=self._frame_populationSize, text=10000, width=100)
        self._label_slider_populationSize_value.grid(row=1, column=1, sticky='w', padx=10)

        self._frame_cityName = customtkinter.CTkFrame(master=self)
        self._frame_cityName.grid(row=1, column=0, padx=20, pady=(10, 5))

        self._label_cityName = CTkLabel(master=self._frame_cityName, text_color=self._text_color,
                                        fg_color="transparent", text="City Name")
        self._label_cityName.grid(row=0, column=0, padx=20, pady=(5, 5), sticky='we')
        self._entry_cityName = CTkEntry(master=self._frame_cityName,
                                        width=320,
                                        fg_color=self._entry_fg_color,
                                        border_color=self._entry_border_color,
                                        text_color=self._entry_text_color)
        self._entry_cityName.insert(0, "City Name:")
        self._entry_cityName.grid(row=1, column=0, sticky="nw", pady=(5, 10), padx=10)

        self._entry_cityName.bind("<FocusIn>", self._entry_cityName_focusIN)
        self._entry_cityName.bind("<FocusOut>", self._entry_cityName_focusOut)
        self._entry_cityName.bind("<Return>", self._entry_cityName_handle_enter)

        self._frame_buttons = customtkinter.CTkFrame(master=self, width=320)
        self._frame_buttons.grid(row=2, column=0, padx=20, pady=10)
        self._next_button = CTkButton(master=self._frame_buttons,
                                      width=100,
                                      border_width=0,
                                      fg_color=self._button_fg_color,
                                      hover_color=self._button_hover_color,
                                      text_color=self._button_text_color,
                                      text="Next",
                                      command=self._next_event)
        self._next_button.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky='w')

        self._cancel_button = CTkButton(master=self._frame_buttons,
                                        width=100,
                                        border_width=0,
                                        fg_color=self._button_fg_color,
                                        hover_color=self._button_hover_color,
                                        text_color=self._button_text_color,
                                        text="Cancel",
                                        command=self._cancel_event)
        self._cancel_button.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="e")


    def _label_slider_populationSize_getValue(self, *args):
        self._slider_populationSize_value = self._slider_populationSize.get()
        self._slider_populationSize_value = int(self._slider_populationSize_value)
        print(self._slider_populationSize_value)
        self._label_slider_populationSize_value.configure(text=self._slider_populationSize_value)

    def _entry_cityName_focusIN(self, _):
        if self._entry_cityName.get() == "City Name:":
            self._entry_cityName.delete(0, customtkinter.END)
            self._entry_cityName.configure(fg_color='grey')
        else:
            pass

    def _entry_cityName_focusOut(self, _):
        self._entry_cityName.configure(fg_color=self._entry_fg_color)
        pass

    def _entry_cityName_handle_enter(self, txt):
        self._entry_cityName.get()
        self._entry_cityName_focusOut('dummy')

    def get_input(self):
        self.master.wait_window(self)
        return self.cityName, self.population

    def _next_event(self, event=None):
        self.cityName = self._entry_cityName.get()
        self.population = self._slider_populationSize.get()
        self.grab_release()
        self.destroy()

    def _cancel_event(self):
        self.destroy()

    def _on_closing(self):
        self.grab_release()
        self.destroy()
