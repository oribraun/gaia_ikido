# !/usr/bin/env python
# coding: utf-8

from gaiaframework.base.pipeline.predictables.predictable import DS_Predictable

##
# @file
# @brief Predictable class, implements DS_Predictable base class.
class IkidoClassifierPredictable(DS_Predictable):
    """! IkidoClassifierPredictable class inherits from DS_Predictable.

    Predictable objects are basically a list of objects which is transferred between different components
    of the pipline.

    See the following example to understand better its usage:
    @code{.py}
    self.predictables = self.preprocess(**kwargs)
    for c in self.components:
        self.predictables = c.execute(self.predictables)
    return self.postprocess(self.predictables)
    @endcode
    """

    def __init__(self) -> None:
        """! Initializer for IkidoClassifierPredictable"""
        ##
        # @hidecallgraph @hidecallergraph
        super().__init__()

