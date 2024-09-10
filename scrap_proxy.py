import requests

with open("checked_proxy.txt",'r') as f:
    proxies = f.read().split('\n')

# sites_to_check = ["https://www.glassdoor.co.in/index.htm",
#                   "https://www.glassdoor.co.in/Job/index.htm",
#                   "https://www.glassdoor.co.in/Reviews/index.htm",
#                   "https://www.glassdoor.co.in/Salaries/index.htm"]

sites_to_check = ["https://books.toscrape.com/",
                 "https://books.toscrape.com/catalogue/category/books/fiction_10/index.html",
                 "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"]

count = 30

for site in sites_to_check:
    try:
        print(f"Using the proxy : {proxies[count]}")
        res = requests.get(site,proxies={"http":proxies[count],"https":proxies[count]})
        print(res.status_code)
        print(res.text)
    except:
        print('failed')
    finally:
        count+=1
        count % len(proxies)