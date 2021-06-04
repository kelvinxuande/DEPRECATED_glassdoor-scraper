# Import necessary libraries
# standard libraries
import json
import os
from sys import stdout
from time import time
# custom
from packages.common import requestAndParse
from packages.page import extract_maximums, extract_listings
from packages.listing import extract_listing


def load_configs(path):
    with open(path) as config_file:
        configurations = json.load(config_file)

    base_url = configurations['base_url']
    target_num = int(configurations["target_num"])

    return base_url, target_num


def format_url(base_url, page_index):

    if page_index == 2:
        formatted_url = base_url[:-4:] + "_IP2.htm"
    elif page_index < 10:
        formatted_url = base_url[:-5:] + '{}.htm'.format(page_index)
    else: # page_index < 100
        formatted_url = base_url[:-6:] + '{}.htm'.format(page_index)

    return formatted_url


if __name__ == "__main__":
    # initialise variables:
    page_index = 1
    total_listingCount = 0

    # load user defined configurations
    base_url, target_num = load_configs(path="data\config.json")

    # extract maximum number of jobs
    maxJobs, maxPages = extract_maximums(base_url)
    print("[INFO] Maximum number of jobs in range: {}, number of pages in range: {}".format(maxJobs, maxPages))
    if (target_num >= maxJobs):
        print("[ERROR] Target number larger than maximum number of jobs. Exiting program...\n")
        os._exit(0)

    formatted_url = base_url
    while total_listingCount <= target_num:
        print("[INFO] Processing page index: {}\n".format(page_index))

        # format links
        formatted_url = format_url(base_url, page_index)
        print(formatted_url)

        page_soup = requestAndParse(formatted_url)
        listings_set, jobCount = extract_listings(page_soup)
        print("[INFO] Found {} links in page: {}\n".format(jobCount, page_index))

        for listing_url in listings_set:
            returned_tuple = extract_listing(listing_url)
            print(returned_tuple)
            
        # format and write to file

        # done with page, moving onto next page
        total_listingCount = total_listingCount + jobCount
        print("\n[INFO] Finished processing page index: {}; Total number of jobs processed: {}".format(page_index, total_listingCount))
        page_index = page_index + 1