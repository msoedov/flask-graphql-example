#!/usr/bin/env bash
exec gunicorn api:app -b 0.0.0.0:5000