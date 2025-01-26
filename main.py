from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json

API_KEY = "1fd10517d980ad53ff74945bccb29da0"

HEADERS = {
    "X-TRUS-API-Key": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Cache-Control": "no-cache"
}

# FastAPI app
app = FastAPI()

# Pydantic model for request data validation
class RequestModel(BaseModel):
    contentUri: str
    language: str = "eng"

@app.post("/summarize/")
async def summarize_text(request: RequestModel):

    API_ENDPOINT_TRUST_LEVEL = "https://app.trustservista.com/api/rest/v2/summary"
    try:
        payload = {
            "content": "EMPTY",
            "contentUri": request.contentUri,
            "language": request.language
        }
        response = requests.post(API_ENDPOINT_TRUST_LEVEL, headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/trust-level/")
async def trust_level_analysis(request: RequestModel):

    API_ENDPOINT_TRUST_LEVEL = "https://app.trustservista.com/api/rest/v2/trustlevel"

    try:
        # Prepare the payload for the trust level API
        payload = {
            "content": "EMPTY",
            "contentUri": request.contentUri,
            "language": request.language
        }

        # Send the request to the /rest/v2/trustlevel endpoint
        response = requests.post(API_ENDPOINT_TRUST_LEVEL, headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()  # Raise exception for HTTP errors

        # Return the response from the TrustServista API
        return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"TrustServista API error: {str(e)}")


@app.post("/patient-zero/")
async def trust_level_analysis(request: RequestModel):

    API_ENDPOINT_TRUST_LEVEL = "https://app.trustservista.com/api/rest/v2/p0"

    try:
        # Prepare the payload for the trust level API
        payload = {
            "content": "EMPTY",
            "contentUri": request.contentUri,
            "language": request.language
        }

        response = requests.post(API_ENDPOINT_TRUST_LEVEL, headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()  # Raise exception for HTTP errors

        return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"TrustServista API error: {str(e)}")
