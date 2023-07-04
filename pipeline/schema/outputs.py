#!/usr/bin/env python
# coding: utf-8

from pydantic.main import BaseModel


class IkidoClassifierOutputs(BaseModel):
    label: str
    score: float
    version: str = '0.1'
    forced: bool = False
    forced_reason:str = ''
    predictor_label:str = ''

