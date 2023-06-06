#!/usr/bin/env python
# coding: utf-8

from pydantic.main import BaseModel


class IkidoClassifierOutputs(BaseModel):
    label: str
    score: float
    version: str
