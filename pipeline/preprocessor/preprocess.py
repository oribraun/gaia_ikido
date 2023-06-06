# !/usr/bin/env python
# coding: utf-8
import io
import sys
import re
import string
import PyPDF2
import requests

from typing import List, Any

from gaiaframework.base.pipeline.preprocessor import DS_Preprocessor
from ..schema.inputs import IkidoClassifierInputs, IkidoClassifierInput
from ..schema.inputs import IkidoClassifierInput, IkidoClassifierInputs
from ..schema.outputs import IkidoClassifierOutputs
from ..artifacts.shared_artifacts import IkidoClassifierSharedArtifacts

from nltk.corpus import stopwords, words
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
# import nltk
# nltk.download('words')

##
# @file
# @brief Preprocess class, implements DS_Preprocessor base class.
class IkidoClassifierPreprocess(DS_Preprocessor):
    """! Preprocessor class implements DS_Preprocessor base class.

    This is the first stage of the pipeline and its main goal is to prepare our dataset format to the model.

    Its base class DS_Preprocessor declares phases based on UVM (Universal Verification Methodology) and by this
    gives us a structured way to work in each one of the main components by overriding and implementing those phases
    in this class.

    Important note:
    Those methods are divided into two groups, the ones that run from the __init__() and
    those that run from the execute() method, use them based on the required execution order.

    In the __init__() we have the following called:
    - build
    - config
    - config_from_json
    - connect

    In the execute(), we call the following:
    - reset
    - pre_run
    - run
    - post_run
    - evaluate
    """

    def __init__(self, artifacts: IkidoClassifierSharedArtifacts=None):
        """! IkidoClassifierPreprocess (Preprocess) initializer

        Args:
            artifacts(IkidoClassifierSharedArtifacts): Shared artifacts instance.
        """

        ##
        # @hidecallgraph @hidecallergraph
        super().__init__(artifacts)

    def normalize_input(self, **kwargs: Any) -> IkidoClassifierInputs:
        """! Converts dataset to IkidoClassifierInputs

        Args:
            **kwargs: Loaded dataset.
        Returns:
            The loaded dataset in IkidoClassifierInputs datatype.
        """
        return IkidoClassifierInputs(**kwargs)

    def config(self):
        """! Config method called from DS_Component.__init__()

        Method not implemented, ready for your implementation, see more information in class description.
        """
        pass

    def connect(self):
        """! Connect method called from DS_Component.__init__().

        Method not implemented, ready for your implementation, see more information in class description.
        """

        ##
        #@hidecallgraph @hidecallergraph

        super().connect()

    def reset(self, text: str = '', hints: List[Any] = []):
        """! Reset data members, called from DS_Component.execute() method.

        Method not implemented, ready for your implementation, see more information in class description.

        Args:
            text: str
            hints: List[Any]
        """

        ##
        # For example:
        # @code {.py}
        # def reset(self, text: str, raw_input: Any):
        #
        #     self.text = ""
        #     self.hints = raw_input.hints
        #
        # @endcode

        pass

    def get_from_regex(self):
        """! Get a predefined key from common/regex_handler.py

        Method not implemented, ready for your implementation.
        """
        ##
        # For example:
        # @code{.py}
        # from gaiaframework.base.common import RegexHandler
        #
        # def get_from_regex(self):
        #    return RegexHandler.url.findall("")
        # @endcode

        pass

    def preprocess(self, raw_input: Any):
        clean_text_results = []
        for d in raw_input.inputs:
            pdf_datasheet_url = d.pdf_datasheet_url
            pdf_datasheet_text = d.pdf_datasheet_text
            if pdf_datasheet_url:
                pdf_datasheet_text = self.extract_text_from_pdf_url(pdf_datasheet_url, self.artifacts.pdf_words)
            clean_text = self.clean_text(pdf_datasheet_text)
            clean_text_results.append(clean_text)

        """! Implement method to return a list of predictable objects in IkidoClassifierInputs datatype.

        Args:
            raw_input: Data loaded initially to run model on.

        Returns:
            raw_input: Not implemented yet.

        Raises:
            NotImplementedError
        """

        ##
        # For example, minimum return as-is:
        # @code{.py}
        # def preprocess(self, raw_input: Any):
        #     return raw_input
        # @endcode

        return clean_text_results

    def extract_text_from_pdf_url(self, pdf_url, n=None):
        # Download the PDF file from the URL
        response = requests.get(pdf_url)
        response.raise_for_status()

        # Create a file-like object from the downloaded content
        pdf_file = io.BytesIO(response.content)

        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Extract text from each page of the PDF
        extracted_text = []
        word_count = 0
        for page_num in range(len(pdf_reader.pages)):
            if n and word_count >= n:
                break
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            words = page_text.split()
            for word in words:
                extracted_text.append(word)
                word_count += 1

                if word_count >= n:
                    break

        return ' '.join(extracted_text[:n])

    def edit_line(self, text):
        text = text.lower().strip()
        text = text.replace('ca pacitance', 'capacitance')
        text = text.replace('dev ice', 'device')
        text = text.replace('temp erature', 'temperature')
        text = text.replace('vol tage', 'voltage')
        text = text.replace('vo ltage', 'voltage')
        text = text.replace('ro hs', 'rohs')
        text = text.replace('to leranc', 'toleranc')
        text = text.replace('las er', 'laser')
        text = text.replace('ha logen', 'halogen')
        text = text.replace('data she et', 'datasheet')

        return text

    def fix_whitespace_issues(self, text):
        # Get the frequency distribution of words in the English language
        freq_dist = FreqDist(words.words())

        def replace(list_of_two_words):
            if len(list_of_two_words) != 2:
                return False, list_of_two_words

            # remove panktuation
            word1 = re.sub(r'[^\w\s]', '', list_of_two_words[0])
            word2 = re.sub(r'[^\w\s]', '', list_of_two_words[1])
            combined_word = word1 + word2

            # Calculate the probability that the words are separate vs combined
            prob_separate = freq_dist[word1] * freq_dist[word2]
            prob_combined = freq_dist[combined_word]

            if (prob_combined >= prob_separate) and (prob_combined > 0):
                return True, [combined_word]
            else:
                return False, list_of_two_words

        text_list = text.split(' ')
        new_text = []
        i = 0
        while i <= (len(text_list) - 1):
            replaced, ret_element = replace(text_list[i:i + 2])
            if replaced:
                new_text += ret_element
                i += 2
            else:
                new_text += [text_list[i]]
                i += 1

        fixed_text = ' '.join(new_text)
        return fixed_text

    def remove_stopwords(self, text):
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        # converts the words in word_tokens to lower case and then checks whether
        # they are present in stop_words or not
        filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
        # with no lower case conversion
        filtered_sentence = []

        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)

        return ' '.join(filtered_sentence)

    def remove_urls(self, text):
        text = re.sub(r'http\S+', '', text, flags=re.MULTILINE)
        return text

    def remove_numbers(self, text):
        return ''.join(filter(lambda x: not x.isdigit(), text))

    def remove_token(self, token):
        if len(token) > 20 or 'www.' in token:
            return ''
        return token

    def remove_non_printable_chars(self, s):
        """Replace non-printable characters in a string."""
        return s.translate(RegexHandler.NOPRINT_TRANS_TABLE)

    def clean_text(self, text):
        text = self.fix_whitespace_issues(text)
        lines = text.replace('⚫', '•').replace('-', '•').replace('□', '•').replace('■', '•').split('•')
        lines = [self.remove_non_printable_chars(self.remove_numbers(self.remove_urls(self.edit_line(l)))) for l in lines]
        text_cleaned = ' '.join([self.remove_token(t) for t in ' '.join(lines).split()]).strip()
        return text_cleaned

class RegexHandler():
    # build a table mapping all non-printable characters to None
    NOPRINT_TRANS_TABLE = {
        i: None for i in range(0, sys.maxunicode + 1) if not chr(i).isprintable()
    }
    # NOPRINT_TRANS_TABLE = str.maketrans('', '', string.printable[:-5])
