#!/usr/bin/env python
# coding: utf-8

from typing import List
from pydantic.main import BaseModel
from pydantic import root_validator


class IkidoClassifierInput(BaseModel):
    pdf_datasheet_url: str = ''
    pdf_datasheet_text: str = ''

    @root_validator(pre=True)
    def validate_xor(cls, values):  # better name needed ;)
        if sum([bool(v) for v in values.values()]) != 1:
            raise ValueError('Either pdf_datasheet_url or pdf_datasheet_text must be set.')
        return values

class IkidoClassifierInputs(BaseModel):
    inputs: List[IkidoClassifierInput]

