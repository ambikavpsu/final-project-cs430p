# final-project-cs430p
This is a CloudShell project that utilizes multiple APIs to answer questions about places/ locations. It is coded in Python.

For security reasons, credentials are not included in this repository. To run the application, create a Google Cloud API key with the required API restrictions and set it as GOOGLE_API_KEY in your environment.
GOOGLE_API_KEY, GOOGLE_MODEL, YELP_API_KEY

Steps:
1. Set Google API key. Also set this on CloudRun
2. export GOOGLE_MODEL
3. unset GOOGLE_APPLICATION_CREDENTIALS
4. cd into server and submit a build and deploy:
   gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/mcp-server
    gcloud run deploy mcp-server \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/mcp-server \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
5. export MCP_URL
6. run python client.py

Example commands:
List all restaurants in Portland from table restaurant
List all restaurants in Portland from table restaurant with stars greater than 3
List the top restaurants in Portland
Use both the Yelp and sqlite to 1. get entries from table restaurant 2. find the number of stars for each on Yelp

