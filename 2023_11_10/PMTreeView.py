from tkinter import ttk

class PMTreeView(ttk.Treeview):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,**kwargs)
        self.heading('site',text='測站名稱')
        self.heading('county',text='縣市名稱')
        self.heading('pm25',text='細懸浮微粒濃度')
        self.heading('datacreationdate',text='資料建置日期')

        self.column('site',width=120)
        self.column('county',width=120)
        self.column('pm25',width=60)
        self.column('datacreationdate',width=270)



    def update_content(self,site_datas):
        '''
        更新內容
        '''
        #清除所有內容
        for i in self.get_children():
            self.delete(i)
        
        for site in site_datas:
            self.insert('','end',values=site)