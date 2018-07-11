#!/usr/bin/env python3
import subprocess
import gi.repository
gi.require_version('Budgie', '1.0')
from gi.repository import Budgie, GObject, Gtk

def getStatusOfGpu():
    # only works with python 3.5 or higher
    commandOutput = subprocess.run(['cat', '/sys/bus/pci/devices/0000\\:01\\:00.0/power/control'], stdout=subprocess.PIPE) # get the object
    result = commandOutput.stdout.decode('utf8') # stdout will be a bytes object, so decode it to a string
    if (result == "on"):
        return("Currently using Nvidia")
    else:
        return("Currently using Intel")    

class SomeApp(GObject.GObject, Budgie.Plugin):

    __gtype_name__ = "SomeApp"

    def __int__(self):
        GObject.Object.__init__(self)

    def do_get_panel_widget(self, uuid):
        return SomeAppApplet(uuid)


class SomeAppApplet(Budgie.Applet):

    manager = None

    def __init__(self, uuid):

        Budgie.Applet.__init__(self)

        self.box = Gtk.EventBox()
        self.add(self.box)
        img = Gtk.Image.new_from_icon_name("video-display-symbolic", Gtk.IconSize.MENU)
        self.box.add(img)
        self.menu = Gtk.Menu()
        self.create_menu()
        self.box.show_all()
        self.show_all()

    def run_command(self, menuitem):
        print(menuitem)
        subprocess.Popen(["pkexec", "bash", "-c", "prime-select intel && reboot"])
        dialog = Gtk.MessageDialog(type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text="Please wait...")
        dialog.format_secondary_text("This might take a while. Don't turn off your computer. ")
        dialog.run()
        print("INFO dialog closed")
        dialog.destroy()

    def run_command_2(self, menuitem):
        print(menuitem)
        subprocess.Popen(["pkexec", "bash", "-c", "prime-select nvidia && reboot"])
        dialog = Gtk.MessageDialog(type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text="Please wait...")
        dialog.format_secondary_text("This might take a while. Don't turn off your computer. ")
        dialog.run()
        print("INFO dialog closed")
        dialog.destroy()

    def run_command_3(self, menuitem):
        print(menuitem)
        # subprocess.Popen(["pkexec", "bash", "-c", "prime-select nvidia && reboot"])
        dialog = Gtk.MessageDialog(type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text="Please wait...")
        dialog.format_secondary_text("This might take a while. Don't turn off your computer. ")
        dialog.run()
        print("INFO dialog closed")
        dialog.destroy()


    def create_menu(self):
        sep = Gtk.SeparatorMenuItem(getStatusOfGpu())
        item1 = Gtk.MenuItem('Switch to Intel Graphics and reboot')
        item1.connect("activate", self.run_command)
        item2 = Gtk.MenuItem('Switch to Nvidia Graphics and reboot')
        item2.connect("activate", self.run_command_2)
       	# item3 = Gtk.MenuItem('Test')
        # item3.connect("activate", self.run_command_3)
        for item in [sep, item1, item2]:
            self.menu.append(item)
        self.menu.show_all()
        self.box.connect("button-press-event", self.popup_menu)

    def popup_menu(self, *args):
        self.menu.popup(
            None, None, None, None, 0, Gtk.get_current_event_time()
        )
