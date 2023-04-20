from googlesearch import search
import requests
import os
import html2text
import re
import subprocess
# nltk.download('stopwords')

def checker():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    result = subprocess.run(['text-matcher', 'sources\source.txt', 'sources\html_text.txt'], stdout=subprocess.PIPE, shell = True)
    return f"{result.stdout.decode('utf-8')}\nend of pl"

def log_clean():
    file = open("log.txt", 'r')
    log = file.read()
    file.close()
    file = open("logger.txt", 'a', encoding='utf8')
    file.write(f"{log}\n")
    file.close()
    os.remove("log.txt")
    
def clear_text(url):
    html = (requests.get(url)).text
    h = html2text.HTML2Text()
    h.ignore_links = True
    text = h.handle(html)
    return text

def result_folder():
    order = 0
    for item in os.listdir(os.chdir(os.path.dirname(os.path.abspath(__file__)))):
        if item.startswith('results'):
            order += 1
    if not os.path.exists(f'results{order}'):
        os.makedirs(f'results{order}')
    return order

def write_file(text, url):
    if text.endswith("end of pl"):
        i = 0
        while os.path.exists(f'result{i}.txt'):
            i += 1
        file = open(f'result{i}.txt', 'a', encoding='utf8')
        file.write(f"\n Web: {url}\n")
        file.write(text)
        file.close()
    else:
        file = open('sources\html_text.txt', 'w+', encoding='utf8')
        file.write(text)
        file.close()
        
def cleaning():
    order = 0
    clean_order = 0
    dir = os.listdir(os.chdir(os.path.dirname(os.path.abspath(__file__))))
    for item in dir:
        if item.startswith('results'):
            order += 1
    for item in dir:
        if item.startswith('result') and item.endswith('.txt'):
            os.rename(f'result{clean_order}.txt', f'results{order-1}/result{clean_order}.txt')
            clean_order += 1

def part_file(source_text):
    sentences = [x for x in re.split("[//.|//!|//?]", source_text) if x!=""]
    return sentences

def read_file():
    file = open('sources\source.txt', 'r', encoding='utf8')
    source_text = file.read()
    file.close()
    return part_file(source_text)



query = read_file()
for line in query:
    print(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    num = 0
    query_num = 2
    result_folder()
    for url in search(line, lang='tr'):
        write_file(clear_text(url), url)
        write_file(checker(), url)
        #log_clean()
        if num == query_num:
            break
        #time.sleep(3)
        num += 1
    cleaning()

#   for text matcher
#   author = {Reeve, Jonathan},
#   title = {Text-Matcher},
#   year = {2020},
#   publisher = {GitHub},
#   journal = {GitHub repository},
#   howpublished = {\url{https://github.com/JonathanReeve/text-matcher}},
#   commit = {988d9422a63165225ea136fc31427b1e57814505},
#   doi = {10.5281/zenodo.3937738}