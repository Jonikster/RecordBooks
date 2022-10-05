import glob
import os
import wx
import recorder
from chardet.universaldetector import UniversalDetector

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        self.count = 1
        self.gl = glob.glob('*.wav')
        if len(self.gl) != 0:
            for g in self.gl:
                if g.split('.')[0].isdigit():
                    if int(g.split('.')[0]) > self.count:
                        self.count = int(g.split('.')[0])
            if self.count > 1:
                self.count += 1
        self.r = recorder.Recorder()
        self.encoding = ''
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()
        filemenu = wx.Menu()
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", " Open a file")
        menuSave = filemenu.Append(wx.ID_SAVE, "&Save", " Save a file")
        menuSaveAs = filemenu.Append(wx.ID_SAVEAS, "&Save as", " Save a file as")
        menuClear = filemenu.Append(wx.ID_ANY, "&Clear", " Clear audio files")
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit", " Terminate the program")
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, menuSaveAs)
        self.Bind(wx.EVT_MENU, self.OnClear, menuClear)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        open_id = wx.NewIdRef()
        save_id = wx.NewIdRef()
        save_as_id = wx.NewIdRef()
        record_id = wx.NewIdRef()
        stop_id = wx.NewIdRef()
        play_id = wx.NewIdRef()
        delete_id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.OnOpen, id=open_id)
        self.Bind(wx.EVT_MENU, self.OnSave, id=save_id)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, id=save_as_id)
        self.Bind(wx.EVT_MENU, self.OnKeyRecord, id=record_id)
        self.Bind(wx.EVT_MENU, self.OnKeyStop, id=stop_id)
        self.Bind(wx.EVT_MENU, self.OnKeyPlay, id=play_id)
        self.Bind(wx.EVT_MENU, self.OnKeyDelete, id=delete_id)
        entries = [wx.AcceleratorEntry() for i in range(7)]
        entries[0].Set(wx.ACCEL_CTRL, ord('O'), open_id)
        entries[1].Set(wx.ACCEL_CTRL, ord('S'), save_id)
        entries[2].Set(wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord('S'), save_as_id)
        entries[3].Set(wx.ACCEL_CTRL, ord('1'), record_id)
        entries[4].Set(wx.ACCEL_CTRL, ord('2'), stop_id)
        entries[5].Set(wx.ACCEL_CTRL, ord('3'), play_id)
        entries[6].Set(wx.ACCEL_CTRL, ord('4'), delete_id)
        a_tbl = wx.AcceleratorTable(entries)
        self.SetAcceleratorTable(a_tbl)
        self.Show(True)
    def OnOpen(self, e):
        self.dirname = ""
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            detector = UniversalDetector()
            for line in open(os.path.join(self.dirname, self.filename), 'rb'):
                detector.feed(line)
                if detector.done: break
            detector.close()
            self.encoding = detector.result['encoding']
            f = open(os.path.join(self.dirname, self.filename), 'r', encoding=detector.result['encoding'], errors='ignore')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()
    def OnSave(self, e):
        try:
            if self.encoding != '':
                f = open(os.path.join(self.dirname, self.filename), 'w', encoding=self.encoding)
                f.write(self.control.GetValue())
                f.close()
            else:
                f = open(os.path.join(self.dirname, self.filename), 'w', encoding='utf8')
                f.write(self.control.GetValue())
                f.close()
        except:
            try:
                dlg = wx.FileDialog(self, "Save to file", ".", "", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                if (dlg.ShowModal() == wx.ID_OK):
                    self.filename = dlg.GetFilename()
                    self.dirname = dlg.GetDirectory()
                    f = open(os.path.join(self.dirname, self.filename), 'w', encoding='utf8')
                    f.write(self.control.GetValue())
                    f.close()
                dlg.Destroy()
            except:
                pass
    def OnSaveAs(self, event):
        try:
            dlg = wx.FileDialog(self, "Save to file", ".", "", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if (dlg.ShowModal() == wx.ID_OK):
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                f = open(os.path.join(self.dirname, self.filename), 'w', encoding='utf8')
                f.write(self.control.GetValue())
                f.close()
            dlg.Destroy()
        except:
            pass
    def OnClear(self, e):
        gl = glob.glob('*.wav')
        if len(gl) != 0:
            for g in gl:
                os.remove(g)
            self.count = 1
    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "A Record text editor", "About Record Books", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
    def OnExit(self, e):
        self.Close(True)
    def OnKeyRecord(self, e):
            self.r.record(str(self.count))
    def OnKeyStop(self, e):
            self.r.stop()
            self.count += 1
    def OnKeyPlay(self, e):
            self.r.play(str(self.count-1))
    def OnKeyDelete(self, e):
            if os.path.exists(str(self.count-1) + '.wav'):
                os.remove(str(self.count-1) + '.wav')
                if self.count > 1:
                    self.count -= 1
app = wx.App(False)
frame = MainWindow(None, "Record Books 1.1")
app.MainLoop()