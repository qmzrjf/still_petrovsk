#!/bin/bash

gunicorn -w 2 -b 0.0.0.0:8000 --chdir /srv/project/src currency_exchange.wsgi:application