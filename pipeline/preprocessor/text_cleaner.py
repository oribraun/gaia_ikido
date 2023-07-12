
from gaiaframework.base.common.object import DS_Object
from gaiaframework.base.common.regex_handler import RegexHandler
import re

from ..artifacts.shared_artifacts import IkidoClassifierSharedArtifacts

class IkidoTextCleaner(DS_Object):
    def __init__(self, artifacts: IkidoClassifierSharedArtifacts=None):
        super().__init__()
        self.artifacts = artifacts
        self.stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

        self.reset()

    def __call__(self,text:str):
        return self.clean_text(text)
    
    def reset(self):
        self.raw_text = ''
        self.tokens = []
        self.lines = []
        self.numbers = []
        self.urls = []
        self.text_cleaned = ''
 
    def remove_numbers(self, text):
        return  '' .join((z for z in text if not z.isdigit()))
        # return ''.join(filter(lambda x: not x.isdigit(), text))

    def remove_token(self, token):
        if len(token) > 20 or 'www.' in token or token in self.urls:
            return ''
        return token.replace('�', ' ')

    def remove_stopwords(self, text):
        tokens = text.split()
        filtered_sentence = [w for w in tokens if not w.lower() in self.stopwords]
        return ' '.join(filtered_sentence)
    
    def edit_line(self, text):
        text = text.replace('ca pacitance', 'capacitance')
        text = text.replace('dev ice', 'device')
        text = text.replace('temp erature', 'temperature')
        text = text.replace('vol tage', 'voltage')
        text = text.replace('vo ltage', 'voltage')
        text = text.replace('ro hs', 'rohs')
        text = text.replace('to leranc', 'toleranc')
        text = text.replace('las er', 'laser')
        text = text.replace('ha logen', 'halogen')
        text = text.replace('data she et', 'datasheet')

        return text

    def clean_text(self,text:str=''):
        self.reset()
        self.urls = self.find_urls(text, unique=True)
        self.raw_text =  RegexHandler.remove_non_printable_chars(text)
        self.tokens = self.raw_text.split()
        self.lines = text.split('\n')
        self.lines_normalized = []
        self.numbers = RegexHandler.get_numbers(self.raw_text)
        for line in self.lines:
            line = self.edit_line(line.lower().strip())
            line = ' '.join(line.replace('⚫', '•').replace('-', '•').replace('□', '•').replace('■', '•').split('•'))
            line = self.remove_numbers(line)
            line = ' '.join([self.remove_token(t) for t in line.split()]).strip()
            line = self.remove_stopwords(line)
            if line.strip():
                self.lines_normalized.append(line)
              
        self.text_cleaned = '\n'.join(self.lines_normalized)

    def find_urls(self, text, unique=False):

        url_pattern = r"(?i)\b(?:https?://|www\.)?\S+\.(?:com|org|uk|net|gov|edu|mil|io|info|biz|co|xyz|tv|me|name|us|ca|eu|au|asia|local)\b"
        re_url = re.compile(url_pattern)
        urls = re_url.findall(text)
        urls = [url for url in urls if url[0] != '']
        if unique:
            urls = list(sorted(set(urls)))
        return urls
