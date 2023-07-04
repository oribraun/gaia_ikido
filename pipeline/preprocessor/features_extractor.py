

from gaiaframework.base.common.object import DS_Object
from ..artifacts.shared_artifacts import IkidoClassifierSharedArtifacts
from .text_cleaner import IkidoTextCleaner 
from .pdf_processor import IkidoPdfProcessor
import types

class IkidoFeaturesExtractor(DS_Object):
    def __init__(self, artifacts: IkidoClassifierSharedArtifacts=None):
        super().__init__()
        self.artifacts = artifacts
        self.reset()

    def reset(self):
        f = types.SimpleNamespace()
        f.pdf_url = ''
        f.table_of_content = []
        f.number_of_pages  = -1
        f.meta_data = {}
        f.image_list = []
        f.table_list = []
        f.n_images = 0
        f.n_tables = 0
        f.raw_text = ''
        f.text_cleaned = ''
        f.tokens = []
        f.lines =[]
        f.lines_normalized = []
        f.n_lines = 0
        f.n_lines_normalized = 0
        f.n_tokens = 0
        f.urls = []
        f.n_urls = 0
        f.numbers = []
        f.n_numbers = 0
        f.keywords_counts_dict = {}
        f.keywords = []
        f.n_keywords = 0
        f.negative_keywords_counts_dict = {}
        f.negative_keywords = []
        f.n_negative_keywords = 0
 
        self.features = f

    
    def __call__(self, pdf_processor:IkidoPdfProcessor = None, text_cleaner:IkidoTextCleaner = None):
        return self.extract_features(pdf_processor, text_cleaner)
    
    def extract_keywords_information(self, keywords_dict, raw_text):
        all_keywords = []
        for key, values in keywords_dict.items():
            if type(values)==list:
                all_keywords+=values
        all_keywords = set(all_keywords)
        keywords_counts = {}
        sum_counts = 0
            
        for keyword in all_keywords:
            counts = raw_text.lower().count(keyword.lower())
            if counts:
                keywords_counts[keyword] = counts
                sum_counts+=counts
        return keywords_counts, list(keywords_counts.keys()), sum_counts
    
    def extract_features(self, pdf_processor:IkidoPdfProcessor = None, text_cleaner:IkidoTextCleaner = None):
        self.reset()
        f = self.features
        if pdf_processor:
            f.pdf_url = pdf_processor.url
            f.table_of_content = pdf_processor.table_of_content
            f.number_of_pages  = pdf_processor.number_of_pages
            f.meta_data = pdf_processor.meta_data
            f.image_list = pdf_processor.image_list
            f.table_list = pdf_processor.table_list
            f.n_images = len(f.image_list)
            f.n_tables = len(f.table_list)
        if text_cleaner:
            f.raw_text = text_cleaner.raw_text
            f.tokens = text_cleaner.tokens
            f.lines = text_cleaner.lines
            f.lines_normalized = text_cleaner.lines_normalized
            f.n_lines = len(f.lines)
            f.n_lines_normalized = len(f.lines_normalized)
            f.n_tokens = len(f.tokens)
            f.text_cleaned = text_cleaner.text_cleaned
            f.urls = text_cleaner.urls
            f.numbers = text_cleaner.numbers
            f.n_numbers = len(f.numbers)
            f.n_urls  = len(f.urls)
        
        keywords_dict        = self.artifacts.get('class_keywords',{})
        negative_tokens_dict = self.artifacts.get('negative_tokens',{})

        if keywords_dict:
            f.keywords_counts_dict, f.keywords, f.n_keywords = self.extract_keywords_information(keywords_dict,f.raw_text)
            
        if negative_tokens_dict:
            f.negative_keywords_counts_dict, f.negative_keywords, f.n_negative_keywords = self.extract_keywords_information(negative_tokens_dict,f.raw_text)