import json
import re
# import string
from flask import Flask, render_template, request
# from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, AutoModel

# import torchtext
# from torchtext.models import RobertaClassificationHead, XLMR_BASE_ENCODER
import torch
# from torch.nn import functional as f
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
# from pyvi import ViTokenizer
# from collections import Counter
from nltk.stem import WordNetLemmatizer

app = Flask(__name__, template_folder='template')

DEVICE = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
label_map = {
    0: 'positive',
    1: 'negative',
    2: 'neutral'
}

def articleCrawler(url):
    if 'vneconomy.vn' in url:
        div_class = 'detail__content'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find("div", class_=div_class) 
        if content_div:
            content = content_div.find_all('p')
            content_texts = ' '.join([c.get_text() for c in content])
            return content_texts
        
    elif 'vnexpress.net' in url:
        div_class = 'fck_detail'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find("article", class_=div_class) 
        if content_div:
            content = content_div.find_all('p')
            content_texts = ' '.join([c.get_text() for c in content])
            return content_texts
        
    elif 'cafef.vn' in url:
        div_class = 'contentdetail'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find("div", class_=div_class) 
        if content_div:
            content = content_div.find_all('p')
            content_texts = ' '.join([c.get_text() for c in content])
            return content_texts
        
    else:
        return
    
def get_stopwords_list(stop_file_path):
    """load stop words """

    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return list(frozenset(stop_set))
    
stopwords_path = '/home/bxs/QST/data/vietnamese_stopwords.txt'
sw = get_stopwords_list(stopwords_path)
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z?.!,¿0-9]+", " ", text)
    punctuations = '@#!?+&*[]-%.:/();$=><|{}^,_' + "'`"
    for p in punctuations:
        text = text.replace(p,'')
    text = [word.lower() for word in text.split() if word.lower() not in sw]
    text = [lemmatizer.lemmatize(word) for word in text]
    text = " ".join(text)
    return text

def prepare_model():
    model = AutoModelForSequenceClassification.from_pretrained('/home/bxs/QST/models/phobert')
    return model

def prepare_text_transform():
    tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")
    return tokenizer

def predict(sentence, model, tokenizer, label_map):
    inp = tokenizer(sentence, padding='max_length', max_length=128, truncation=True, return_tensors="pt")
    out = model(**inp)
    probabilities = torch.softmax(out.logits, dim=1).squeeze().detach().cpu().numpy()
    return probabilities

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def display():
    input_text = request.form['input-text']
    
    model = prepare_model()
    tokenizer = prepare_text_transform()
    
    probs = list(predict(input_text, model, tokenizer, label_map))
    
        
    return render_template('index.html', 
                           input_text=input_text, 
                           probs=probs,
                           dump_label_map=json.dumps(label_map),
                           label_map=label_map
                           )

@app.route('/predictUrl', methods=['POST'])
def show():
    input_url = request.form['input-url']
    
    model = prepare_model()
    tokenizer = prepare_text_transform()
    
    probs = list(predict(articleCrawler(input_url), model, tokenizer, label_map))
    return render_template('index.html', 
                           input_url=input_url, 
                           result_content=articleCrawler(input_url), 
                           probs=probs,
                           dump_label_map=json.dumps(label_map),
                           label_map=label_map
                           )

if __name__ == '__main__':
    app.run(debug=True)