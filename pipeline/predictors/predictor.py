from typing import List, Any
from gaiaframework.base.common.component import DS_Component

##
# @file
# @brief Predictor class, this is where the model goes.

class IkidoClassifierPredictor(DS_Component):
    """! IkidoClassifierPredictor class (Predictor) implements DS_Component base class.

    This is the second stage of the pipeline and its main goal is to pass our dataset to the model.
    Basically our model goes in this class.
    """

    def __init__(self, artifacts=None) -> None:
        """IkidoClassifierPredictor class (Postprocessor) initializer

        Args:
            artifacts: Shared artifacts instance.
        """

        ##
        # @hidecallgraph @hidecallergraph
        super().__init__(artifacts)

    def execute(self, predictables: List[Any], **kwargs) -> List[Any]:
        """! IkidoClassifierPredictor.execute (Predictor) - Run the data against the model in this method.

        Args:
            predictables:List[Any]: List of predictable objects received from Preprocess.
            **kwargs: Dictionary with additional variables, if necessary.
        Returns:
            List[DS_Predictable]: List of predictable objects.
        """

        ##
        # For example:
        # @code{.py}
        #     def execute(self, predictables: List[Any], **kwargs) -> List[Any]:
        #         features = [list(vars(p.features).values()) for p in predictables]
        #
        #         results = self.artifacts.rf_model.predict_proba(features)
        #
        #         idx = 0
        #         for p in predictables:
        #             p.prob = results[idx][-1]
        #             idx += 1
        #         return predictables
        # @endcode

        ##
        # another example:
        # @code
        #     def execute(self, predictables: List[Any], **kwargs) -> List[Any]:
        #         df = pd.DataFrame([predictables.dict()])
        #         df = self.text_data_preparation(df)
        #         data = self.encode_batch(df['text'].tolist())
        #
        #         bert_output = self.artifacts.model(data)
        #
        #         probas = list(tf.nn.softmax(bert_output.logits).numpy())
        #         return probas
        # @endcodes
        n = 300  # group size
        m = 50  # overlap size
        results = []
        for p in predictables:
            tokens = p.split()
            splitted = [' '.join(tokens[i:i + n]) for i in range(0, len(tokens), n - m)]
            ret = self.artifacts.classifier(splitted, top_k=None)
            max_score = 0
            label = ''
            best_item = None
            for item in ret:
                for categ in item:
                    if max_score >= 0.99:
                        break
                    if categ['score'] > max_score:
                        label = categ['label']
                        max_score = categ['score']
                        best_item = item
            r = {}
            r['label'] = label
            r['score'] = max_score
            results.append(r)
        return results
