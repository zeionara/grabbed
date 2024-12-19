#!/bin/bash

conda create -n grabbed python=3.12
conda activate grabbed

conda install python-lsp-server click
pip install pykeen rdflib python-docx
