# !/usr/bin/env python
# coding: utf-8

from typing import List, Any

from gaiaframework.base.pipeline.preprocessor import DS_Preprocessor
from ..schema.inputs import IkidoClassifierInput, IkidoClassifierInputs
from ..artifacts.shared_artifacts import IkidoClassifierSharedArtifacts
from .text_cleaner import IkidoTextCleaner 
from .features_extractor import IkidoFeaturesExtractor 
from .pdf_processor import IkidoPdfProcessor
from ..predictables.predictable import IkidoClassifierPredictable 

class IkidoClassifierPreprocess(DS_Preprocessor):
    def __init__(self, artifacts: IkidoClassifierSharedArtifacts=None):
        super().__init__(artifacts)
        self.pdf_processor = IkidoPdfProcessor(artifacts)
        self.text_cleaner = IkidoTextCleaner(artifacts)
        self.features_extractor = IkidoFeaturesExtractor(artifacts)

    def normalize_input(self, **kwargs: Any) -> IkidoClassifierInputs:
        return IkidoClassifierInputs(**kwargs)

    def preprocess(self, raw_input: Any):
        '''
            In this stage we have the raw input inside self.input (same as raw_input)
            Now we need to to the following:
            a) Fetch the content of the pdf and look for tables and images
            b) Clean and normalize the input
            c) Extract features and store common items in the shared artifacts
            d) Convert the raw input into a list of predictable objects
        '''

        self.predictables = []

        for input_item in raw_input.inputs:
            # PDF Manipulation to retreive text + other pdf items (tables/images/metadata/table of content ....)
            if input_item.pdf_datasheet_url:
                url = input_item.pdf_datasheet_url
                self.pdf_processor(url)
                text = self.pdf_processor.text
            else:
                text = input_item.pdf_datasheet_text

            # Text cleanup and normalization
            self.text_cleaner(text)
            self.features_extractor(pdf_processor = self.pdf_processor, text_cleaner = self.text_cleaner)
            self.predictables.append(IkidoClassifierPredictable(self.features_extractor.features))
 
        return self.predictables