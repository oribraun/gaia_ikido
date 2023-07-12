#!/usr/bin/env python
# coding: utf-8

import json
from gaiaframework.base.pipeline.artifacts.shared_artifacts import DS_SharedArtifacts
from gaiaframework.base.common.output_logger import OutputLogger

# from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers import TextClassificationPipeline, pipeline
import time

class IkidoClassifierSharedArtifacts(DS_SharedArtifacts):

    def __init__(self) -> None:
        super().__init__()
        self.logger = OutputLogger('IkidoClassifierSharedArtifacts', log_level='INFO')
        if self.log_level:
            self.logger.set_log_level(self.log_level)

    def extend_load_file_type(self, file_type, path, absolute_path, name):
        if absolute_path:
            self.load_text_classification(file_type, path, absolute_path, name)
            if file_type == 'your-file-type':
                with open(absolute_path) as json_file:
                    setattr(self, name, json.load(json_file))

    def load_text_classification(self, file_type, path, absolute_path, name):
        if absolute_path:
            if file_type == 'text-classification':
                classifier = pipeline('text-classification', absolute_path)
                setattr(self, name, classifier)
