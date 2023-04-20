HTML_INDEX = 'plagiarism\sources\html'
SOURCE_INDEX = 'plagiarism\sources\source.txt'
PACKAGES = 'plagiarism\matcher'
from tkinter import *
from text_matcher import cli
from googlesearch import search
from requests import get
import html2text
from re import split
from bs4 import BeautifulSoup
from time import sleep
#nltk.download('stopwords')

class HtmlSearch():
    def __init__(self):
        self.data = ""
        self.clear_data_url = []
        self.query_number = 2
        self.url_list()
        self.check_html()
    
    def clear_text(self, url):
        html = (get(url)).text
        soup = BeautifulSoup(html, features="html.parser")
        h = html2text.HTML2Text()
        h.ignore_links = True
        text = h.handle(soup.prettify())
        return text

    def part_file(self, source_text):
        sentences = [x for x in split("[//.|//!|//?]", source_text) if x!=""]
        return sentences

    def url_list(self):
        with open(SOURCE_INDEX, "r", encoding='utf8') as text:
            self.data = text.read()
            lines = self.part_file(self.data)
            print(lines)
            number = 0
            for line in lines:
                for url in search(line, lang='tr'):
                    self.clear_data_url.append(url)
                    number += 1
                    if number >= self.query_number:
                        break
                sleep(self.query_number)
            
    def check_html(self):
        # file_list = os.listdir(HTML_INDEX)
        # if not file_list:
        #     print("ERROR")
        # else:
        file_order = 0
        for url in self.clear_data_url:
            # with open(f"plagiarism\results\html_urls.txt", "a", encoding="utf8") as urls:
            #     urls.write(url)
            with open(f"{HTML_INDEX}\html_document_{file_order}.txt", "+w", encoding="utf8") as indexed_html:
                indexed_html.write(self.clear_text(url))
                file_order +=1
