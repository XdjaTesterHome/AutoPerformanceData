#!/usr/bin/env python      
# -*- coding: utf-8 -*-
from Tkinter import *
from ttk import *
from tkMessageBox import *

import GUIUtil as gui_util

__author__ = 'zhouliwei'

"""
function: 主界面
date:2016/12/12

"""


class MainGUI(Frame):
    tab_array = ['CPU', '内存', '流量', '流畅度', '电量', 'kpi']

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('性能测试工具')
        gui_util.center_window(master, 1280, 800)
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()
        self.style = Style()

        tab_strip = Notebook(self.top, width=1920)
        tab_strip.place(relx=0.062, rely=0.071, relwidth=0.887, relheight=0.876)

        for tab in self.tab_array:
            tabstrip_tab = Frame(tab_strip)
            tabstrip_tablbl = Label(tabstrip_tab, text='Please add widgets in code.')
            tabstrip_tablbl.place(relx=0.1, rely=0.5)
            tab_strip.add(tabstrip_tab, text=tab)


class MainGuiEvent(MainGUI):
    def __init__(self, master=None):
        MainGUI.__init__(self, master)


if __name__ == '__main__':
    top = Tk()
    MainGuiEvent(top).mainloop()
