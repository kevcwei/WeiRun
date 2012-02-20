#!/bin/sh
export PYTHONPATH=$PYTHONPATH:weirun
cd weirun && python manage.py cron
