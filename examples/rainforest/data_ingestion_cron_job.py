from rainforestapi_helper import send_request

params = {
 "q": "keyword",
    "from": "2024-03-01",
    "to": "2024-03-26",
    "language": "en",
    "sortBy": "publishedAt",
    "apiKey": "86839fb89b9c4286810e7d5f1cb30e54"
}

data_dir = "./examples/rainforest"

send_request(data_dir, params)
