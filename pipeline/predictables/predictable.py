# !/usr/bin/env python
# coding: utf-8

from gaiaframework.base.pipeline.predictables.predictable import DS_Predictable
from gaiaframework.base.common.output_logger import OutputLogger
from ..artifacts.shared_artifacts import IkidoClassifierSharedArtifacts

class IkidoClassifierPredictable(DS_Predictable):
  
    def __init__(self, features, artifacts: IkidoClassifierSharedArtifacts=None) -> None:
        super().__init__(artifacts)
        self.logger = OutputLogger('IkidoClassifierPredictable', log_level='INFO')
        if self.artifacts.log_level:
            self.logger.set_log_level(self.artifacts.log_level)
        self.features = features

