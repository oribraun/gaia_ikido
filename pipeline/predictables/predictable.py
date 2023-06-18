# !/usr/bin/env python
# coding: utf-8

from gaiaframework.base.pipeline.predictables.predictable import DS_Predictable
class IkidoClassifierPredictable(DS_Predictable):
  
    def __init__(self, features) -> None:
        super().__init__()
        self.features = features

