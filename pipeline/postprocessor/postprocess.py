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

    def get_output_object(self, predictable):
        score = predictable.category_score
        label = predictable.category_label
        return IkidoClassifierOutputs(score=score, label=label, version=self.artifacts.version)

