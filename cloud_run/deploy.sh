#!/bin/bash
cd $(dirname $0)
gcloud builds submit --tag gcr.io/$gcp_project/morning-ai
gcloud beta run deploy morning-ai --image gcr.io/$gcp_project/morning-ai --platform managed --region us-west1
