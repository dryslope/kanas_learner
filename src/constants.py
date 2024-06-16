#!/bin/env python3
# -*- coding: utf-8 -*-

import os

INDEX_JP = 0
INDEX_EN = 1
SEPARATOR = ":"
NB_KANAS = 46
HOME = os.environ["HOME"]
LEARNER_DIR = os.environ.get("LEARNER", f"{HOME}/kanas_learner")
ALL_KANAS_DIR = f"{LEARNER_DIR}/resources"
GENERATED_DIR = f"{LEARNER_DIR}/generated"
FILE_RESULTS = f"{GENERATED_DIR}/records.metrics"