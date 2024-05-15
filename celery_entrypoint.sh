#!/bin/bash
cd /app/
/opt/venv/bin/celery -A business worker -l INFO -E