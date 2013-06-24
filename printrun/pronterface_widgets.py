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

from subprocess import call
def invokeAVRDude(hex_image, port, baud=115200):
  config = "tools/avrdude.conf"
  avrdude = "tools/avrdude"
  cmd = "%s -C%s -v -v -v -v -patmega2560 -cwiring -P%s -b%d -D -Uflash:w:%s:i" %(avrdude, config, port, baud, hex_image)
  print "Gravando firmware: [%s]" % (cmd)
  call(cmd, shell=True)

from tempfile import mkstemp
from webbrowser import open_new_tab
from urlgrabber import urlopen, urlgrab
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
    if self.ShowModal() == wx.ID_OK:
      pass

    self.Destroy()

  def install_fw(self, event):
    print "downloading firmware image:"
    image = self.images[event.GetId()]
    print image

    tmpfile_handle, hex_image_path = mkstemp()
    urlgrab(str(image), filename=hex_image_path)

    port = str(self.pronterface.serialport.GetValue())
    baudrate = int(self.pronterface.baud.GetValue())

    self.pronterface.disconnect(False)
    invokeAVRDude(hex_image_path, port, baudrate)
    self.pronterface.connect(False)
    #TODO: delete tmpfile

  def show_fw_source_code(self, event):
    source = self.sources[event.GetId()]
    open_new_tab(source)

  def build_firmware_list(self):
    updates_list_xml = urlopen("http://pub.metamaquina.com.br/firmware/updates.xml")
    updates_list = parse(updates_list_xml)
    i=0
    for node in updates_list.getElementsByTagName('update'):
      def getText(nodelist):
          rc = []
          for node in nodelist:
              if node.nodeType == node.TEXT_NODE:
                  rc.append(node.data)
          return ''.join(rc)

      title = getText(node.getElementsByTagName("title")[0].childNodes)
      title_text = wx.StaticText(self, -1, title)
      title_text.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

      source = getText(node.getElementsByTagName("source")[0].childNodes)
      self.sources.append(source)
      source_button = wx.Button(self, id=i, label=_("Source Code"))
      source_button.Bind(wx.EVT_BUTTON, self.show_fw_source_code)

      image = getText(node.getElementsByTagName("image")[0].childNodes)
      self.images.append(image)
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

    self.sizer.Add(self.zup1)
    self.sizer.Add(self.zup01)
    self.sizer.Add(self.zdown01)
    self.sizer.Add(self.zdown1)

  def send_gcode(self, printer):
    printer.send_now("G1 X100 Y100 Z5 F3000")

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
