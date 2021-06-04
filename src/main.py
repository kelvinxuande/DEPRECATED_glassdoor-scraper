# Import necessary libraries
# standard libraries
import json
import os
from sys import stdout
from time import time
# custom functions
from functions.commonFunctions import requestAndParse
from functions.pageFunctions import extract_maximums, extract_listings


def load_configs(path):
    with open(path) as config_file:
        configurations = json.load(config_file)

    base_url = configurations['base_url']
    target_num = int(configurations["target_num"])

    return base_url, target_num


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


if __name__ == "__main__":
    # initialise variables:
    page_index = 1
    total_jobCount = 0
    # run = True

    # load user defined configurations
    base_url, target_num = load_configs(path="data\config.json")

    # extract maximum number of jobs
    maxJobs, maxPages = extract_maximums(base_url)
    print("[INFO] Maximum number of jobs in range: {}, number of pages in range: {}".format(maxJobs, maxPages))
    if (target_num >= maxJobs):
        print("[ERROR] Target number larger than maximum number of jobs. Exiting program...\n")
        os._exit(0)

    formatted_url = base_url

    while total_jobCount <= target_num:
        # format links
        formatted_url = format_url(page_index, formatted_url)

        page_soup = requestAndParse(formatted_url)

        listings_set, jobCount = extract_listings(page_soup)
        print("[INFO] Found {} links in page: {}\n".format(len(listings_set), page_index))
        print(listings_set)

        # send set to get extracted, return 2d list
        # format and write to file

        # done with page, moving onto next page
        total_jobCount = total_jobCount + jobCount
        print("\n[INFO] Total number of jobs processed: {}".format(total_jobCount))
        page_index = page_index + 1