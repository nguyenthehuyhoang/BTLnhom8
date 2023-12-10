from tkinter import *
from tkinter import ttk 


class Program:
    def __init__(self):
        self.root = Tk()
        self.root.title("Digital Signal Processing App")
        self.root.geometry('1200x700')
        self.root.resizable(0, 0)

        self.notebook = ttk.Notebook(self.root)
        
        # tạo các tab trong notebook
        # tab1 về lý thuyết một số bộ lọc
        self.tab1 = ttk.Frame(self.notebook)

        # tab2 về thiết kế bộ lọc
        self.tab2 = ttk.Frame(self.notebook)

        # tab3 về đóng góp, phản hồi từ user cho developer
        self.tab3 = ttk.Frame(self.notebook)

        # thêm các tab vào notebook
        self.notebook.add(child=self.tab1, text="Priciples")
        self.notebook.add(child=self.tab2, text="Filter Design")
        self.notebook.add(child=self.tab3, text="Feedback")

        # thêm sự kiện vào notebook để chuyển tab
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
        
        
        # Tab1
        self.lbl1 = ttk.Label(self.tab1, text="This is Tab 1")
        self.lbl1.pack(padx=10, pady=10)

        # Tab2 
        self.lbl2 = ttk.Label(self.tab2, text="This is Tab 2")
        self.lbl2.pack(padx=20, pady=20)

        # Tab 3
        self.lbl3 = ttk.Label(self.tab3, text="This is Tab 3")
        self.lbl3.pack(padx=15, pady=15)

        # Hiển thị Notebook
        self.notebook.pack(padx=10, pady=10, fill="both", expand="True")
        


    def on_tab_selected(self, event):
        selected_tab = self.notebook.index(self.notebook.select())
        print(f"Tab {selected_tab + 1} selected")
        pass


if __name__ == '__main__':
    app = Program()
    app.root.mainloop()