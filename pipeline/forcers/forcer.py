from gaiaframework.base.common.component import DS_Component
from ..predictables.predictable import IkidoClassifierPredictable 
from typing import List, Any

class IkidoClassifierForcer(DS_Component):
    def __init__(self, artifacts=None) -> None:
        super().__init__(artifacts)


    def execute(self, predictables: List[IkidoClassifierPredictable], **kwargs) -> List[Any]:
        n_tokens_min_thr = 100
        n_numbers_min_thr = 15

        for predictable in predictables:
            features = predictable.features
            # Rule - if n_tokens < Thr
            if features.n_tokens < n_tokens_min_thr:
                predictable.forced_pred = 'Non Datasheet'
                predictable.forced_reason = f'Number of tokens is too low ({features.n_tokens}) < ({n_tokens_min_thr})'
                continue

            # Rule - if there are no numbers
            if features.n_numbers < n_numbers_min_thr:
                predictable.forced_pred = 'Non Datasheet'
                predictable.forced_reason = f'Not enough numbers ({features.n_numbers}) < ({n_numbers_min_thr})'
                continue

            # Rule - if the n_negative_keywords > number_of_pages (usually pcn is 1-2 pages and the number of negeative keywords is more than that)
            if features.n_negative_keywords > features.number_of_pages and features.number_of_pages>0:
                predictable.forced_pred = 'Non Datasheet'
                predictable.forced_reason = f'More negative keywords than pages (NK = {features.n_negative_keywords}) > (P = {features.number_of_pages})'
                continue
            
        return predictables