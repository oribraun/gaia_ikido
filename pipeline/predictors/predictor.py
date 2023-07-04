from typing import List, Any
from gaiaframework.base.common.component import DS_Component
from ..predictables.predictable import IkidoClassifierPredictable 

class IkidoClassifierPredictor(DS_Component):

    def __init__(self, artifacts=None) -> None:
        super().__init__(artifacts)
        self.component_type_classifier = self.artifacts.classifier
        self.component_type_classifier_non_datasheet_supported = self.artifacts.classifier_non_datasheet_supported
        # self.pdf_datasheet_classifier = self.artifacts.datashhet_classifier

    def execute(self, predictables: List[IkidoClassifierPredictable], **kwargs) -> List[Any]:
        
        # PDF CLASSIFIER
        for p in predictables:
            p.datasheet_valid = p.forced_pred is None
            

        # COMPONENT CLASSIFIER
        n = 300  # group size
        m = 50   # overlap size
        max_token_len_to_process = 700
        
        for p in predictables:
            # check if valid data sheet
            if p.datasheet_valid:
                tokens = p.features.text_cleaned.split()
                n_tokens = len(tokens)
                max_len = max_token_len_to_process if n_tokens>max_token_len_to_process else n_tokens
                tokens = tokens[:max_len]
                splitted = [' '.join(tokens[i:i + n]) for i in range(0, len(tokens), n - m)]
                # ret = self.component_type_classifier(splitted, top_k=None)
                ret = self.component_type_classifier_non_datasheet_supported(splitted, top_k=None)
                max_score = 0
                label = ''
                # select the top score from all the windows
                for item in ret:
                    for categ in item:
                        if max_score >= 0.99:
                            break
                        if categ['score'] > max_score:
                            label = categ['label']
                            max_score = categ['score']
                # update the predictable object
                p.category_label = label
                p.category_score = max_score
            else:
                p.category_label = 'Non Datasheet'
                p.category_score = -1
        return predictables
