from tkinter import *
from tkinter import ttk, messagebox, filedialog 
from PIL import Image, ImageTk # dùng để xử lý ảnh để hiển thị lên giao diện
import smtplib # thư viện gửi email giao thức smtp
from email.message import EmailMessage
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import signal


class Program:
    lowpass_ = Image.open('LocThongThap.png').resize((384, 164))  # resize tỉ lệ 1:2
    highpass_ = Image.open('LocThongCao.png').resize((378, 170)) # resize tỉ lệ 1:2
    bandpass_ = Image.open('LocThongDai.png').resize((382, 192)) # resize tỉ lệ 1:2
    bandreject_ = Image.open('LocChanDai.png').resize((366, 186)) # resize tỉ lệ 1:2

    formu_lp_ = Image.open('Formular_LP.png').resize((390, 205)) # resize tỉ lệ 1:2
    formu_hp_ = Image.open('Formular_HP.png').resize((376, 204)) # resize tỉ lệ 1:2
    formu_bp_ = Image.open('Formular_BP.png').resize((366, 206)) # 1:2
    formu_br_ = Image.open('Formular_BR.png').resize((366, 175))  # 1:1.7

    def __init__(self):
        self.root = Tk()
        self.root.title("Digital Signal Processing App")
        self.root.geometry('1200x700')
        self.root.resizable(0, 0)
        self.make_center()

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
        
        
        ######################################################
        # TAB 1
        ######################################################
        # Tab1
        self.lbl1 = ttk.Label(self.tab1, text="Lý thuyết")
        self.lbl1.pack(padx=10, pady=10)

        self.principle_note = ttk.Notebook(self.tab1)
        self.lowpass_f = ttk.Frame(self.principle_note)
        self.highpass_f = ttk.Frame(self.principle_note)
        self.bandpass_f = ttk.Frame(self.principle_note)
        self.bandreject_f = ttk.Frame(self.principle_note)

        self.principle_note.add(child=self.lowpass_f, text="Low Pass Filter")
        self.principle_note.add(child=self.highpass_f, text="High Pass Filter")
        self.principle_note.add(child=self.bandpass_f, text="Band Pass Filter")
        self.principle_note.add(child=self.bandreject_f, text="Band Reject Filter")

        self.principle_note.bind("<<NotebookTabChanged>>", self.on_filter_tab_selected)

        # Lý thuyết bộ lọc thông thấp
        self.lbl_lowpass = ttk.Label(self.lowpass_f, text="Bộ lọc thông thấp (Low Pass Filter)")
        self.lbl_lowpass.grid(row=0, column=3, padx=10, pady=10)
        self.concept_lp = ttk.Label(self.lowpass_f, text="Khái niệm: Bộ lọc thông thấp là bộ lọc cho phép chúng ta giữ lại các \nthành phần tần số ở mức thấp hơn một giới hạn nhất định, gọi \nlà mức cắt (omega cắt) (cut-off frequency), và loại bỏ các thành phần tần số ở mức cao hơn.")
        self.concept_lp.grid(row=1, column=0, padx=5, pady=5, sticky='w') # w: west: căn trái
        self.lowpass = ImageTk.PhotoImage(Program.lowpass_)
        self.lp = ttk.Label(self.lowpass_f, image=self.lowpass)
        self.lp.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.formu_lp = ImageTk.PhotoImage(Program.formu_lp_)
        self.formular_lp = ttk.Label(self.lowpass_f, image=self.formu_lp)
        self.formular_lp.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.lp_application = ttk.Label(self.lowpass_f, text="Ứng dụng:\nXử Lý Âm Thanh: Trong âm thanh, bộ lọc thông thấp có thể được sử dụng để loại bỏ nhiễu cao tần không mong muốn.\nXử Lý Ảnh: Trong xử lý ảnh, nó có thể được sử dụng để làm mịn ảnh hoặc loại bỏ nhiễu cao tần.")
        self.lp_application.grid(row=4, column=0, padx=5, pady=5)
        
        # lý thuyết bộ lọc thông cao
        self.lbl_highpass = ttk.Label(self.highpass_f, text="Bộ lọc thông cao (High Pass Filter)")
        self.lbl_highpass.place(x=500, y=10)
        # self.lbl_highpass.grid(row=0, column=3, padx=5, pady=5)
        self.concept_hp = ttk.Label(self.highpass_f, text="Khái niệm: Bộ lọc thông cao số là một hệ thống xử lý tín hiệu số được thiết kế để giảm độ chói \nhoặc loại bỏ các thành phần tần số ở mức thấp hơn một giới hạn cắt nhất định và giữ \nlại hoặc tăng cường độ chói của các thành phần tần số cao hơn.")
        self.concept_hp.place(x=50, y=30) # w: west: căn trái
        # self.concept_hp.grid(row=1, column=0, padx=5, pady=5, sticky='w') # w: west: căn trái
        self.highpass = ImageTk.PhotoImage(Program.highpass_)
        self.hp = ttk.Label(self.highpass_f, image=self.highpass)
        self.hp.place(x=50, y=100)
        # self.hp.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.formu_hp = ImageTk.PhotoImage(Program.formu_hp_)
        self.formular_hp = ttk.Label(self.highpass_f, image=self.formu_hp)
        self.formular_hp.place(x=50, y=300)
        # self.formular_hp.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.hp_application = ttk.Label(self.highpass_f, text="Ứng dụng:\nXử Lý Âm Thanh: Loại bỏ hoặc giảm độ chói của âm thanh tần số thấp không mong\
            \nmuốn, như tiếng ồn hậu kỳ, tiếng động.\
            \nXử Lý Ảnh: Lọc nổi bật các đặc trưng tần số cao trong ảnh, giúp phân biệt chi tiết\
            \nnhỏ và kích thích việc nhận diện.\
            \nTruyền Thông Số: Trong việc truyền thông số, bộ lọc thông cao có thể được sử dụng\
            \nđể loại bỏ nhiễu tần số thấp từ tín hiệu, giữ lại tín hiệu chính.\
            \nXử Lý Tín Hiệu Video: Trong xử lý video, bộ lọc thông cao được sử dụng để làm\
            \nsáng hoặc làm nổi bật các đối tượng tương phản trong cảnh quan.\
            \nTruyền Thông Dữ Liệu: Trong các hệ thống truyền thông số, bộ lọc thông cao có thể\
            \nđược sử dụng để giảm nhiễu và tăng độ chói của tín hiệu truyền.")
        self.hp_application.place(x=500, y=300)
        # self.hp_application.grid(row=4, column=0, padx=5, pady=5)

        # lý thuyết bộ lọc thông dải
        self.lbl_bandpass = ttk.Label(self.bandpass_f, text="Bộ lọc thông dải (Band Pass Filter)")
        self.lbl_bandpass.place(x=500, y=10)
        # self.lbl_bandpass.grid(row=0, column=0, padx=10, pady=10)
        self.concept_bp = ttk.Label(self.bandpass_f, text="Khái niệm: Bộ lọc thông dải số (Digital Band Pass Filter - BPF) là một hệ thống xử lý tín hiệu\
            \nsố được thiết kế để chọn lọc hoặc tăng cường các thành phần tần số trong một dải\
            \ntần số cụ thể, giữ lại các tần số ở mức trung bình trong dải được chọn và loại bỏ các\
            \ntần số ở mức thấp và cao hơn.")
        self.concept_bp.place(x=50, y=30) # w: west: căn trái
        # self.concept_bp.grid(row=1, column=0, padx=5, pady=5, sticky='w') # w: west: căn trái
        self.bandpass = ImageTk.PhotoImage(Program.bandpass_)
        self.bp = ttk.Label(self.bandpass_f, image=self.bandpass)
        self.bp.place(x=50, y=100)
        # self.bp.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.formu_bp = ImageTk.PhotoImage(Program.formu_bp_)
        self.formular_bp = ttk.Label(self.bandpass_f, image=self.formu_bp)
        self.formular_bp.place(x=50, y=300)
        # self.formular_bp.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.bp_application = ttk.Label(self.bandpass_f, text="Ứng dụng:\
            \nTruyền Thông Số: Trong truyền thông số, bộ lọc thông dải được sử dụng để chọn lọc\
            \nhoặc tăng cường một dải tần số cụ thể của tín hiệu truyền thông.\
            \nXử Lý Âm Thanh: Bộ lọc thông dải số có thể được sử dụng để tách hoặc\
            \ntăng cường các thành phần âm thanh trong một khoảng tần số cụ thể, giúp trong việc chế biến âm nhạc.\
            \nXử Lý Ảnh và Video: Trong xử lý ảnh và video, bộ lọc thông dải có thể được sử\
            \ndụng để làm nổi bật hoặc loại bỏ các đối tượng ở một dải tần số nhất định.\
            \nDò Tìm Tín Hiệu: Trong dò tìm tín hiệu, bộ lọc thông dải có thể được sử dụng để\
            \nchọn lọc tín hiệu từ môi trường và loại bỏ nhiễu không mong muốn.\
            \nTruyền Tải Dữ Liệu: Trong hệ thống truyền tải dữ liệu, bộ lọc thông dải có thể được\
            \nsử dụng để tách các kênh truyền thông cụ thể.")
        self.bp_application.place(x=500, y=300)
        # self.bp_application.grid(row=4, column=0, padx=5, pady=5)


        # lý thuyết bộ lọc chặn dải
        self.lbl_bandreject = ttk.Label(self.bandreject_f, text="Bộ lọc chặn dải (Band Reject Filter)")
        self.lbl_bandreject.grid(row=0, column=3, padx=10, pady=10)
        self.concept_br = ttk.Label(self.bandreject_f, text="Khái niệm: Bộ lọc chặn dải (Digital Band Stop Filter) là một hệ thống xử lý tín hiệu số được\
            \nthiết kế để loại bỏ hoặc giảm độ chói của các thành phần tần số nằm trong một\
            \nkhoảng tần số cụ thể, trong khi giữ lại hoặc truyền qua các thành phần tần số ở các\
            \nkhoảng tần số khác.")
        self.concept_br.grid(row=1, column=0, padx=5, pady=5, sticky='w') # w: west: căn trái
        self.bandreject = ImageTk.PhotoImage(Program.bandreject_)
        self.br = ttk.Label(self.bandreject_f, image=self.bandreject)
        self.br.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.formu_br = ImageTk.PhotoImage(Program.formu_br_)
        self.formular_br = ttk.Label(self.bandreject_f, image=self.formu_br)
        self.formular_br.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.br_application = ttk.Label(self.bandreject_f, text="Ứng dụng:Loại Bỏ Nhiễu Tần Số: Bộ lọc chặn dải số được sử dụng để loại bỏ nhiễu ở các khoảng tần số cụ thể mà không ảnh hưởng đến các tần số khác.\
            \nXử Lý Âm Thanh: Trong xử lý âm thanh, nó có thể được sử dụng để loại bỏ tiếng ồn có tần số nằm trong một khoảng cụ thể.\
            \nXử Lý Ảnh và Video: Bộ lọc chặn dải số có thể được sử dụng để loại bỏ nhiễu hoặc các thành phần tần số không mong muốn trong xử lý ảnh và video.\
            \nTruyền Thông Số: Trong truyền thông số, nó có thể được sử dụng để loại bỏ nhiễu hoặc tín hiệu ngoại vi không mong muốn.\
            \nDò Tìm Tín Hiệu: Trong dò tìm tín hiệu, bộ lọc chặn dải số có thể được sử dụng để lọc ra các tín hiệu từ môi trường và loại bỏ nhiễu.")
        self.br_application.grid(row=4, column=0, padx=5, pady=5)

        self.principle_note.pack(padx=10, pady=10, fill="both", expand="True")

        ######################################################
        # END TAB 1
        ######################################################


        ######################################################
        # TAB 2
        ######################################################
        self.lbl2 = ttk.Label(self.tab2, text="Thiết kế bộ lọc butterworth")
        self.lbl2.pack(padx=20, pady=20)
        
        self.options = ttk.Combobox(self.tab2)
        self.options['values'] = (
            "Lọc Thông Thấp",
            "Lọc Thông Cao",
            "Lọc Thông Dải",
            "Lọc Chặn Dải"
            )
        self.options.place(x=50, y=10)
        self.options.current(0)

        # Bộ lọc thông dải
        '''
        Thiết kế bộ lọc thông dải cần quan tâm các tham số:
        Tần số lấy mẫu: f_sample (điều kiện > 2 * f_max)
        Tần số dải thông: f_pass_min và f_pass_max
        Tần số dải chặn: f_stop_min và f_stop_max
        Khoảng cách f_pass_min và f_stop_min nên là 350
        fs: là frequency slope và nằm trong phạm vi (0, 1]
        Td: chu kỹ lấy mẫu và thường là 1
        g_pass: gain pass
        g_stop: gain stop
        '''
        self.bandpass_frame = ttk.Frame(self.tab2)
        self.bandpass_frame.place(x=50, y=50, width=300, height=400)

        self.f_sample_var = DoubleVar(value=7000)
        self.f_pass_min_var = DoubleVar(value=1400)
        self.f_pass_max_var = DoubleVar(value=2100)
        self.f_stop_min_var = DoubleVar(value=1050)
        self.f_stop_max_var = DoubleVar(value=2450)
        self.fs_var = DoubleVar(value=0.5)
        self.Td_var = DoubleVar(value=1)
        self.g_pass_var = DoubleVar(value=0.4)
        self.g_stop_var = DoubleVar(value=50)

        # Create and place input labels and entry widgets
        input_labels = ["Sampling Frequency:", "Passband Frequency (Min):", "Passband Frequency (Max):",
                        "Stopband Frequency (Min):", "Stopband Frequency (Max):", "Sampling Time:", "Passband Ripple:",
                        "Stopband Attenuation:"]
        input_vars = [self.f_sample_var, self.f_pass_min_var, self.f_pass_max_var, self.f_stop_min_var,
                      self.f_stop_max_var, self.Td_var, self.fs_var, self.g_pass_var, self.g_stop_var]

        for i, label_text in enumerate(input_labels):
            label = ttk.Label(self.bandpass_frame, text=label_text)
            label.grid(column=0, row=i, padx=10, pady=5, sticky=W)

            entry = ttk.Entry(self.bandpass_frame, textvariable=input_vars[i], width=10)
            entry.grid(column=1, row=i, padx=10, pady=5, sticky=W)

        # Create and place the "Plot" button
        plot_button = ttk.Button(self.bandpass_frame, text="Plot", command=self.plot_response)
        plot_button.grid(column=1, row=len(input_labels), pady=10)


        self.create_plot_canvas()
        ######################################################
        # END TAB 2
        ######################################################

        ######################################################
        # TAB 3
        ######################################################
        self.lbl_frm_3 = ttk.LabelFrame(self.tab3, text="Gửi ý kiến của bạn đến nhóm phát triển")
        self.lbl_frm_3.grid(row=0, column=0, padx=50, pady=10)

        self.email_lbl = ttk.Label(self.lbl_frm_3, text="Nhập Email của bạn: ")
        self.email_lbl.grid(row=0, column=0, padx=10, pady=10)
        self.email_ent = ttk.Entry(self.lbl_frm_3, width=75)
        self.email_ent.grid(row=0, column=1, padx=10, pady=10)

        self.subject_mail = ttk.Label(self.lbl_frm_3, text="Nhập tiêu đề email: ")
        self.subject_mail.grid(row=1, column=0, padx=10, pady=10)
        self.subject_ent = ttk.Entry(self.lbl_frm_3, width=75)
        self.subject_ent.grid(row=1, column=1, padx=10, pady=10)

        self.body_mail = ttk.Label(self.lbl_frm_3, text="Nhập nội dung email:")
        self.body_mail.grid(row=2, column=0, padx=10, pady=10)

        self.body_mail_text = Text(self.lbl_frm_3, width=60)
        self.body_mail_text.grid(row=3, column=1, padx=10, pady=10)

        # self.attactment_btn = ttk.Button(self.lbl_frm_3, text='Đính kèm file')
        # self.attactment_btn.grid(row=4, column=1, padx=10, pady=10, sticky='w') # west: tây, căn trái
        self.submit_btn = ttk.Button(self.lbl_frm_3, text='Gửi', command=self.submit_form)
        self.submit_btn.grid(row=5, column=1, padx=10, pady=10, sticky='w')
        self.result_lbl = ttk.Label(self.lbl_frm_3, text='')
        self.result_lbl.grid(row=5, column=2, padx=10, pady=10)
        ######################################################
        # TAB 3
        ######################################################

        # Hiển thị Notebook
        self.notebook.pack(padx=10, pady=10, fill="both", expand="True")
        


    def on_tab_selected(self, event):
        selected_tab = self.notebook.index(self.notebook.select())
        print(f"Tab {selected_tab + 1} selected")
        pass

    
    def on_filter_tab_selected(self, event):
        selected_filter = self.principle_note.index(self.principle_note.select())
        print(f"Filter {selected_filter + 1} selected")
        pass


    def create_plot_canvas(self):
        self.plot_frame = ttk.Frame(self.tab2)
        self.plot_frame.place(x=400, y=50, width=700, height=600)
        # self.plot_frame.place(x=400, y=50, width=700, height=600)

        self.fig, self.ax = plt.subplots(nrows=2, ncols=2, figsize=(10,12), tight_layout=True)
        self.canvas1 = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        # self.canvas1.get_tk_widget().place(x=0,y=0,width=300,height=290)
        self.canvas1.get_tk_widget().pack(expand=True, fill='both')

    def plot_response(self):
        # Get the input values
        f_sample = self.f_sample_var.get()
        f_pass_min = self.f_pass_min_var.get()
        f_pass_max = self.f_pass_max_var.get()
        f_stop_min = self.f_stop_min_var.get()
        f_stop_max = self.f_stop_max_var.get()
        fs = self.fs_var.get()
        Td = self.Td_var.get()
        g_pass = self.g_pass_var.get()
        g_stop = self.g_stop_var.get()

        # Specifications of Filter
        f_pass = [f_pass_min, f_pass_max]
        f_stop = [f_stop_min, f_stop_max]

        # Conversion to prewrapped analog frequency
        omega_p = self.convertX(f_sample, f_pass)
        omega_s = self.convertX(f_sample, f_stop)

        # Design of Filter using signal.buttord function
        N, Wn = signal.buttord(omega_p, omega_s, g_pass, g_stop, analog=True)

        # Conversion in Z-domain
        b, a = signal.butter(N, Wn, 'bandpass', True)
        z, p = signal.bilinear(b, a, fs)

        # Frequency Response
        w, h = signal.freqz(z, p, 512)

        # Clear previous plots
        for ax_row in self.ax:
            for ax in ax_row:
                ax.clear()

        # Plot the magnitude response
        self.ax[0, 0].semilogx(w, 20 * np.log10(abs(h)))
        self.ax[0, 0].set_xscale('log')
        self.ax[0, 0].set_title('Butterworth filter frequency response')
        self.ax[0, 0].set_xlabel('Frequency [Hz]')
        self.ax[0, 0].set_ylabel('Amplitude [dB]')
        self.ax[0, 0].margins(0, 0.1)
        self.ax[0, 0].grid(which='both', axis='both')
        self.ax[0, 0].axvline(100, color='green')

        # Impulse Response
        imp = signal.unit_impulse(40)
        c, d = signal.butter(N, 0.5)
        response = signal.lfilter(c, d, imp)

        self.ax[1, 0].stem(np.arange(0, 40), imp, markerfmt='D', basefmt=' ')
        self.ax[1, 0].stem(np.arange(0, 40), response, basefmt=' ')
        self.ax[1, 0].margins(0, 0.1)
        self.ax[1, 0].set_xlabel('Time [samples]')
        self.ax[1, 0].set_ylabel('Amplitude')
        self.ax[1, 0].grid(True)

        # Phase Response
        angles = np.unwrap(np.angle(h))
        self.ax[1, 1].plot(w / 2 * np.pi, angles, 'g')
        self.ax[1, 1].grid()
        self.ax[1, 1].axis('tight')
        self.ax[1, 1].set_title('Digital filter phase response')
        self.ax[1, 1].set_ylabel('Angle (radians)')
        self.ax[1, 1].set_xlabel('Frequency [Hz]')

        # Redraw canvas
        self.canvas1.draw()


    
    def convertX(self, f_sample, f):
        w = []
        for i in range(len(f)):
            b = 2 * ((f[i] / 2) / (f_sample / 2))
            w.append(b)

        omega_mine = []

        for i in range(len(w)):
            c = (2 / self.Td_var.get()) * np.tan(w[i] / 2)
            omega_mine.append(c)

        return omega_mine

    def make_center(self):
        self.root.update_idletasks()
        width = self.root.winfo_width() # width of root
        height = self.root.winfo_height() # height of root

        # x, y là vị trí xuất hiện trên màn hình
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        return


    def submit_form(self):
        user_email = str(self.email_ent.get()).strip()
        subject_email = str(self.subject_ent.get()).strip()
        body_email = str(self.body_mail_text.get("1.0", "end-1c"))

        if not user_email or not subject_email or not body_email: # nếu 1 trong các trường trên trống
            messagebox.error(title='error', message="Vui lòng điền đầy đủ thông tin vào các trường trên!")
        else: # nếu đã điền đủ thông tin
            # kiểm tra tất cả các trường đã đầy đủ và không trống hay không
            if self.is_email(user_email):
                print("Valid")
                # email hợp lệ thì mới gửi email
                result = self.send_feedback(user_email, subject_email, body_email)
                self.result_lbl.configure(text=result)
                self.result_lbl.grid(row=5, column=2, padx=10, pady=10)
                self.result_lbl.after(2000, self.result_lbl.destroy) # sau 2s gửi thông báo cho user là có thành công hay không?
                self.lbl_frm_3.after(2000, self.clear_input) # sau 2s clear input
            else:
                # không hợp lệ thì thông báo lỗi
                print("Invalid")
                messagebox.error(title='error', message="Email không hợp lệ!!!")
            # print(user_email)

    
    def clear_input(self):
        self.email_ent.delete(0, "end")
        self.subject_ent.delete(0, "end")
        self.body_mail_text.delete("1.0", "end")
        pass
    

    def is_email(self, email):
        """
        Hàm kiểm tra xem email có hợp lệ hay không bằng biểu thức chính quy
        """
        # r: raw string
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(regex, email):  # hàm này trả về None nếu mẫu không khớp
            return True
        else:
            return False
        
    
    # gửi email
    def send_feedback(self, user_mail, subject_mail, body_mail, attactment_file=None):
        """
        user_mail: email của user, sau khi nhà phát triển giải đáp các phản hồi của user thì sẽ lấy thông tin này để gửi
        subject_mail: tiêu đề phản hồi về ứng dụng của user
        body_mail: nội dung phản hồi
        attactment_file = None: tham số mặc định, user có thể đính kém file hoặc không?
        """
        # trong python quy ước hằng số viết in hoa và không thể gán lại
        SOURCE_EMAIL = 'nl142857nl@outlook.com.vn' # Email của ứng dụng
        PASSWORD = '@nl142857D1019'
        DESTINATION_EMAIL = 'rinnmusic2.2@gmail.com' # Email của nhóm phát triển
        MAIL_SERVER = 'smtp.office365.com'  # input: microsoft là smtp.office365.com ; google là smtp.gmail.com
        MAIL_PORT = 587 # microsort = 587, google 587 (bảo mật TLS - Transport Layer Security), 465 (SSL - Secure Socket Layer)
        subject_mail_ = subject_mail
        body_mail_ = "Xin chào nhóm phát triển ứng dụng,\r\n" + f"Feedback từ: {user_mail}" + "\r\n" + body_mail + "\r\n" + "Trân trọng!"

        email = EmailMessage()
        email['To'] = DESTINATION_EMAIL
        email['From'] = SOURCE_EMAIL
        email['Subject'] = subject_mail_
        email.set_content(body_mail_)

        if attactment_file: # nếu file tồn tại
            with open(file=attactment_file, mode='rb') as f:
                data = f.read()
                email.add_attachment(data, maintype='text', subtype='plain', filename=f.name)

        try:
            connection = smtplib.SMTP(host=MAIL_SERVER, port=MAIL_PORT)
            connection.starttls() # bảo mật tls: Transport Layer Security
            connection.login(SOURCE_EMAIL, PASSWORD)
            connection.send_message(from_addr=SOURCE_EMAIL, to_addrs=DESTINATION_EMAIL, msg=email)
            connection.quit()
            return "Gửi thành công! Bạn sẽ nhận được phản hồi trong vòng 48h!"
            
        except Exception as e:
            print(e)
            return f"{e}"

if __name__ == '__main__':
    app = Program()
    app.root.mainloop()