# Import necessary libraries
# standard libraries
import time
# 3rd-party libraries
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from bs4 import BeautifulSoup as soup


# checks and corrects the scheme of the requested url
def checkURL(requested_url):
    if not urlparse(requested_url).scheme:
        requested_url = "https://" + requested_url
    return requested_url


# fetches data from requested url and parses it through beautifulsoup
def requestAndParse(requested_url):
    requested_url = checkURL(requested_url)
    try:
        # define headers to be provided for request authentication
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                        'AppleWebKit/537.11 (KHTML, like Gecko) '
                        'Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
        request_obj = Request(url = requested_url, headers = headers)
        opened_url = urlopen(request_obj)
        page_html = opened_url.read()
        opened_url.close()
        page_soup = soup(page_html, "html.parser")
        return page_soup, requested_url

    except Exception as e:
        print(e)


if __name__ == "__main__":
    
    url = "https://www.glassdoor.sg/job-listing/senior-software-engineer-java-scala-nosql-rakuten-asia-pte-JV_KO0,41_KE42,58.htm?jl=1006818844403&pos=104&ao=1110586&s=58&guid=00000179d5112735aff111df641c01be&src=GD_JOB_AD&t=SR&vt=w&ea=1&cs=1_c8e7e727&cb=1622777342179&jobListingId=1006818844403&cpc=AF8BC9077DDDE68D&jrtk=1-1f7ah29sehimi801-1f7ah29t23ogm000-80a84208d187d367&jvt=aHR0cHM6Ly9zZy5pbmRlZWQuY29tL3JjL2dkL3BuZz9hPUh5MlI4ekNxUWl3d19sM3FuaUJHaFh3RlZEYUJyUWlpeldIM2VBR1ZHTUVSeUk5VEo1ZTEzWWl5dU1sLWJWX0NIeGU4NjBDc3o0dE5sV3ZLT2pRTHFIZU5KTHpPLUhLeEFRSERmeE5CdHNUTUc1RV9FSFR2VW5FNldmWWxJQVp5dXIzNFRZZjIzLWNWNXE0NnRhSTF3V1pKeW54dHhNUkxVRlhEekI2djYwMVZGWl9vbGU5andSYjVhX3BvT0cza0JJb0NYQXo0TVZhNWdvUFY4dXY3WVJTYlMySUpZTVpyR252dEc3ZFM1aXlFQ09icHI0YVRKU2ZLUzkzMUxmLXpyQjFlZHZxbHBxbElZMXhpRksxZmdIMEhFLTJBN2pySHRZa1g0aDJCWGRxTzBCdDM0bDNzWlJDLWIxaUlCT0xnZFh6bjg4cnNjZ1N0V1BHdVhNVm5xT3A3Q0s1UEEtb0QxWDl0WFhkY19WM3Fic0dSS0tfZi1oVUZyUUlrc0o2ZV9yVHNjaFpRVkIyV2V1bmRBejNYQWVPcFZNb3lqZFlONWpLUTdVbDUxTlU5LXFVWnZIT19VWlNEWDVtdVYwR3dNbWpXVDFyaHhMM3ZkcUZqcnM4WDZuc3BYYUhYcHg1dXNUVTVJODdzQk12Q2owaXkxTmRjUmhNXzU2TF9KbXNlY0VzajNWWmFOMDQ3QmNSWU5HSGNFNmctcXUzRUV4bHJrdjQxQ3QteW02ZFo5bE45XzBfb3prR2NBVkdqQU9kaS1UNWRwVnllYzA1OU53Q3Aya2QwdHdoRU5kUnU5UzNlTUR5WmJOSFZGb0t3MnR6V1lKbTllaGxuS3hTMEdoMDhLekVBWGg4OW9BblZGR2U2ajRtMUw3T29CSVNvZWVZaC0wRHRoSTV4eUV0ODJCRERkeTV3QlREUVNTUUZ1Mkp3WUEyRE9qZk5udk5xbzQwaVZKRmF0VWFlVDc2TFl6bnIwQTB2RWRGZlNORE41QmlUaHI3VmgyUWs3bkRGaVFibmUzcWlqZE1ZYzR5TmVYZUhnUFFmOHEwc1Q2aHJrX0hPX1RwbWI5M21hd2hxOEd6a2lEaFMtUQ&ctt=1622777391568"
    start_time = time.time()
    page_soup, requested_url = requestAndParse(url)
    time_taken = time.time() - start_time
    print(page_soup)
    print("[INFO] returned in {} seconds".format(time_taken))