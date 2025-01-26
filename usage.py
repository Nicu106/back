# import requests
# import json
# # Define API endpoint and headers
# API_ENDPOINT_SEARCH = "https://app.trustservista.com/api/rest/v2/search"
# API_ENDPOINT_TEXT = "https://app.trustservista.com/api/rest/v2/text"
# API_KEY = "!!!YOUR API KEY!!!" # Replace with your actual API key
# HEADERS = {
# "X-TRUS-API-Key": API_KEY,
# "Content-Type": "application/json",
# "Accept": "application/json",
# "Cache-Control": "no-cache"
# }
#
# def search(query, size=20, page=1):
# data = {
# "q": query,
# "size": size,
# "page": page
# }
# response = requests.post(API_ENDPOINT_SEARCH, headers=HEADERS, data=json.dumps(data))
# if response.status_code == 200:
# return response.json()
# else:
# print(f"Error {response.status_code}: {response.text}")
# return None
# ​
# def extract_text_from_url(url):
# data = {
# "contentUri": url
# }
# response = requests.post(API_ENDPOINT_TEXT, headers=HEADERS, data=json.dumps(data))
# if response.status_code == 200:
# return response.json()
# else:
# print(f"Error {response.status_code}: {response.text}")
# return None
# ### /search endpoint examples ###
# # 1. Search by title (partial string)
# title_query = "title:*georgescu*"
# print("Search by title (partial string):")
# print(search(title_query))
# # 2. Search by author (partial string)
# author_query = "author:*pavel*"
# print("\nSearch by author (partial string):")
# print(search(author_query))
# # 3. Search by source (partial string)
# source_query = "source:*g4*"
# print("\nSearch by source (partial string):")
# print(search(source_query))
# ​
# # 4. Search by URL
# url_query = "url:\"https://www.example.com/article123\""
# print("\nSearch by URL:")
# print(search(url_query))
# ​
# # 5. Search by publish time (date only)
# publish_time_query = "publishTime:[2024-01-01 TO 2024-12-31]"
# print("\nSearch by publish time (date only):")
# print(search(publish_time_query))
# ​
# # 6. Search by sentiment
# sentiment_query = "sentiment:neg"
# print("\nSearch by sentiment:")
# print(search(sentiment_query))
# ​
# # 7. Search by trust level
# trustlevel_query = "trustlevel:[75 TO 100]"
# print("\nSearch by trust level:")
# print(search(trustlevel_query))
# ​
# # 8. Search by clickbait score
# clickbait_query = "clickbait:[0 TO 50]"
# print("\nSearch by clickbait score:")
# print(search(clickbait_query))
# ​
# # Special combined query examples
# ​
# # 9. Search by source name and published date interval
# source_date_query = "source:*G4* AND publishTime:[2024-11-27 TO 2024-11-29]"
# print("\nSearch by source name and published date interval:")
# print(search(source_date_query))
# ​
# # 10. Search by publish date interval and title containing a string fragment
# date_title_query = "publishTime:[2024-11-27 TO *] AND title:*aleger*"
# print("\nSearch by publish date interval and title containing a string fragment:")
# print(search(date_title_query))
# ​
# # 11. Search by publish date interval and author (partial name)
# date_author_query = "publishTime:[2024-11-27 TO *] AND author:*Panta*"
# print("\nSearch by publish date interval and author (partial name):")
# print(search(date_author_query))
# ​
# ### /text endpoint examples ###
# # 12. Extract text from URL example
# url_to_extract = "https://www.g4media.ro/foto-protestatarii-anti-georgescu-si-anti-rusia-din-arad-amenintati-cu-moartea-si-atacuri-homofobe.html"
# print("\nExtract text from URL:")
# print(extract_text_from_url(url_to_extract))
# ​
# # 13. Extract text from another URL example
# another_url_to_extract = "https://tass.ru/armiya-i-opk/22531193"
# print("\nExtract text from another URL:")
# print(extract_text_from_url(another_url_to_extract