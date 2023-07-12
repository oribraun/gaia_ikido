 # !/usr/bin/env python
# coding: utf-8

##
# @file
# @brief Postprocessor class, implemented DS_Postprocessor base.

from typing import List, Union
from gaiaframework.base.pipeline.predictables.predictable import DS_Predictable
from gaiaframework.base.common.output_logger import OutputLogger

from gaiaframework.base.pipeline.postprocessor import DS_Postprocessor
from ..artifacts.shared_artifacts import IkidoClassifierSharedArtifacts
from ..schema.outputs import IkidoClassifierOutputs


class IkidoClassifierPostprocess(DS_Postprocessor):

    def __init__(self, artifacts: IkidoClassifierSharedArtifacts=None) -> None:
        super().__init__(artifacts)
        self.logger = OutputLogger('IkidoClassifierPostprocess', log_level='INFO')
        if self.artifacts.log_level:
            self.logger.set_log_level(self.artifacts.log_level)
        self.cfg = self.artifacts.get('postprocessor_cfg', {})

   
    def normalize_output(self, predictables: Union[DS_Predictable, List[DS_Predictable]]) -> Union[IkidoClassifierOutputs, List[IkidoClassifierOutputs]]:

        output: IkidoClassifierOutputs = ''
        isList = isinstance(predictables, list)
        if isList:
            output: List[IkidoClassifierOutputs] = []
        if isList:
            if predictables and len(predictables):
                for item in predictables:
                    output.append(self.get_output_object(item))
        else:
            output = self.get_output_object(predictables)
        return output

    def threshold_based_modifications(self, predictable):
        threshold = self.cfg.get('threshold', 0.5)
        score = predictable.category_score
        if score != -1 and score < threshold:
            predictable.forced_pred = 'Not Sure'
            predictable.forced_reason = f'prediction score is {score} < predefined threshold ({threshold})'

    def get_output_object(self, predictable):
        self.threshold_based_modifications(predictable)

        forced = predictable.forced_pred != None
        score = predictable.category_score
        label = predictable.category_label if not forced else predictable.forced_pred
        predictor_label = predictable.category_label
        forced_reason = predictable.forced_reason
        
        return IkidoClassifierOutputs(score=score, label=label, version=self.artifacts.version, predictor_label=predictor_label, forced = forced, forced_reason=forced_reason).json()

