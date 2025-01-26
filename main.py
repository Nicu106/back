# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import requests
# import json
#
# API_KEY = "1fd10517d980ad53ff74945bccb29da0"
#
# HEADERS = {
#     "X-TRUS-API-Key": API_KEY,
#     "Content-Type": "application/json",
#     "Accept": "application/json",
#     "Cache-Control": "no-cache"
# }
#
# # FastAPI app
# app = FastAPI()
#
# # Pydantic model for request data validation
# class RequestModel(BaseModel):
#     contentUri: str
#     language: str = "eng"
#
# @app.post("/summarize/")
# async def summarize_text(request: RequestModel):
#
#     API_ENDPOINT_TRUST_LEVEL = "https://app.trustservista.com/api/rest/v2/summary"
#     try:
#         payload = {
#             "content": "EMPTY",
#             "contentUri": request.contentUri,
#             "language": request.language
#         }
#         response = requests.post(API_ENDPOINT_TRUST_LEVEL, headers=HEADERS, data=json.dumps(payload))
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#
#
# @app.post("/trust-level/")
# async def trust_level_analysis(request: RequestModel):
#
#     API_ENDPOINT_TRUST_LEVEL = "https://app.trustservista.com/api/rest/v2/trustlevel"
#
#     try:
#         # Prepare the payload for the trust level API
#         payload = {
#             "content": "EMPTY",
#             "contentUri": request.contentUri,
#             "language": request.language
#         }
#
#         # Send the request to the /rest/v2/trustlevel endpoint
#         response = requests.post(API_ENDPOINT_TRUST_LEVEL, headers=HEADERS, data=json.dumps(payload))
#         response.raise_for_status()  # Raise exception for HTTP errors
#
#         # Return the response from the TrustServista API
#         return response.json()
#
#     except requests.exceptions.RequestException as e:
#         raise HTTPException(status_code=500, detail=f"TrustServista API error: {str(e)}")
#
#
#
#
#
# @app.post("/graph/")
# async def trust_level_analysis(request: RequestModel):
#
#     API_ENDPOINT_TRUST_LEVEL = "https://app.trustservista.com/api/rest/v2/graph"
#
#     try:
#         # Prepare the payload for the trust level API
#         payload = {
#             "content": "EMPTY",
#             "contentUri": request.contentUri,
#             "language": request.language
#         }
#
#         response = requests.post(API_ENDPOINT_TRUST_LEVEL, headers=HEADERS, data=json.dumps(payload))
#         response.raise_for_status()  # Raise exception for HTTP errors
#
#         # Process the response JSON
#         response_data = response.json()
#
#         # Extract titles and links
#         filtered_data = [
#             {"title": article["title"], "url": article["url"]}
#             for node in response_data.get("outboundNodes", [])
#             for article in node.get("articleGraphNodes", [])
#         ]
#
#         return filtered_data
#
#     except requests.exceptions.RequestException as e:
#         raise HTTPException(status_code=500, detail=f"TrustServista API error: {str(e)}")


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

@app.post("/analyze_all/")
async def analyze_all(request: RequestModel):
    try:
        # Define endpoints
        endpoints = {
            "summary": "https://app.trustservista.com/api/rest/v2/summary",
            "trust-level": "https://app.trustservista.com/api/rest/v2/trustlevel",
            "graph": "https://app.trustservista.com/api/rest/v2/graph"
        }

        # Payload for all requests
        payload = {
            "content": "EMPTY",
            "contentUri": request.contentUri,
            "language": request.language
        }

        # Store responses
        responses = {}

        # Make requests to all endpoints
        for key, endpoint in endpoints.items():
            try:
                response = requests.post(endpoint, headers=HEADERS, data=json.dumps(payload))
                response.raise_for_status()

                # Process responses based on endpoint
                if key == "graph":
                    # Extract only titles and links for "graph"
                    data = response.json()
                    responses[key] = [
                        {"title": article["title"], "url": article["url"]}
                        for node in data.get("outboundNodes", [])
                        for article in node.get("articleGraphNodes", [])
                    ]
                elif key == "trust-level":
                    # Extract only "trustLevel"
                    data = response.json()
                    responses[key] = {"trustLevel": data.get("trustLevel")}
                else:
                    # Return full response for "summary"
                    responses[key] = response.json()

            except requests.exceptions.RequestException as e:
                responses[key] = {"error": f"Failed to fetch {key}: {str(e)}"}

        # Return the combined responses
        return responses

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")