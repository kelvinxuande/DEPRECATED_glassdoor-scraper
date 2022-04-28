# Import necessary libraries
# standard libraries
import re
from time import time
# 3rd-party libraries
try:
    from packages.common import requestAndParse
except ModuleNotFoundError:
    from common import requestAndParse


# extract maximum number of jobs stated, only applicable for the "base" url
def extract_maximums(base_url):
    page_soup,_ = requestAndParse(base_url)
    print(page_soup)
    tmp_match_1 = [item for item in page_soup.find_all("p") if "data-test" in item.attrs][0]
    tmp_match_2 = [item for item in page_soup.find_all("div") if "data-test" in item.attrs][-2]
    
    maxJobs_raw = tmp_match_1.get_text()    # e.g. 7,764 Jobs
    maxPages_raw = tmp_match_2.get_text()   # e.g. Page 1 of 30

    try:
        assert "jobs" in maxJobs_raw
        assert "Page" in maxPages_raw
    except Exception as e:
        print(e)
        print("[ERROR] Assumptions invalid")

    maxJobs = re.sub(r"\D", "", maxJobs_raw)
    maxPages = re.sub(r"\D", "", maxPages_raw)[1:]
    
    
    
    return(int(maxJobs), int(maxPages))


# extract listing urls
def extract_listings(page_soup):
    # this is slower but more robust:
    # get all links regardless of type and extract those that match
    listings_list = list()

    for a in page_soup.find_all('a', href=True):
        if "/partner/jobListing.htm?" in a['href']:
            # print("Found the URL:", a['href'])
            listings_list.append("www.glassdoor.com" + a['href'])

    listings_set = set(listings_list)
    jobCount = len(listings_set)

    try:
        assert jobCount != 0
    except Exception as e:
        print(e)
        print("[ERROR] Assumptions invalid")

    return listings_set, jobCount


if __name__ == "__main__":

    url = "https://www.glassdoor.sg/Job/singapore-software-engineer-jobs-SRCH_IL.0,9_IC3235921_KO10,27_IP1.htm"
    start_time = time()
    maxJobs, maxPages = extract_maximums(url)
    time_taken = time() - start_time
    print("[INFO] Maximum number of jobs in range: {}, number of pages in range: {}".format(maxJobs, maxPages))
    print("[INFO] returned in {} seconds".format(time_taken))

    url = "https://www.glassdoor.sg/Job/singapore-software-engineer-jobs-SRCH_IL.0,9_IC3235921_KO10,27_IP1.htm"
    start_time = time()
    page_soup, requested_url = requestAndParse(url)
    listings_set, jobCount = extract_listings(page_soup)
    time_taken = time() - start_time
    print(listings_set)
    print(jobCount)
    print("[INFO] returned in {} seconds".format(time_taken))