from gi.repository import Gtk, Adw

from typing import TYPE_CHECKING

from src.backend.DeckManagement.InputIdentifier import Input
from src.windows.mainWindow.elements.Sidebar.elements.ActionManager import ActionManager
from src.windows.mainWindow.elements.Sidebar.elements.StateSwitcher import StateSwitcher
from src.windows.mainWindow.DeckPlus.ScreenBar import ScreenBarImage

from PIL import Image

if TYPE_CHECKING:
    from src.windows.mainWindow.elements.Sidebar.Sidebar import Sidebar

import globals as gl

class ScreenEditor(Gtk.ScrolledWindow):
    def __init__(self, sidebar: "Sidebar"):
        self.sidebar = sidebar
        super().__init__(hexpand=True, vexpand=True)

        self.build()

    def build(self):
        self.clamp = Adw.Clamp(hexpand=True, vexpand=True)
        self.set_child(self.clamp)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, hexpand=True)
        self.clamp.set_child(self.main_box)

        self.header = Gtk.Label(label="Touch Bar", css_classes=["large-title", "bold"], margin_top=15, margin_bottom=30)
        self.main_box.append(self.header)

        self.state_switcher = StateSwitcher("touchscreens", margin_start=20, margin_end=20, margin_top=10, margin_bottom=10, hexpand=True)
        self.state_switcher.add_switch_callback(self.on_state_switch)
        self.state_switcher.add_add_new_callback(self.on_add_new_state)
        self.state_switcher.set_n_states(0)
        self.main_box.append(self.state_switcher)

        self.action_manager_group = Adw.PreferencesGroup(title="Actions")
        self.main_box.append(self.action_manager_group)

        self.action_manager = ActionManager(self.sidebar)
        self.action_manager_group.add(self.action_manager)

        self.remove_state_button = Gtk.Button(label="Remove State", css_classes=["destructive-action"], margin_top=15, margin_bottom=15, margin_start=15, margin_end=15)
        self.remove_state_button.connect("clicked", self.on_remove_state)
        self.main_box.append(self.remove_state_button)


    def on_state_switch(self, *args):
        state = self.state_switcher.get_selected_state()
        # self.sidebar.active_state = self.state_switcher.get_selected_state()

        visible_child = gl.app.main_win.leftArea.deck_stack.get_visible_child()
        if visible_child is None:
            return
        controller = visible_child.deck_controller
        if controller is None:
            return
        
        for t in controller.touchscreens:
            if t.identifier == self.sidebar.active_identifier:
                t.set_state(state, update_sidebar=True)
                break

    def on_add_new_state(self, state):
        controller = gl.app.main_win.get_active_controller()

        if controller is None:
            return
        
        for t in controller.touchscreens:
            if t.identifier == self.sidebar.active_identifier:
                t.add_new_state()
                self.remove_state_button.set_visible(self.state_switcher.get_n_states() > 1)
                break

    def on_remove_state(self, button):
        if self.state_switcher.get_n_states() <= 1:
            return

        controller = gl.app.main_win.get_active_controller()
        if controller is None:
            return
        
        active_state = self.state_switcher.get_selected_state()
        
        for t in controller.touchscreens:
            if t.identifier == self.sidebar.active_identifier:
                t.remove_state(active_state)
                break

        self.remove_state_button.set_visible(self.state_switcher.get_n_states() > 1)


    def load_for_identifier(self, identifier, state):
        self.sidebar.active_identifier = identifier

        controller = gl.app.main_win.get_active_controller()
        if controller is None:
            return
        
        controller_input = controller.get_input(identifier)
        self.state_switcher.load_for_identifier(identifier, state)
        controller_input.set_state(state, update_sidebar=False)

        self.remove_state_button.set_visible(self.state_switcher.get_n_states() > 1)

        self.action_manager.load_for_identifier(identifier, state)
