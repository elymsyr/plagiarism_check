from tkinter import *
from matcher import Matcher
from matcher import Text as T
from googlesearch import search
import requests
import os
import html2text
import re
import subprocess
from bs4 import BeautifulSoup
#import nltk
from time import sleep
#nltk.download('stopwords')

os.chdir(os.path.dirname(os.path.abspath(__file__)))

#Checker
def checker():
    result = subprocess.run(['text-matcher', 'sources\source.txt', 'sources\html_text.txt'], stdout=subprocess.PIPE, shell = True)
    text = (result.stdout.decode('utf-8')).strip()
    return (f"{text.strip()}\n--$--\n")
def clear_text(url):
    html = (requests.get(url)).text
    soup = BeautifulSoup(html, features="html.parser")
    h = html2text.HTML2Text()
    h.ignore_links = True
    text = h.handle(soup.prettify())
    return text
def part_file(source_text):
    sentences = [x for x in re.split("[//.|//!|//?]", source_text) if x!=""]
    return sentences
def html_text():
    with open("sources\source.txt", "r", encoding='utf8') as text:
        global data
        data = text.read()
        clear_data = []
        lines = part_file(data)
        query_number = 0
        for line in lines:
            for url in search(line, lang='tr'):
                clear_data.append(clear_text(url))
                query_number += 1
                if query_number > 0:
                    break
                sleep(1)
    return clear_data
def result_write(name, text):
    with open(f"results\{name}.txt", "a", encoding="utf8") as result_file:
        result_file.write(f"{text.strip()}\n")
def control(data):
    result = []
    control_text_list = data
    for site in control_text_list:
        with open("sources\html_text.txt", "w", encoding="utf8") as html_text:
            html_text.write(site)
        result.append(matcher())
    return result                        
def results():
    return control(html_text())    
def matcher():
    with open("sources\html_text.txt", "r", encoding="utf8") as html_text:
        text_b = T(html_text.read(),'HTML')
    with open("sources\source.txt", "r", encoding='utf8') as data: 
        text_a = T(data.read(),'Source')
    myMatch = Matcher(text_a,text_b)
    myMatch.match()
    
data=""
button_state = "New Input"

def save_l(log, state):
    with open("log.txt", "+w", encoding='utf8') as log_save:
        log_save.write(log.get("1.0",END))
    if state == 0:
        window.quit()
def reset_l():
    log.delete('1.0', END)

#Log
window = Tk()
log_frame = Frame(window)
log_frame.grid(column=0, row=4)
log_frame.config(pady=2)
log = Text(log_frame, height=2, width=50)
log.grid(column=0, row=0, columnspan=8, rowspan=10)
log.config(padx=10, pady=10)
log_sb = Scrollbar(log_frame)
log.config(yscrollcommand=log_sb.set)
log_sb.config(command=log.yview)
log_sb.grid(column=9, row=0, rowspan=10,  sticky=N+S)
reset_log = Button(log_frame, text="Reset", command=reset_l)
save_log = Button(log_frame, text="Save", command=lambda: save_l(log, 1))
reset_log.grid(column=10, row=0, rowspan=5)
save_log.grid(column=10, row=5, rowspan=5)

def read_first_line(state):
    if state == 0: 
        with open("sources\source.txt", "r", encoding='utf8') as text:
            data = text.readline()
            return f"{data[0]}"
    elif state == 1:
        data = textbox.get("1.0",END)
        line = data.split('\n', 1)[0]
        return f"[{line}]"
    
def read_file():
    with open("sources\source.txt", "r", encoding='utf8') as text:
        global data
        data = text.read()
        line = data.split('\n', 1)[0]
        textbox.delete('1.0', END)
        textbox.insert(END, data)
        log.insert(END, f"$ '.txt' file inserted to Input Area [{line}]")
        return data
    
def use_input():
    with open("sources\source.txt", "r", encoding='utf8') as text:
        global data
        data = textbox.get("1.0",END)
        file_data = text.read()
        if file_data.strip() == data.strip():
            log.insert(END, f"$ Process Starting...")
            run_process()  
        else:
            question()
            pass

def save_input():
    with open("sources\source.txt", "+w", encoding='utf8') as text:
        global data
        data = textbox.get("1.0",END)
        text.write(data)
        line = data.split('\n', 1)[0]
        log.insert(END, f"$ Text in Input Area is written on '.txt' file [{line}]. Reset with backup to take the old text back to the '.txt' file.")
        return data

