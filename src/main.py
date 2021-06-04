# Import necessary libraries
# standard libraries
import json
import os
from datetime import datetime
from time import time
import csv
from tqdm import tqdm
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


def fileWriter(listOrTuple, output_fileName):
    if type(listOrTuple) == type(list()):
        # format and write to file
        with open(output_fileName,'a', newline='') as out:
            csv_out=csv.writer(out)
            for row in listOrTuple:
                try:
                    csv_out.writerow(row)
                    # can also do csv_out.writerows(data) instead of the for loop
                except Exception as e:
                    print("[WARN] In filewriter: {}".format(e))
    else:
        # format and write to file
        with open(output_fileName,'a', newline='') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(listOrTuple)


if __name__ == "__main__":
    # initialise variables:
    page_index = 1
    total_listingCount = 0

    # load user defined configurations
    base_url, target_num = load_configs(path="data\config.json")

    # initialise file and directory:
    if not os.path.exists('output'):
        os.makedirs('output')
    now = datetime.now() # current date and time
    output_fileName = "./output/output_" + now.strftime("%d-%m-%Y") + ".csv"
    csv_header = ("companyName", "company_starRating", "company_offeredRole", "company_roleLocation", "listing_jobDesc", "requested_url")
    fileWriter(listOrTuple=csv_header, output_fileName=output_fileName)

    # extract maximum number of jobs
    maxJobs, maxPages = extract_maximums(base_url)
    print("[INFO] Maximum number of jobs in range: {}, number of pages in range: {}".format(maxJobs, maxPages))
    if (target_num >= maxJobs):
        print("[ERROR] Target number larger than maximum number of jobs. Exiting program...\n")
        os._exit(0)

    formatted_url = base_url
    while total_listingCount <= target_num:
        list_returnedTuple = []

        # format links
        formatted_url = format_url(base_url, page_index)

        print("\n[INFO] Processing page index {}: {}".format(page_index, formatted_url))

        page_soup,_ = requestAndParse(formatted_url)
        listings_set, jobCount = extract_listings(page_soup)
        print("[INFO] Found {} links in page index {}".format(jobCount, page_index))

        for listing_url in tqdm(listings_set):
            # to implement cache here

            returned_tuple = extract_listing(listing_url)
            list_returnedTuple.append(returned_tuple)
            # print(returned_tuple)

        fileWriter(listOrTuple=list_returnedTuple, output_fileName=output_fileName)

        # done with page, moving onto next page
        total_listingCount = total_listingCount + jobCount
        print("[INFO] Finished processing page index {}; Total number of jobs processed: {}".format(page_index, total_listingCount))
        page_index = page_index + 1