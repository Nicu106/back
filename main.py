from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json

# API Key and headers for TrustServista API
API_KEY = "1fd10517d980ad53ff74945bccb29da0"
HEADERS = {
    "X-TRUS-API-Key": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Cache-Control": "no-cache",
}

# Initialize FastAPI app
app = FastAPI()

# Pydantic model for request data validation
class RequestModel(BaseModel):
    contentUri: str
    language: str = "eng"


@app.post("/analyze_all/")
async def analyze_all(request: RequestModel):
    try:
        # Define API endpoints
        endpoints = {
            "summary": "https://app.trustservista.com/api/rest/v2/summary",
            "trust-level": "https://app.trustservista.com/api/rest/v2/trustlevel",
            "graph": "https://app.trustservista.com/api/rest/v2/graph",
        }

        responses = {}

        # Iterate through endpoints and make API calls
        for key, endpoint in endpoints.items():
            try:
                # Prepare the payload
                payload = {
                    "content": "EMPTY",
                    "contentUri": request.contentUri,
                    "language": request.language,
                }

                # Add a size parameter for "summary" endpoint
                if key == "summary":
                    payload["size"] = 24

                # Make the API request
                response = requests.post(endpoint, headers=HEADERS, data=json.dumps(payload))
                response.raise_for_status()

                # Process response based on endpoint
                data = response.json()
                if key == "graph":
                    # Extract titles and links for "graph"
                    responses[key] = [
                        {"title": article["title"], "url": article["url"]}
                        for node in data.get("outboundNodes", [])
                        for article in node.get("articleGraphNodes", [])
                    ]
                elif key == "trust-level":
                    # Extract trust level
                    responses[key] = {"trustLevel": data.get("trustLevel")}
                elif key == "summary":
                    # Extract summary
                    responses[key] = {"summary": data.get("summary", "No summary available")}
                else:
                    # Default: store full response
                    responses[key] = data

            except requests.exceptions.RequestException as e:
                # Handle individual endpoint errors
                responses[key] = {"error": f"Failed to fetch {key}: {str(e)}"}

        # Return aggregated responses
        return responses

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")