def new_input():
    global button_state
    global button_new
    if button_state == "New Input":
        textbox.delete('1.0', END)
        textbox.insert(INSERT, "Write here.")
        button_state = "Read Input"
        button_new.config(text=button_state)
        log.insert(END, f"$ Waiting for new data to write on '.txt' file.")
    elif button_state == "Read Input":
        line = save_input().split('\n', 1)[0]
        button_state = "New Input"
        button_new.config(text=button_state)
        log.insert(END, f"$ Text in Input Area is written on '.txt' file [{line}]. Reset with backup to take the old text back to the '.txt' file.")
    else:
        print("Somehing went wrong.")
        
def start_process(state, choice, new_window):
    new_window.destroy()
    if choice == 0:
        run_process()
    elif choice == 1:
        if state == 0:  
            run_process()
        elif state == 1:
            save_input()
            run_process()
            
def run_process():
    for result in results():
        print(result)

def question():
    new_window = Toplevel(window)
    new_window.title("Are you sure?")
    new_window.minsize(width=100, height=40)
    new_window.config(padx=10, pady=5)
    ques = Label(new_window, text="It seems that the texts in the '.txt' file and the input area\nare different. Which one do you want to use for the process?", font=("Arial", 10))
    ques.grid(column=0, row=0, pady=7, columnspan=2)
    checked_state = IntVar()
    checked_state.set(0)
    checkbutton = Checkbutton(new_window, text="Do you want to write the data in Input Area to the '.txt' file.\n(Only works if you choose input data.)", variable=checked_state)
    checkbutton.grid(column=0, columnspan=2, row=2, sticky=W)
    button_a = Button(new_window, text="Data in '.txt' file", command=lambda: start_process(0, 0, new_window))
    button_b = Button(new_window, text="Data in Input Area", command=lambda: start_process(checked_state.get(), 1, new_window))
    button_a.config(padx=6, pady=3)
    button_a.grid(column=0,row=1)
    button_b.config(padx=6, pady=3)
    button_b.grid(column=1,row=1)

def reset_app(state):
    if state == 0:
        textbox.delete('1.0', END)
    elif state == 1:
        with open("sources\source.txt", "+w", encoding='utf8') as text:
            global backup
            text.write(backup.strip())
            line = backup.split('\n', 1)[0]
            log.insert(END, f"$ Backup restored to '.txt' file [{line}]")
    checked_state.set(0)
   
def nothing(current_window):
    current_window.destroy()
     
def terminate(state):
    if state == 0:
        exit_window = Toplevel(window)
        exit_window.title("Are you sure?")
        exit_window.minsize(width=100, height=40)
        exit_window.config(padx=10, pady=13)
        ques = Label(exit_window, text="You are going to lose your backup. Do you want to continue?", font=("Arial", 10))
        ques.grid(column=0, row=0, columnspan=2, sticky=W+E)
        ques.config(pady=10,padx=5)
        yes_button = Button(exit_window, text="Continue", command=lambda: save_l(log, 0))
        yes_button.grid(column=0, row=1)
        no_button = Button(exit_window, text="Cancel", command=lambda: nothing(exit_window))
        no_button.grid(column=1, row=1)
    else:
        reset_app(state)
        window.quit()

#Config
window.title("My First GUI Program")
window.minsize(width=440, height=400)
window.config(padx=10, pady=10)
#Label
my_label = Label(text="Plagiarism Checker", font=("Arial", 24, "bold"))
my_label.grid(column=0, row=0)
#Button
button_frame = Frame()
button_frame.grid(column=0, row=1 ,sticky=W+E)
button_frame.config(pady=20)
button_run = Button(button_frame, text="Run Process", command=use_input)
button_see = Button(button_frame, text="See the '.txt' file.", command=read_file)
button_new = Button(button_frame, text=button_state, command=new_input)
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)
button_frame.columnconfigure(2, weight=1)
button_see.grid(row=0, column=0)
button_run.grid(row=0, column=1)
button_new.grid(row=0, column=2)
#Textbox
frame_text = Frame(window)
frame_text.grid(column=0, row=2)
frame_text.config(pady=5)
textbox = Text(frame_text, height=10, width=50)
textbox.grid(column=0, row=0, columnspan=9, rowspan=10)
textbox.config(padx=10, pady=10)
sb = Scrollbar(frame_text)
textbox.config(yscrollcommand=sb.set)
sb.config(command=textbox.yview)
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
reset = Button(button_frame_2, text="Reset", command=lambda: reset_app(checked_state.get()))
reset.grid(column=1, row=0, sticky=E)
exit = Button(button_frame_2, bg="#EBC2BD", text="Exit", command=lambda: terminate(checked_state.get()))
exit.grid(column=3, row=0, sticky=W)




#Program
backup = read_file()
textbox.delete('1.0', END)
log.delete('1.0', END)



window.mainloop()