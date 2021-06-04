# Import necessary libraries
# standard libraries
import re
import csv
import os
# 3rd-party libraries
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup

from packages.common import requestAndParse


def format_url(page_index, base_url):
    if page_index == 2:
        formatted_url = base_url[:-4:] + "_IP2.htm"
    elif page_index < 10:
        formatted_url = base_url[:-5:] + '{}.htm'.format(page_index)
    elif page_index < 100:
        formatted_url = base_url[:-6:] + '{}.htm'.format(page_index)
    else:   # maximum page number = 999
        formatted_url = base_url[:-7:] + '{}.htm'.format(page_index)

    return formatted_url


# Function to acquire the maximum number of jobs, only applicable for the base/ first html
def extract_maximums(base_url):

    page_soup = requestAndParse(base_url)

    tmp_match_1 = [item for item in page_soup.find_all("p") if "data-test" in item.attrs][0]
    tmp_match_2 = [item for item in page_soup.find_all("div") if "data-test" in item.attrs][-1]
    maxJobs_raw = tmp_match_1.get_text()    # e.g. 7,764 Jobs
    maxPages_raw = tmp_match_2.get_text()   # e.g. Page 1 of 30

    try:
        assert "Jobs" in maxJobs_raw
        assert "Page" in maxPages_raw
    except Exception as e:
        print(e)
        print("[ERROR] Assumptions invalid")

    maxJobs = re.sub(r"\D", "", maxJobs_raw)
    maxPages = re.sub(r"\D", "", maxPages_raw)[1:]
    
    return(int(maxJobs), int(maxPages))


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