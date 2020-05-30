#!/bin/bash
cd ~/development/number_six
python manage.py runscript -v3  batch_json_processor --script-args process=db_update
