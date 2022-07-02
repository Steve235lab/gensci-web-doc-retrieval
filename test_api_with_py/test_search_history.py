# test_search_history.py

import requests

res = requests.get(url='http://127.0.0.1:8000/search/history/?message_type=get_history&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dWlkIjoiMCIsImV4cCI6MTY1NjY2NTc5NC44OTE2MzYxLCJzYWx0IjoiU3RldmUyMzVMYWIifQ.ACqjJW3MCddjktM2besTLW4TIYjtYOZZRtzE3Vg3F8M')
print(res.text)
