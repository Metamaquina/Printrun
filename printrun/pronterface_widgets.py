# This file is part of the Printrun suite.
#
# Printrun is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Printrun is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Printrun.  If not, see <http://www.gnu.org/licenses/>.

import wx
import re
from sys import platform as _platform

class MacroEditor(wx.Dialog):
    """Really simple editor to edit macro definitions"""

    def __init__(self, macro_name, definition, callback, gcode = False):
        self.indent_chars = "  "
        title = "  macro %s"
        if gcode:
            title = "  %s"
        self.gcode = gcode
        wx.Dialog.__init__(self, None, title = title % macro_name, style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.callback = callback
        self.panel = wx.Panel(self,-1)
        titlesizer = wx.BoxSizer(wx.HORIZONTAL)
        titletext = wx.StaticText(self.panel,-1, "              _")  #title%macro_name)
        #title.SetFont(wx.Font(11, wx.NORMAL, wx.NORMAL, wx.BOLD))
        titlesizer.Add(titletext, 1)
        self.findb = wx.Button(self.panel,  -1, _("Find"), style = wx.BU_EXACTFIT)  #New button for "Find" (Jezmy)
        self.findb.Bind(wx.EVT_BUTTON,  self.find)
        self.okb = wx.Button(self.panel, -1, _("Save"), style = wx.BU_EXACTFIT)
        self.okb.Bind(wx.EVT_BUTTON, self.save)
        self.Bind(wx.EVT_CLOSE, self.close)
        titlesizer.Add(self.findb)
        titlesizer.Add(self.okb)
        self.cancelb = wx.Button(self.panel, -1, _("Cancel"), style = wx.BU_EXACTFIT)
        self.cancelb.Bind(wx.EVT_BUTTON, self.close)
        titlesizer.Add(self.cancelb)
        topsizer = wx.BoxSizer(wx.VERTICAL)
        topsizer.Add(titlesizer, 0, wx.EXPAND)
        self.e = wx.TextCtrl(self.panel, style = wx.HSCROLL|wx.TE_MULTILINE|wx.TE_RICH2, size = (400, 400))
        if not self.gcode:
            self.e.SetValue(self.unindent(definition))
        else:
            self.e.SetValue("\n".join(definition))
        topsizer.Add(self.e, 1, wx.ALL+wx.EXPAND)
        self.panel.SetSizer(topsizer)
        topsizer.Layout()
        topsizer.Fit(self)
        self.Show()
        self.e.SetFocus()

    def find(self, ev):
        # Ask user what to look for, find it and point at it ...  (Jezmy)
        S = self.e.GetStringSelection()
        if not S :
            S = "Z"
        FindValue = wx.GetTextFromUser('Please enter a search string:', caption = "Search", default_value = S, parent = None)
        somecode = self.e.GetValue()
        numLines = len(somecode)
        position = somecode.find(FindValue,  self.e.GetInsertionPoint())
        if position == -1 :
         #   ShowMessage(self,-1,  "Not found!")
            titletext = wx.TextCtrl(self.panel,-1, "Not Found!")
        else:
        # self.title.SetValue("Position : "+str(position))

            titletext = wx.TextCtrl(self.panel,-1, str(position))

            # ananswer = wx.MessageBox(str(numLines)+" Lines detected in file\n"+str(position), "OK")
            self.e.SetFocus()
            self.e.SetInsertionPoint(position)
            self.e.SetSelection(position,  position + len(FindValue))
            self.e.ShowPosition(position)

    def ShowMessage(self, ev , message):
        dlg = wxMessageDialog(self, message,
                              "Info!", wxOK | wxICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def save(self, ev):
        self.Destroy()
        if not self.gcode:
            self.callback(self.reindent(self.e.GetValue()))
        else:
            self.callback(self.e.GetValue().split("\n"))

    def close(self, ev):
        self.Destroy()

    def unindent(self, text):
        self.indent_chars = text[:len(text)-len(text.lstrip())]
        if len(self.indent_chars) == 0:
            self.indent_chars = "  "
        unindented = ""
        lines = re.split(r"(?:\r\n?|\n)", text)
        #print lines
        if len(lines) <= 1:
            return text
        for line in lines:
            if line.startswith(self.indent_chars):
                unindented += line[len(self.indent_chars):] + "\n"
            else:
                unindented += line + "\n"
        return unindented
    def reindent(self, text):
        lines = re.split(r"(?:\r\n?|\n)", text)
        if len(lines) <= 1:
            return text
        reindented = ""
        for line in lines:
            if line.strip() != "":
                reindented += self.indent_chars + line + "\n"
        return reindented

class options(wx.Dialog):
    """Options editor"""
    def __init__(self, pronterface):
        wx.Dialog.__init__(self, None, title = _("Edit settings"), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        topsizer = wx.BoxSizer(wx.VERTICAL)
        vbox = wx.StaticBoxSizer(wx.StaticBox(self, label = _("Defaults")) ,wx.VERTICAL)
        topsizer.Add(vbox, 1, wx.ALL+wx.EXPAND)
        grid = wx.FlexGridSizer(rows = 0, cols = 2, hgap = 8, vgap = 2)
        grid.SetFlexibleDirection( wx.BOTH )
        grid.AddGrowableCol( 1 )
        grid.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        vbox.Add(grid, 0, wx.EXPAND)
        ctrls = {}
        for k, v in sorted(pronterface.settings._all_settings().items()):
            ctrls[k, 0] = wx.StaticText(self,-1, k)
            ctrls[k, 1] = wx.TextCtrl(self,-1, str(v))
            if k in pronterface.helpdict:
                ctrls[k, 0].SetToolTipString(pronterface.helpdict.get(k))
                ctrls[k, 1].SetToolTipString(pronterface.helpdict.get(k))
            grid.Add(ctrls[k, 0], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.ALIGN_RIGHT)
            grid.Add(ctrls[k, 1], 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND)
        topsizer.Add(self.CreateSeparatedButtonSizer(wx.OK+wx.CANCEL), 0, wx.EXPAND)
        self.SetSizer(topsizer)
        topsizer.Layout()
        topsizer.Fit(self)
        if self.ShowModal() == wx.ID_OK:
            for k, v in pronterface.settings._all_settings().items():
                if ctrls[k, 1].GetValue() != str(v):
                    pronterface.set(k, str(ctrls[k, 1].GetValue()))
        self.Destroy()

def makePageTitle(wizPg, title):
  sizer = wx.BoxSizer(wx.VERTICAL)
  wizPg.SetSizer(sizer)
  title = wx.StaticText(wizPg, -1, title)
  title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
  sizer.AddWindow(title, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
  sizer.AddWindow(wx.StaticLine(wizPg, -1), 0, wx.EXPAND|wx.ALL, 5)
  return sizer

from os import listdir
from os.path import isfile, join
class slicingsettings(wx.Dialog):
  def __init__(self, pronterface):
    self.pronterface = pronterface
    printer_path = "profiles/printer"
    print_path = "profiles/print"
    filament_path = "profiles/filament"
    printer_choices = [ f.split(".")[0] for f in listdir(printer_path) if isfile(join(printer_path,f)) ]
    resolution_choices = [ f.split(".")[0] for f in listdir(print_path) if isfile(join(print_path,f)) ]
    filament_choices = [ f.split(".")[0] for f in listdir(filament_path) if isfile(join(filament_path,f)) ]

    wx.Dialog.__init__(self, None, title = _("Slicing Settings"), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)

    self.sizer = makePageTitle(self, _("Slicing Settings"))

    grid = wx.FlexGridSizer(rows = 3, cols = 2, hgap = 2, vgap = 2)
    grid.SetFlexibleDirection( wx.BOTH )
    grid.AddGrowableCol( 1 )
    grid.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
    self.sizer.Add(grid, 0, wx.EXPAND)

    printer_profile = wx.ComboBox(self, -1, choices = printer_choices, value=self.pronterface.settings.printer_profile, style = wx.CB_DROPDOWN, size = (120,-1))
    grid.Add(wx.StaticText(self,-1, _("Printer:")), 0, flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
    grid.Add(printer_profile, 1, flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)

    print_profile = wx.ComboBox(self, -1, choices = resolution_choices, value=self.pronterface.settings.print_profile, style = wx.CB_DROPDOWN, size = (120,-1))
    grid.Add(wx.StaticText(self,-1, _("Quality:")), 0, flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
    grid.Add(print_profile, 1, flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)

    filament_profile = wx.ComboBox(self, -1, choices = filament_choices, value=self.pronterface.settings.filament_profile, style = wx.CB_DROPDOWN, size = (120,-1))
    grid.Add(wx.StaticText(self,-1, _("Filament:")), 0, flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
    grid.Add(filament_profile, 1, flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)

    fill_density = wx.Slider(self, -1, int(self.pronterface.settings.fill_density), minValue=0, maxValue=100, style=wx.SL_AUTOTICKS|wx.SL_LABELS, size = (120,-1))
    grid.Add(wx.StaticText(self,-1, _("Fill density:")), 0, flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
    grid.Add(fill_density, 1, flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)

    grid.Add(wx.StaticText(self,-1, _("Support:")), 0, flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
    support_material = wx.CheckBox(self, -1, _("Use support material"), (10, 10))
    support_material.SetValue(self.pronterface.settings.support_material)
    grid.Add(support_material, 1, flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)

    self.sizer.Add(self.CreateSeparatedButtonSizer(wx.OK+wx.CANCEL), 0, wx.EXPAND)
    self.SetSizer(self.sizer)
    self.sizer.Layout()
    self.sizer.Fit(self)

    if self.ShowModal() == wx.ID_OK:
      if print_profile.GetValue() != str(self.pronterface.settings.print_profile):
        pronterface.set("print_profile", print_profile.GetValue())

      if printer_profile.GetValue() != str(self.pronterface.settings.printer_profile):
        pronterface.set("printer_profile", printer_profile.GetValue())

      if filament_profile.GetValue() != str(self.pronterface.settings.filament_profile):
        pronterface.set("filament_profile", filament_profile.GetValue())

      if fill_density.GetValue() != str(self.pronterface.settings.fill_density):
        pronterface.set("fill_density", fill_density.GetValue())

      if support_material.GetValue() != str(self.pronterface.settings.support_material):
        pronterface.set("support_material", support_material.GetValue())

      if _platform == "win32" or _platform == "cygwin":
        slicer_executable = "Slic3r_windows/slic3r.exe"
      else:
        slicer_executable = "Slic3r_gnulinux/bin/slic3r"

      if support_material.GetValue():
        support_material_param = "--support_material"
      else:
        support_material_param = ""

      pronterface.set("slicecommand", "%s --load %s/%s.ini --load %s/%s.ini --load %s/%s.ini --fill-density %s %s $s --output $o" % (slicer_executable, printer_path, printer_profile.GetValue(), print_path, print_profile.GetValue(), filament_path, filament_profile.GetValue(), str(int(fill_density.GetValue())/100.0), support_material_param))

    self.Destroy()

class MessageToUserDialog(wx.Dialog):
  """Display a remote message to our users"""
  def download(self, event):
    open_new_tab(self.url)
    self.Destroy()

  def __init__(self, msg):
    wx.Dialog.__init__(self, None, title = _("Message from Metamaquina"), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
    title=msg["title"]
    instructions=msg["text"]
    self.sizer = makePageTitle(self, title)
    instr = wx.StaticText(self, -1, instructions)
    instr.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
    instr.Wrap(400)
    self.sizer.AddWindow(instr, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    if "url" in msg.keys():
      self.url = msg["url"]

      if "urllabel" in msg.keys():
        label = msg["urllabel"]
      else:
        label = "Download"

      download_button = wx.Button(self, label=label)
      download_button.Bind(wx.EVT_BUTTON, self.download)
      self.sizer.AddWindow(download_button, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    self.ShowModal()
    self.Destroy()

from subprocess import call

def invokeAVRDude(hex_image, port, baud):
  if _platform == "win32" or _platform == "cygwin":
    avrdude = "tools\\avrdude.exe"
    config = "tools\\avrdude.conf"
  else:
    avrdude = "tools/avrdude"
    config = "tools/avrdude.conf"

  cmd = "%s -C%s -v -v -v -v -patmega2560 -cwiring -P%s -b%d -D -Uflash:w:%s:i" %(avrdude, config, port, baud, hex_image)
  print "Gravando firmware: [%s]" % (cmd)

  call(cmd, shell=True)

class WaitForAVRDude(wx.Dialog):
  def __init__(self):
    wx.Dialog.__init__(self, None, title = _("Uploading firmware"), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
    title=_("Uploading firmware")
    instructions=_("Please wait while the firmware is loaded. This may take a few minutes.")
    self.sizer = makePageTitle(self, title)
    instr = wx.StaticText(self, -1, instructions)
    instr.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
    instr.Wrap(400)
    self.sizer.AddWindow(instr, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    self.Fit()
    self.Layout()
    self.CentreOnScreen()
    # Display the Dialog
    self.Show()
    # Make sure the screen gets fully drawn before continuing.
    wx.Yield()

from os import remove
from tempfile import mkstemp
from webbrowser import open_new_tab
import urlgrabber
from xml.dom.minidom import parse
class firmwareupdate(wx.Dialog):
  """Firmware Update Wizard"""
  def __init__(self, pronterface):
    self.pronterface = pronterface
    wx.Dialog.__init__(self, None, title = _("Firmware Update"), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
    title=_("Firmware Update")
    instructions=_("Be sure to plug your 3d printer to the USB port before clicking 'install'.")
    self.sizer = makePageTitle(self, title)
    instr = wx.StaticText(self, -1, instructions)
    instr.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
    instr.Wrap(400)
    self.sizer.AddWindow(instr, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    self.images = []
    self.sources = []
    self.build_firmware_list()
    self.sizer.Layout()
    self.sizer.Fit(self)
    self.ShowModal()

  def install_fw(self, event):
    print _("downloading firmware image:")
    image = self.images[event.GetId()]
    print image

    try:
      wait = WaitForAVRDude()

      tmpfile_handle, hex_image_path = mkstemp()
      urlgrabber.urlgrab(str(image), filename=hex_image_path, timeout=15)

      port = str(self.pronterface.serialport.GetValue())
      baudrate = int(self.pronterface.baud.GetValue())

      self.pronterface.disconnect(False)
      invokeAVRDude(hex_image_path, port, baudrate)
      self.pronterface.connect(False)
      wait.Destroy()
      self.Destroy()
      remove(hex_image_path)

    except urlgrabber.grabber.URLGrabError:
      print _("We're probably offline. We'll not look for updates this time. Please check your internet connection if you wish to receive software updates.")

  def show_fw_source_code(self, event):
    source = self.sources[event.GetId()]
    open_new_tab(source)

  def build_firmware_list(self):
    i=0
    for fw in self.pronterface.fw_update_list:
      title_text = wx.StaticText(self, -1, fw["title"])
      title_text.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

      self.sources.append(fw["source"])
      source_button = wx.Button(self, id=i, label=_("Source Code"))
      source_button.Bind(wx.EVT_BUTTON, self.show_fw_source_code)

      self.images.append(fw["image"])
      update_button = wx.Button(self, id=i, label=_("Install"))
      update_button.Bind(wx.EVT_BUTTON, self.install_fw)
      i+=1

      hbox = wx.BoxSizer(wx.HORIZONTAL)
      self.sizer.AddWindow(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 5)
      self.sizer.AddWindow(title_text, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
      hbox.AddWindow(source_button, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
      hbox.AddWindow(update_button, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
      self.sizer.AddWindow(hbox, 0 , wx.ALIGN_CENTRE|wx.ALL, 5)

import wx.wizard as wiz

class WizardPageWithGCODE(wiz.WizardPageSimple):
  def __init__(self, parent, title, instructions):
    wiz.WizardPageSimple.__init__(self, parent)
    self.sizer = makePageTitle(self, title)
    instr = wx.StaticText(self, -1, instructions)
    instr.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
    instr.Wrap(400)
    self.sizer.AddWindow(instr, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

class WizardBedLevel(WizardPageWithGCODE):
  def __init__(self, parent, moveCallback):
    self.move = moveCallback
    WizardPageWithGCODE.__init__(self, parent, title=_("Adjusting bed level"), instructions=_("In this step we'll calibrate the height of the heated bed. If the printer is moving, please wait until it stops.\n\nThen use the 'up' and 'down' buttons below in order to make the extruder nozzle gently touch the heated bed surface.\n\nOnce you're finished, press 'next'."))

    self.zdown1 = wx.Button(self, id=-1, label=_("1mm Down"))
    self.zdown1.Bind(wx.EVT_BUTTON, self.zdown1Click)
    self.zdown01 = wx.Button(self, id=-1, label=_("0.1mm Down"))
    self.zdown01.Bind(wx.EVT_BUTTON, self.zdown01Click)
    self.zup1 = wx.Button(self, id=-1, label=_("1mm Up"))
    self.zup1.Bind(wx.EVT_BUTTON, self.zup1Click)
    self.zup01 = wx.Button(self, id=-1, label=_("0.1mm Up"))
    self.zup01.Bind(wx.EVT_BUTTON, self.zup01Click)

    self.zup1.SetToolTip(wx.ToolTip(_("move the extruder nozzle 1mm away from the build platform")))
    self.zup01.SetToolTip(wx.ToolTip(_("move the extruder nozzle 0.1mm away from the build platform")))
    self.zdown1.SetToolTip(wx.ToolTip(_("move the extruder nozzle 1mm closer to the build platform")))
    self.zdown01.SetToolTip(wx.ToolTip(_("move the extruder nozzle 0.1mm closer to the build platform")))

    self.sizer.Add(self.zup1, 0, wx.CENTER)
    self.sizer.Add(self.zup01, 0, wx.CENTER)
    self.sizer.Add(self.zdown01, 0, wx.CENTER)
    self.sizer.Add(self.zdown1, 0, wx.CENTER)

  def send_gcode(self, printer):
    printer.send_now("G1 X100 Y100 Z10 F3000")

  def zdown1Click(self, event):
    self.move(-1)

  def zdown01Click(self, event):
    self.move(-0.1)

  def zup1Click(self, event):
    self.move(1)

  def zup01Click(self, event):
    self.move(0.1)

class WizardSaveCalibration(WizardPageWithGCODE):
  def __init__(self, parent):
    WizardPageWithGCODE.__init__(self, parent, title=_("Success!"), instructions=_("The printer has now saved the calibration to it's internal memory. The printer will always restore this calibration setting from memory when it's turned on, so you don't need to repeat this process, unless the heated bed leveling is changed."))

  def send_gcode(self, printer):
    printer.send_now("M251 S2")
    printer.send_now("G92 X100 Y100 Z0")
    printer.send_now("G1 Z5 F3000")
    printer.send_now("G1 X0 Y0")
    printer.send_now("G1 Z0")

class zcalibration(wiz.Wizard):
  """Z Axis calibration wizard"""

  def __init__(self, pronterface):
    self.pronterface = pronterface
    wx.wizard.Wizard.__init__(self, None, -1, _("Z Axis Calibration Wizard"))
    page1 = WizardBedLevel(self, self.pronterface.moveZ)
    page2 = WizardSaveCalibration(self)
    self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED,self.OnWizardPageChange)
    wiz.WizardPageSimple_Chain(page1, page2)
    self.FitToPage(page1)
    self.RunWizard(page1)
    self.Destroy()

  def OnWizardPageChange(self, event):
    self.GetCurrentPage().send_gcode(self.pronterface.p)

class ButtonEdit(wx.Dialog):
    """Custom button edit dialog"""
    def __init__(self, pronterface):
        wx.Dialog.__init__(self, None, title = _("Custom button"), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.pronterface = pronterface
        topsizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.FlexGridSizer(rows = 0, cols = 2, hgap = 4, vgap = 2)
        grid.AddGrowableCol(1, 1)
        grid.Add(wx.StaticText(self,-1, _("Button title")), 0, wx.BOTTOM|wx.RIGHT)
        self.name = wx.TextCtrl(self,-1, "")
        grid.Add(self.name, 1, wx.EXPAND)
        grid.Add(wx.StaticText(self, -1, _("Command")), 0, wx.BOTTOM|wx.RIGHT)
        self.command = wx.TextCtrl(self,-1, "")
        xbox = wx.BoxSizer(wx.HORIZONTAL)
        xbox.Add(self.command, 1, wx.EXPAND)
        self.command.Bind(wx.EVT_TEXT, self.macrob_enabler)
        self.macrob = wx.Button(self,-1, "..", style = wx.BU_EXACTFIT)
        self.macrob.Bind(wx.EVT_BUTTON, self.macrob_handler)
        xbox.Add(self.macrob, 0)
        grid.Add(xbox, 1, wx.EXPAND)
        grid.Add(wx.StaticText(self,-1, _("Color")), 0, wx.BOTTOM|wx.RIGHT)
        self.color = wx.TextCtrl(self,-1, "")
        grid.Add(self.color, 1, wx.EXPAND)
        topsizer.Add(grid, 0, wx.EXPAND)
        topsizer.Add( (0, 0), 1)
        topsizer.Add(self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL), 0, wx.ALIGN_CENTER)
        self.SetSizer(topsizer)

    def macrob_enabler(self, e):
        macro = self.command.GetValue()
        valid = False
        try:
            if macro == "":
                valid = True
            elif self.pronterface.macros.has_key(macro):
                valid = True
            elif hasattr(self.pronterface.__class__, u"do_"+macro):
                valid = False
            elif len([c for c in macro if not c.isalnum() and c != "_"]):
                valid = False
            else:
                valid = True
        except:
            if macro == "":
                valid = True
            elif self.pronterface.macros.has_key(macro):
                valid = True
            elif len([c for c in macro if not c.isalnum() and c != "_"]):
                valid = False
            else:
                valid = True
        self.macrob.Enable(valid)

    def macrob_handler(self, e):
        macro = self.command.GetValue()
        macro = self.pronterface.edit_macro(macro)
        self.command.SetValue(macro)
        if self.name.GetValue()=="":
            self.name.SetValue(macro)

class SpecialButton(object):

    label = None
    command = None
    background = None
    pos = None
    span = None
    tooltip = None
    custom = None

    def __init__(self, label, command, background = None, pos = None, span = None, tooltip = None, custom = False):
        self.label = label
        self.command = command
        self.pos = pos
        self.background = background
        self.span = span
        self.tooltip = tooltip
        self.custom = custom
