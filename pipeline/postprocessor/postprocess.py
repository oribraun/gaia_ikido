 # !/usr/bin/env python
# coding: utf-8

##
# @file
# @brief Postprocessor class, implemented DS_Postprocessor base.

from gaiaframework.base.pipeline.predictables.predictable import DS_Predictable
from typing import List, Union

from gaiaframework.base.pipeline.postprocessor import DS_Postprocessor
from ..artifacts.shared_artifacts import IkidoClassifierSharedArtifacts
from ..schema.outputs import IkidoClassifierOutputs


class IkidoClassifierPostprocess(DS_Postprocessor):
    """IkidoClassifierPostprocess class (Postprocessor) implements DS_Postprocessor base class.
    It is the last stage of the pipeline, its main focus is to return the results in the required format.
    """

    def __init__(self, artifacts: IkidoClassifierSharedArtifacts=None) -> None:
        """! IkidoClassifierPostprocess class (Postprocessor) initializer

        Args:
            artifacts(IkidoClassifierSharedArtifacts): Shared artifacts instance.
        """

        ##
        # @hidecallgraph @hidecallergraph
        super().__init__(artifacts)

    def config(self):
        """Implement here configurations required on Preprocess stage. Overrides DS_Component.config()"""
        pass

    def normalize_output(self, predictables: Union[DS_Predictable, List[DS_Predictable]]) -> Union[IkidoClassifierOutputs, List[IkidoClassifierOutputs]]:
        """! Converts received predictable objects to IkidoClassifierOutputs datatype.

        Args:
            predictables: List[DS_Predictable] - Predictable objects, the results from the model.

        Returns:
            IkidoClassifierOutputs: List[IkidoClassifierOutputs] - Results converted to Outputs format.
        """

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
        """! Parse a single predictable item, needs to be implemented.

        Args:
            predictable: DS_Predictable - Single predictable object.

        Returns:
            IkidoClassifierOutputs: IkidoClassifierOutputs - Parsed results

        Raises:
            NotImplementedError

        """

        ##
        # Implementation example:
        # @code{.py}
        # prob = predictable[-1]
        # pred = False
        #
        # if prob > self.artifacts.threshold:
        #     pred = True
        # return IkidoClassifierOutputs(pred=pred, prob=prob, version=self.artifacts.version)
        # @endcode

        # for streaming chat
        # from gaiaframework.base.common.async_iterator import AsyncIterator
        # import json
        # results = AsyncIterator()
        # count = 0
        # final_text = ''
        # while count < 4:
        #     final_text += f"test_{count}"
        #     count += 1
        #     if count < 4:
        #         final_text += ' '
        #     results.add_item(json.dumps({"text": final_text}))
        # return results
        score = predictable['score']
        label = predictable['label']
        return IkidoClassifierOutputs(score=score, label=label, version=self.artifacts.version)

