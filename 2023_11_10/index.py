import datasource
import psycopg2
import password as pw
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PMTreeView import PMTreeView
from threading import Timer


class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        topFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth=1)
        tk.Label(topFrame,text="taiwan_pm25",font=("arial", 20), bg="#333333", fg='#ffffff',padx=10,pady=10).pack(padx=20,pady=20)
        topFrame.pack(pady=30)

        bottomFrame = tk.Frame(self)
        
        self.PMTreeView = PMTreeView(bottomFrame,show="headings",columns=('site','county','pm25','datacreationdate'),height=20)
        self.PMTreeView.pack(side='left')
        vsb = ttk.Scrollbar(bottomFrame, orient="vertical", command=self.PMTreeView.yview)
        vsb.pack(side='left',fill='y')
        self.PMTreeView.configure(yscrollcommand=vsb.set)
        bottomFrame.pack(pady=(0,30),padx=20)
        #-------------------------------------------



def main():
    def update_data(w:Window)->None:
        try:
            datasource.updata_render_data()

        except Exception:
            messagebox.showerror("錯誤",'網路不正常\n將關閉應用程式\n請稍後再試')

        lastest_data = datasource.lastest_datetime_data()
        w.PMTreeView.update_content(lastest_data)

        t = Timer(5*60, update_data,args=(window,))
        t.start()

    window = Window()
    window.title('taiwan_pm25')
    window.resizable(width=False,height=False)
    lastest_data = datasource.lastest_datetime_data()
    window.PMTreeView.update_content(lastest_data)
    t = Timer(1, update_data,args=(window,))
    t.start()         
    window.mainloop()
    
   

if __name__ == "__main__":
    main()