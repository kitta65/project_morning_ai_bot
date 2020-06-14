#!/bin/bash
cd $(dirname $0)
gcloud functions deploy morning_ai_bot --entry-point morning_ai_bot --runtime python37 --trigger-http --memory 2048MB --timeout 500s --ingress-settings internal-only --allow-unauthenticated
