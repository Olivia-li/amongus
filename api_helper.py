import requests 
  
def send_put_request(url, data)
    r = requests.put(url=url, data=data) 
    if r != 200:
        print("There has been an error")
        print(r) 
    print(r.content) 