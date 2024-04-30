#!/bin/bash
echo "begin to start service.."
gunicorn --config gunicorn.py app:app