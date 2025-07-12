"""
Author: Core447
Year: 2024

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This programm comes with ABSOLUTELY NO WARRANTY!

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Type
from gi.repository import Gtk

from src.backend.DeckManagement.DeckController import ControllerInput
from src.backend.DeckManagement.InputIdentifier import InputIdentifier
import globals as gl

class StateSwitcher(Gtk.ScrolledWindow):
    def __init__(self, type, **kwargs):
        super().__init__(**kwargs)
        self.type = type

        self.switch_callbacks: list[callable] = []
        self.add_new_callbacks: list[callable] = []

        self.build()

    def build(self):
        self.stack = Gtk.Stack()

        self.main_box = Gtk.Box(overflow=Gtk.Overflow.HIDDEN, css_classes=["state-switcher-box", "linked"], valign=Gtk.Align.CENTER, halign=Gtk.Align.CENTER)
        self.set_child(self.main_box)

        self.switcher = Gtk.StackSwitcher(stack=self.stack, css_classes=["state-switcher"])
        self.main_box.append(self.switcher)

        self.add_button = Gtk.Button(icon_name="list-add-symbolic")
        self.add_button.connect("clicked", self.on_add_click)
        self.main_box.append(self.add_button)

    def clear_stack(self):
        while self.stack.get_first_child() is not None:
            self.stack.remove(self.stack.get_first_child())

    def get_n_states(self) -> int:
        n = 0
        child = self.stack.get_first_child()
        while child is not None:
            n += 1
            child = child.get_next_sibling()
        return n

    def set_n_states(self, n: int):
        self._disconnect_signal()
        self.clear_stack()

        for i in range(n):
            self.stack.add_titled(Gtk.Box(), str(i+1), f"State {i+1}")

        self._connect_signal()

    def on_add_click(self, button):
        controller = gl.app.main_win.get_active_controller()
        c_input = controller.get_input(gl.app.main_win.sidebar.active_identifier)

        if c_input is None:
            return
        
        c_input.add_new_state()
        return


        input_element_dict = {
            "keys": controller.keys,
            "dials": controller.dials,
            "touchscreens": controller.touchscreens,
        }[self.type]
        for d in input_element_dict:
            if d.identifier == gl.app.main_win.sidebar.active_identifier:
                d.add_new_state()
                return

        n_states = self.get_n_states()
        self.stack.add_titled(Gtk.Box(), str(n_states + 1), f"State {n_states + 1}")

        for callback in self.add_new_callbacks:
            if callable(callback):
                callback(n_states)

    def get_selected_state(self) -> int:
        name = self.stack.get_visible_child_name()
        return int(name) - 1
    
    def select_state(self, state: int):
        if state >= self.get_n_states():
            return
        self._disconnect_signal()
        self.stack.set_visible_child_name(str(state + 1))
        self._connect_signal()

    def _connect_signal(self):
        self.stack.connect("notify::visible-child-name", self.on_state_switch)

    def _disconnect_signal(self):
        try:
            self.stack.disconnect_by_func(self.on_state_switch)
        except TypeError:
            pass

    def add_switch_callback(self, callback: callable):
        self.switch_callbacks.append(callback)

    def add_add_new_callback(self, callback: callable):
        self.add_new_callbacks.append(callback)

    def on_state_switch(self, *args):
        for callback in self.switch_callbacks:
            if callable(callback):
                callback()

    def load_for_identifier(self, identifier: InputIdentifier, state: int):
        c_input = gl.app.main_win.get_active_controller().get_input(identifier)

        self.load_for_input(c_input, state)

    def load_for_input(self, c_input: ControllerInput, state: int = None) -> None:
        self.set_n_states(len(c_input.states.keys()))
        self.select_state(state or c_input.state)

        self.set_visible(c_input.enable_states)