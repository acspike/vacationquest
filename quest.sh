#!/bin/bash
python bootstrap.py
source venv/bin/activate
python quest.py init provision
/bin/bash --rcfile venv/bin/activate

