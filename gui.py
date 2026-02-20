# -*- encoding=utf8 -*-
# author Hesh233
from multiprocessing import freeze_support, set_start_method
from tkinter import *
from tkinter import messagebox, ttk
from process import CustomProcess
import run_daily
VERSION = "V1.6.4"
class AutoScriptGUI:
    def __init__(self):
        self.root = Tk()
        self.root.iconbitmap("pic/icon.ico") 
        self.root.report_callback_exception = self.report_callback_exception
        self.root.title(f'AGA收菜工具'+VERSION)
        self.root.resizable(False, False)        
        style = ttk.Style()
        style.configure('Green.TButton', foreground='green')
        style.map('Green.TButton', foreground=[('disabled', 'grey'),
                                               ('active','green')])
        style.configure('Red.TButton', foreground='red')
        style.map('Red.TButton', foreground=[('disabled', 'grey'),
                                             ('active','red')])
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid()
        adb_frame = ttk.Frame(main_frame, padding=10)
        adb_frame.grid(column=0, row=0)    
        status_frame = ttk.Frame(main_frame, padding=10)
        status_frame.grid(column=0, row=1)        
        button_frame = ttk.Frame(main_frame, padding=10)
        button_frame.grid(column=1, row=1)
        self.progress_bar = ttk.Progressbar(status_frame, mode='indeterminate')
        self.rouge_button = ttk.Button(
            button_frame, text='调查刷S点', command=self.rougelike_cycle,
            style='Green.TButton', width=20
        )
        self.rouge_button.grid(column=1, row=0)

        self.rouge_pass_button = ttk.Button(
            button_frame, text='调查刷S点（金币跳关）', command=self.rougelike_cycle_pass,
            style='Green.TButton', width=20
        )
        self.rouge_pass_button.grid(column=1, row=1)
        self.work_cycle_button = ttk.Button(
            button_frame, text='调查v2（未完成）', command=self.rougelike_cycle_v2,
            style='Green.TButton',width=20
        )
        self.work_cycle_button.grid(column=1, row=4)

        self.click_cycle_button = ttk.Button(
            button_frame, text='点击循环', command=self.click_cycle,
            style='Green.TButton', width=20
        )
        self.click_cycle_button.grid(column=1, row=5)


        self.rougelike_cycle_short_button = ttk.Button(
            button_frame, text='调查S点(最优路线)', command=self.rougelike_cycle_short,
            style='Green.TButton', width=20
        )
        self.rougelike_cycle_short_button.grid(column=1, row=2)

        self.rougelike_cycle_short_pass_button = ttk.Button(
            button_frame, text='最优路线金币跳过', command=self.rougelike_cycle_short_pass,
            style='Green.TButton', width=20
        )        
        self.rougelike_cycle_short_pass_button.grid(column=1, row=3)               
        self.daily_live_button = ttk.Button(
            button_frame, text='占位', command=self.daily_live,
            width=20
        )
        self.daily_live_button.grid(column=1, row=6)

        self.daily_out_work_button = ttk.Button(
            button_frame, text='占位', command=self.daily_out_work,
            width=20
        )
        self.daily_out_work_button.grid(column=1, row=7)

        self.send_flower_button = ttk.Button(
            button_frame, text='占位', command=self.send_flower,
            width=20
        )
        self.send_flower_button.grid(column=1, row=8)


        self.start_game_button = ttk.Button(
            button_frame, text='占位', command=self.start_game,
            width=20
        )
        self.start_game_button.grid(column=1, row=9)


        self.fight_test_button = ttk.Button(
            button_frame, text='战斗测试', command=self.fight_test,
            width=20
        )
        self.fight_test_button.grid(column=1, row=10)


        self.stop_progress_button = ttk.Button(
            button_frame, text='停止运行', command=self.stop_progress,
            style='Red.TButton', width=20
        )
        self.stop_progress_button.grid(column=1, row=11)
        self.stop_progress_button.config(state=DISABLED)  

        self.text_edit_text_adb = ttk.Entry(status_frame,width=5)     
        self.text_edit_text_adb.insert(0, '7555')
        self.text_edit_text_adb.grid(column=2, row=1,sticky=W)
        self.edit_text_adb_des = ttk.Label(
            status_frame, text=f'模拟器端口号:',
            font=(None, 12), foreground='green') 
        self.edit_text_adb_des.grid(column=1, row=1,sticky=W)

        self.edit_step_des = ttk.Label(
            status_frame, text=f'路线步数:',
            font=(None, 12), foreground='green') 
        self.edit_step_des.grid(column=3, row=1,sticky=W)
        self.text_edit_text3 = ttk.Entry(status_frame,width=4)     
        self.text_edit_text3.insert(0, '1',)
        self.text_edit_text3.grid(column=3, row=2,sticky=W)

        self.text_edit_text1 = ttk.Entry(status_frame,width=8)     
        self.text_edit_text1.insert(0, '800000',)
        self.text_edit_text1.grid(column=2, row=2,sticky=W)
        self.edit_text_des = ttk.Label(
            status_frame, text=f'金币跳过值:',
            font=(None, 12), foreground='green') 
        self.edit_text_des.grid(column=1, row=2,sticky=W)
        self.auto_fight_text_des = ttk.Label(
            status_frame, text=f'战斗点击类型:',
            font=(None, 12), foreground='green') 
        self.auto_fight_text_des.grid(column=1, row=3,sticky=W)
        self.attack_type = IntVar()
        self.attack_type0_button = ttk.Radiobutton(
            status_frame, text='cfg_战斗配置1', variable=self.attack_type, value=0,
        )
        self.attack_type0_button.grid(
            column=1, row=4,sticky=W)
        self.attack_type1_button = ttk.Radiobutton(
            status_frame, text='cfg_战斗配置2', variable=self.attack_type, value=1,
        )
        self.attack_type1_button.grid(
            column=1, row=5,sticky=W)    
        self.attack_type2_button = ttk.Radiobutton(
            status_frame, text='cfg_战斗配置3', variable=self.attack_type, value=2,
        )
        self.attack_type2_button.grid(
            column=1, row=6,sticky=W)    
        self.attack_type3_button = ttk.Radiobutton(
            status_frame, text='cfg_战斗配置4', variable=self.attack_type, value=3,
        )        
        self.attack_type3_button.grid(
            column=1, row=7,sticky=W)              

        self.auto_text_des = ttk.Label(
            status_frame, text=f'启动游戏类型:',
            font=(None, 12), foreground='green') 
        self.auto_text_des.grid(column=2, row=3,sticky=W)


        self.is_open_game = IntVar()
        self.is_open_game0_button = ttk.Radiobutton(
            status_frame, text='启动', variable=self.is_open_game, value=1,
        )
        self.is_open_game0_button.grid(
            column=2, row=4,sticky=W)
        self.is_open_game1_button = ttk.Radiobutton(
            status_frame, text='不启动', variable=self.is_open_game, value=0,
        )
        self.is_open_game1_button.grid(
            column=2, row=5,sticky=W)  
        self.is_open_game2_button = ttk.Radiobutton(
            status_frame, text='在目标界面', variable=self.is_open_game, value=2,
        )
        self.is_open_game2_button.grid(
            column=2, row=6,sticky=W)   
         
        self.read_spoint_text_des = ttk.Label(
            status_frame, text=f'记录速度:',
            font=(None, 12), foreground='green') 

        self.is_read_spoint = IntVar()
        self.is_read_spoint0_button = ttk.Radiobutton(
            status_frame, text='记录', variable=self.is_read_spoint, value=0,
        )

        self.read_spoint1_button = ttk.Radiobutton(
            status_frame, text='不记录', variable=self.is_read_spoint, value=1,
        )      
        self.read_spoint_text_des.grid(column=3, row=6,sticky=W)       
        self.is_read_spoint0_button.grid(
            column=3, row=7,sticky=W)
        self.read_spoint1_button.grid(
            column=3, row=8,sticky=W)      


        self.dec_shell_text_des = ttk.Label(
            status_frame, text=f'解析道具:',
            font=(None, 12), foreground='green')            
        self.is_dec_shell = IntVar()
        self.is_dec_shell_button = ttk.Radiobutton(
            status_frame, text='解析', variable=self.is_dec_shell, value=1,
        )
        self.is_dec_shell_button1 = ttk.Radiobutton(
            status_frame, text='不解析', variable=self.is_dec_shell, value=0,
        )    
        self.dec_shell_text_des.grid(column=3, row=3,sticky=W)  
        self.is_dec_shell_button.grid(
            column=3, row=4,sticky=W)        
        self.is_dec_shell_button1.grid(
            column=3, row=5,sticky=W)



           
        self.button_list = []
        self.button_list.append(self.fight_test_button)
        self.button_list.append(self.rouge_button)
        self.button_list.append(self.click_cycle_button)
        self.button_list.append(self.rouge_pass_button)
        self.button_list.append(self.daily_live_button)
        self.button_list.append(self.work_cycle_button)
        self.button_list.append(self.daily_out_work_button)
        self.button_list.append(self.rougelike_cycle_short_button)
        self.button_list.append(self.send_flower_button)
        self.button_list.append(self.start_game_button)
        # self.button_list.append(self.stop_progress_button)
        self.button_list.append(self.rougelike_cycle_short_pass_button)


    def gui_handle(self,param="", coin_count_pass=0,attack_type=0,is_open_game=0,is_read_spoint = 0,start_step=1,is_dec_shell=0,is_fight_test=0):
        for i in self.button_list:
            i.config(state=DISABLED)
        port = self.text_edit_text_adb.get()
        self.stop_progress_button.config(state=NORMAL)  

        self.progress_bar.grid(column=1, row=8)
        self.progress_bar.start()
        self.process = CustomProcess(target=run_daily.gui_run, daemon=True, 
                                     kwargs={"run_param":param,"coin_count_pass":coin_count_pass,
                                             "attack_type":attack_type,"is_open_game":is_open_game,
                                             "port":port,"is_read_spoint":not is_read_spoint,
                                             "start_step":start_step,"is_dec_shell":is_dec_shell,"is_fight_test":is_fight_test})
        # self.process = CustomProcess(target=run_daily.gui_test, daemon=True,kwargs={"run_param":param,"coin_count_pass":coin_count_pass})
        self.process.start()
        # self.process.join()
        self.root.after(200, self.update_status) 
    def update_status(self):
        if self.process.is_alive(): 
            if self.process.exception:
                self.process(self.process.exception) 
                return
            self.root.after(200, self.update_status)                      
        
        else:
            self.progress_bar.stop()
            self.progress_bar.grid_forget()    
            for i in self.button_list:
                i.config(state=NORMAL)
         
            self.stop_progress_button.config(state=DISABLED)      
    def rougelike_cycle_short_pass(self):
        step = self.text_edit_text3.get()
        is_read_spoint = self.is_read_spoint.get()
        coin_count_pass = self.text_edit_text1.get()
        attack_type = self.attack_type.get()
        is_open_game = self.is_open_game.get()         
        is_dec_shell = self.is_dec_shell.get()        
        self.gui_handle("rougelike_cycle_short_pass",int(coin_count_pass),attack_type,is_open_game,is_read_spoint=is_read_spoint,start_step=int(step),is_dec_shell=int(is_dec_shell)) 
    def fight_test(self):
        attack_type = self.attack_type.get()
        self.gui_handle("fight_test",is_fight_test=1,attack_type=attack_type)
    def send_flower(self):
        self.gui_handle("send_flower")
    def rougelike_cycle_short(self):
        step = self.text_edit_text3.get()
        is_read_spoint = self.is_read_spoint.get()
        coin_count_pass = self.text_edit_text1.get()
        attack_type = self.attack_type.get()
        is_open_game = self.is_open_game.get()    
        is_dec_shell = self.is_dec_shell.get()        
        self.gui_handle("rougelike_cycle_short",int(coin_count_pass),attack_type,is_open_game,is_read_spoint=is_read_spoint,start_step=int(step),is_dec_shell=int(is_dec_shell))     
    def daily_live(self):
        attack_type = self.attack_type.get()
        is_open_game = self.is_open_game.get()        
        self.gui_handle("daily_live",0,attack_type,is_open_game)    
    def daily_out_work(self):
        self.gui_handle("daily_out_work")  
    def rougelike_cycle_pass(self):
        is_read_spoint = self.is_read_spoint.get()
        coin_count_pass = self.text_edit_text1.get()
        attack_type = self.attack_type.get()
        is_open_game = self.is_open_game.get()                
        self.gui_handle("rougelike_cycle_pass",int(coin_count_pass),attack_type,is_open_game,is_read_spoint)          
    def rougelike_cycle(self):
        is_read_spoint = self.is_read_spoint.get()
        coin_count_pass = self.text_edit_text1.get()
        attack_type = self.attack_type.get()
        is_open_game = self.is_open_game.get()                
        self.gui_handle("rougelike_cycle",int(coin_count_pass),attack_type,is_open_game,is_read_spoint)      
    def click_cycle(self):
        coin_count_pass = self.text_edit_text1.get()
        attack_type = self.attack_type.get()
        is_open_game = self.is_open_game.get()
        self.gui_handle("click_cycle",int(coin_count_pass),attack_type,is_open_game)      
    def event_live_cycle(self):
        coin_count_pass = self.text_edit_text1.get()
        attack_type = self.attack_type.get()
        is_open_game = self.is_open_game.get()
        self.gui_handle("event_live_cycle",int(coin_count_pass),attack_type,is_open_game)
    def rougelike_cycle_v2(self):        
        coin_count_pass = self.text_edit_text1.get()
        attack_type = self.attack_type.get()
        is_open_game = self.is_open_game.get()   
        self.gui_handle("rougelike_cycle_v2",int(coin_count_pass),attack_type,is_open_game)          
    def start_game(self):
        self.gui_handle("start_game") 
    def stop_progress(self):
        print("点击停止运行")
        self.process.terminate()
        self.root.after(200, self.update_status)

    def report_callback_exception(self, exc, val, tb):
        # messagebox.showerror('Error', message=traceback.format_exc())   
        messagebox.showerror('出现错误，程序终止', message=self.process._exception)


if __name__ == '__main__':
    freeze_support()
    set_start_method('spawn') 
    # Tk.report_callback_exception = report_callback_exception

    gui = AutoScriptGUI()
    gui.root.mainloop()