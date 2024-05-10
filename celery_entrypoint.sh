#!/bin/bash
cd /app/
/opt/venv/bin/celery -A authentication worker -l INFO -E