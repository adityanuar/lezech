__author__ = 'aditya'
from tkinter import tix
from tkinter.constants import *
import os
from os import walk

class Application(tix.Frame):
    dir = None
    result = []
    folderSlash = "/"

    if "nt" == os.name:
        folderSlash = "\\"
    else:
        folderSlash = "/"

    def sortResult(self):
        print(self.result)
        self.result = sorted(self.result, key=lambda l:l[1], reverse=True)
        print(self.result)

    def collectData(self, path):
        f = []
        d = []
        for (pathnames, dirnames, filenames) in walk(path):
            f.extend(filenames)
            d.extend(dirnames)
            print("f:"+str(f))
            print("d:"+str(d))
            if(len(f) > 0):
                for size in f:
                    self.result.append([str(pathnames+self.folderSlash+size), int(os.stat(pathnames+self.folderSlash+size).st_size)])
            if(len(d) > 0):
                for dir in d:
                    self.collectData(str(pathnames+self.folderSlash+dir))
            break

    def show(self):
        self.result.clear()
        self.list_result.delete(0, END)
        path = self.select_dir["value"]
        self.collectData(path)
        print("result:"+str(self.result))
        self.sortResult()
        for res in self.result:
            self.list_result.insert(END, str(res[0]+"--->"+str(res[1])+" bytes"))

    def createWidgets(self):
        self.select_dir = tix.DirSelectBox(self, width=40, height=40)

        self.select_dir.pack(side=LEFT, fill=BOTH)

        self.button_show = tix.Button(self)
        self.button_show["text"] = "SHOW",
        self.button_show["command"] = self.show

        self.button_show.pack({"side": "left"})


        self.scrollbar = tix.Scrollbar(self, orient=VERTICAL)
        self.scrollbar.config(command=self.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.scrollbarX = tix.Scrollbar(self, orient=HORIZONTAL)
        self.scrollbarX.config(command=self.xview)
        self.scrollbarX.pack(side=BOTTOM, fill=X)

        self.list_result = tix.Listbox(self, width=80, height=40, yscrollcommand=self.scrollbar.set, xscrollcommand=self.scrollbarX.set)
        self.list_result.pack(fill=BOTH, expand=1, side=RIGHT)

    def yview(self, *args):
        print(args)
        self.list_result.yview_moveto(args[1])

    def xview(self, *args):
        self.list_result.xview_moveto(args[1])


    def __init__(self, master=None):
        tix.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
a = ["adit","yanuar"]
root = tix.Tk()
if "nt" == os.name:
    root.wm_iconbitmap(bitmap = "icon.ico")
else:
    root.wm_iconbitmap(bitmap = "@icon.xbm")
app = Application(master=root)
app.master.title("Lezech (fiLE siZE CHecker)")
app.master.minsize(900,400)
app.master.resizable(0, 0)
app.mainloop()
