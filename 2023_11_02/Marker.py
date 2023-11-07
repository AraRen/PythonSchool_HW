import tkinter as tk
import tkintermapview as tkmap

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        #建立地圖
        map_widget = tkmap.TkinterMapView(self,
                                          width=800,
                                          height=600,
                                          corner_radius=0,
                                          )
        map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        marker_1 = map_widget.set_position(25.04781739462304, 121.51733109484061,marker=True) #台北車站位置
        map_widget.set_zoom(17) #設定顯示大小
        marker_1.set_text("台北市半夜最多人的地方")
        # marker_1.set_position(48.860381, 2.338594)  # 改變位置
        # marker_1.delete()刪除

if __name__ == "__main__":
    window = Window()
    window.geometry("600x600")
    window.title("地圖")
    window.mainloop()
