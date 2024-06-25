### QST - Sentiment Analysis on Vietnames Financial Articals

### Technologies and Libraries
* __scrapy__: crawling data from websites
* __numpy__, __pandas__: pre-processing
* __transformers__, __torch__: training models

### File System
```bash
app/                    # demo web application         
crawler/                # scrapy program for crawling data
data/                   # label and split dataset
documents               # include report and slide
env                     # virtual environment
models                  # four trained models
notebook                
-- google-colab         # notebook: training on goole colab
-- data-analysis.ipynb  # data analysis
-- demo-ai.ipynb        # demo by matplotlib
README.md               # markdown manual
```
### Environment
Set up Python virtual environment

```bash
python -m venv env
source env/bin/activate
```
***Note: using latest version of Python to import proper packages
### Dataset
Crawling by Scrapy
```bash
cd crawler/
scrapy crawl crawler/spiders/'spider_name' -o 'data_file'.json
```
*** then classify them into 3 text files: 'positive.txt', 'negative.txt', 'neutral.txt'
```bash
cd data/
python3 plain2json.py       # transform 3 text files into json files, stored in class foler
python3 split.py            # merge and split dataset inside folder class into test and train section store into section/json
```
or command:
`python3 json2csv.py       # transform json files of data/section to csv file, stored in section/csv folder` 
### Installations
Be recorded in 'documents/lib.mp4'

### Demo Web Application
Run: `python3 app.py` 

*NOTE*: Demo runs on model 'phobert' in this drive link 'https://drive.google.com/drive/folders/1SJtxzDpmzzL7LINlmP2tttKlxHzvZla7?usp=drive_link'
For quick check: 'documents/demo.mp4' (demo record) 