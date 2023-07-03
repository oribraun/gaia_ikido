from gaiaframework.base.common.object import DS_Object
from ..artifacts.shared_artifacts import IkidoClassifierSharedArtifacts

import requests, io
import fitz
import tabula 

class IkidoPdfProcessor(DS_Object):
    def __init__(self, artifacts: IkidoClassifierSharedArtifacts=None):
        super().__init__()
        self.artifacts = artifacts
        self.cfg = self.artifacts.get('pdf_processor_cfg', {})
        self.reset()

    def __call__(self, url:str):
        return self.process_pdf(url)
 
    def reset(self):
        self.error = False
        self.url = ''
        self.error_message = ''
        self.doc = None
        self.table_of_content = []
        self.number_of_pages  = 0
        self.meta_data = {}
        self.text = ''
        self.image_list = []
        self.table_list = []

    def process_pdf(self, url:str):
        '''a) Fetch the content of the pdf
           b) Read it into an object 
           c) Process the object'''
        
        self.reset()
        self.url = url
        try:
            request = requests.get(url)
            filestream = io.BytesIO(request.content)
            with fitz.open(stream=filestream, filetype="pdf") as doc:  # open document
                self.doc = doc
                self.table_of_content = doc.get_toc()
                self.number_of_pages  = doc.page_count
                self.meta_data = doc.metadata
                self.text = chr(12).join([page.get_text().encode("utf8").decode("utf8")  for page in doc])
                self.image_list = []
                if self.cfg.get('extract_images_from_pdf', False):
                    for page in doc:
                        image_list=page.get_images()
                        for img in image_list:
                            xref = img[0] # get the XREF of the image
                            pix = fitz.Pixmap(doc, xref) # create a Pixmap
                            if pix.n - pix.alpha > 3: # CMYK: convert to RGB first
                                pix = fitz.Pixmap(fitz.csRGB, pix)
                            self.image_list.append(pix)
            if self.cfg.get('extract_tables_from_pdf', False):
                self.table_list = tabula.read_pdf(url, pages='all', multiple_tables=True, stream=True)

        except  Exception as e:
            self.error_message = f'Error Loading PDF file from : {url}'
            self.error = True
            print(self.error_message, '   ', e)