class MainWindow():
    def __init__(self):
        self.window = Tk()
        self.data=""
        self.button_state = "New Input"
        self.log_frame = Frame(self.window)
        self.log = Text(self.log_frame, height=2, width=50)
        self.frame_text = Frame(self.window)
        self.textbox = Text(self.frame_text, height=10, width=50)
        self.logFrame()
        self.quickConfig()
        self.backup = self.read_file()
        self.window.mainloop()
         
    def quickConfig(self):
        self.window.title("PLAGIARISM CHECKER")
        self.window.minsize(width=440, height=400)
        self.window.config(padx=10, pady=10)
        #Label
        my_label = Label(text="Plagiarism Checker", font=("Arial", 24, "bold"))
        my_label.grid(column=0, row=0)
        #Button
        button_frame = Frame()
        button_frame.grid(column=0, row=1 ,sticky=W+E)
        button_frame.config(pady=20)
        button_run = Button(button_frame, text="Run Process", command=self.use_input)
        button_see = Button(button_frame, text="See the '.txt' file.", command=self.read_file)
        button_new = Button(button_frame, text=self.button_state, command=lambda: self.new_input(button_new))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        button_see.grid(row=0, column=0)
        button_run.grid(row=0, column=1)
        button_new.grid(row=0, column=2)
        #Textbox
        self.frame_text.grid(column=0, row=2)
        self.frame_text.config(pady=5)
        self.textbox = Text(self.frame_text, height=10, width=50)
        self.textbox.delete('1.0', END)
        self.textbox.grid(column=0, row=0, columnspan=9, rowspan=10)
        self.textbox.config(padx=10, pady=10)
        sb = Scrollbar(self.frame_text)
        self.textbox.config(yscrollcommand=sb.set)
        sb.config(command=self.textbox.yview)
        sb.grid(column=10, row=0, rowspan=10,  sticky=N+S)
        #Button
        button_frame_2 = Frame()
        button_frame_2.grid(column=0, row=3, sticky=W+E)
        button_frame_2.config(pady=20)
        button_frame_2.columnconfigure(0, weight=16)
        button_frame_2.columnconfigure(1, weight=6)
        button_frame_2.columnconfigure(2, weight=1)
        button_frame_2.columnconfigure(3, weight=6)
        checked_state = IntVar()
        checkbutton = Checkbutton(button_frame_2, text="Write backup '.txt'?", variable=checked_state)
        checkbutton.grid(column=1, row=1, columnspan=3)
        reset = Button(button_frame_2, text="Reset", command=lambda: self.reset_app(checked_state.get()))
        reset.grid(column=1, row=0, sticky=E)
        exit = Button(button_frame_2, bg="#EBC2BD", text="Exit", command=lambda: self.terminate(checked_state.get()))
        exit.grid(column=3, row=0, sticky=W)
        
    def logFrame(self):
        self.log_frame.grid(column=0, row=4)
        self.log_frame.config(pady=2)
        self.log.grid(column=0, row=0, columnspan=8, rowspan=10)
        self.log.config(padx=10, pady=10)
        log_sb = Scrollbar(self.log_frame)
        self.log.config(yscrollcommand=log_sb.set)
        log_sb.config(command=self.log.yview)
        log_sb.grid(column=9, row=0, rowspan=10,  sticky=N+S)
        reset_log = Button(self.log_frame, text="Reset", command=self.reset_l)
        save_log = Button(self.log_frame, text="Save", command=lambda: self.save_l(self.log, 1))
        reset_log.grid(column=10, row=0, rowspan=5)
        save_log.grid(column=10, row=5, rowspan=5)
    
    def save_l(self, log, state):
        with open("log.txt", "+w", encoding='utf8') as log_save:
            log_save.write(log.get("1.0",END))
        if state == 0:
            self.window.quit()
    def reset_l(self):
        self.log.delete('1.0', END)

    def read_file(self):
        with open(SOURCE_INDEX, "r", encoding='utf8') as text:
            self.data = text.read()
            line = self.data.split('\n', 1)[0]
            self.textbox.delete('1.0', END)
            self.textbox.insert(END, self.data)
            self.log.insert(END, f"$ '.txt' file inserted to Input Area [{line}]")
            return self.data

    def use_input(self):
        with open(SOURCE_INDEX, "r", encoding='utf8') as text:
            global data
            data = self.textbox.get("1.0",END)
            file_data = text.read()
            if file_data.strip() == data.strip():
                self.log.insert(END, f"$ Process Starting...")
                self.run_process()  
            else:
                self.question()
                pass
            
    def save_input(self):
        with open(SOURCE_INDEX, "+w", encoding='utf8') as text:
            global data
            data = self.textbox.get("1.0",END)
            text.write(data)
            line = data.split('\n', 1)[0]
            self.log.insert(END, f"$ Text in Input Area is written on '.txt' file [{line}]. Reset with backup to take the old text back to the '.txt' file.")
            return data

    def new_input(self, button_new):
        if self.button_state == "New Input":
            self.textbox.delete('1.0', END)
            self.textbox.insert(INSERT, "Write here.")
            self.button_state = "Read Input"
            button_new.config(text=self.button_state)
            self.log.insert(END, f"$ Waiting for new data to write on '.txt' file.")
        elif self.button_state == "Read Input":
            line = self.save_input().split('\n', 1)[0]
            self.button_state = "New Input"
            button_new.config(text=self.button_state)
            self.log.insert(END, f"$ Text in Input Area is written on '.txt' file [{line}]. Reset with backup to take the old text back to the '.txt' file.")
        else:
            print("Somehing went wrong.")

    def start_process(self, state, choice, new_window):
        new_window.destroy()
        if choice == 0:
            self.run_process()
        elif choice == 1:
            if state == 0:  
                self.run_process()
            elif state == 1:
                self.save_input()
                self.run_process()

    def run_process(self):
        process = HtmlSearch()
        url_list = process.clear_data_url
        cli(SOURCE_INDEX, HTML_INDEX, url_list)
        

    def question(self):
        new_window = Toplevel(self.window)
        new_window.title("Are you sure?")
        new_window.minsize(width=100, height=40)
        new_window.config(padx=10, pady=5)
        ques = Label(new_window, text="It seems that the texts in the '.txt' file and the input area\nare different. Which one do you want to use for the process?", font=("Arial", 10))
        ques.grid(column=0, row=0, pady=7, columnspan=2)
        checked_state = IntVar()
        checked_state.set(0)
        checkbutton = Checkbutton(new_window, text="Do you want to write the data in Input Area to the '.txt' file.\n(Only works if you choose input data.)", variable=checked_state)
        checkbutton.grid(column=0, columnspan=2, row=2, sticky=W)
        button_a = Button(new_window, text="Data in '.txt' file", command=lambda: self.start_process(0, 0, new_window))
        button_b = Button(new_window, text="Data in Input Area", command=lambda: self.start_process(checked_state.get(), 1, new_window))
        button_a.config(padx=6, pady=3)
        button_a.grid(column=0,row=1)
        button_b.config(padx=6, pady=3)
        button_b.grid(column=1,row=1)

    def reset_app(self, state):
        if state == 0:
            self.textbox.delete('1.0', END)
        elif state == 1:
            with open(SOURCE_INDEX, "+w", encoding='utf8') as text:
                text.write(self.backup.strip())
                line = self.backup.split('\n', 1)[0]
                self.log.insert(END, f"$ Backup restored to '.txt' file [{line}]")
    
    def nothing(self, current_window):
        current_window.destroy()
        
    def terminate(self, state):
        if state == 0:
            exit_window = Toplevel(self.window)
            exit_window.title("Are you sure?")
            exit_window.minsize(width=100, height=40)
            exit_window.config(padx=10, pady=13)
            ques = Label(exit_window, text="You are going to lose your backup. Do you want to continue?", font=("Arial", 10))
            ques.grid(column=0, row=0, columnspan=2, sticky=W+E)
            ques.config(pady=10,padx=5)
            yes_button = Button(exit_window, text="Continue", command=lambda: self.save_l(self.log, 0))
            yes_button.grid(column=0, row=1)
            no_button = Button(exit_window, text="Cancel", command=lambda: self.nothing(exit_window))
            no_button.grid(column=1, row=1)
        else:
            self.reset_app(state)
            self.window.quit()

start = MainWindow()
