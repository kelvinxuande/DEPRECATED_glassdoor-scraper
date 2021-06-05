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


def update_url(prev_url, page_index):
    if page_index == 1:
        prev_substring = ".htm"
        new_substring = "_IP" + str(page_index) + ".htm"
    else:
        prev_substring = "_IP" + str(page_index - 1) + ".htm"
        new_substring = "_IP" + str(page_index) + ".htm"

    new_url = prev_url.replace(prev_substring, new_substring)
    return new_url


def fileWriter(listOfTuples, output_fileName):
    with open(output_fileName,'a', newline='') as out:
        csv_out=csv.writer(out)
        for row_tuple in listOfTuples:
            try:
                csv_out.writerow(row_tuple)
                # can also do csv_out.writerows(data) instead of the for loop
            except Exception as e:
                print("[WARN] In filewriter: {}".format(e))


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
    csv_header = [("companyName", "company_starRating", "company_offeredRole", "company_roleLocation", "listing_jobDesc", "requested_url")]
    fileWriter(listOfTuples=csv_header, output_fileName=output_fileName)

    # extract maximum number of jobs
    maxJobs, maxPages = extract_maximums(base_url)
    print("[INFO] Maximum number of jobs in range: {}, number of pages in range: {}".format(maxJobs, maxPages))
    if (target_num >= maxJobs):
        print("[ERROR] Target number larger than maximum number of jobs. Exiting program...\n")
        os._exit(0)

    # initialise prev_url as base_url
    prev_url = base_url

    while total_listingCount <= target_num:
        # clean up buffer
        list_returnedTuple = []

        # update url
        new_url = update_url(prev_url, page_index)

        print("\n[INFO] Processing page index {}: {}".format(page_index, new_url))

        page_soup,_ = requestAndParse(new_url)
        listings_set, jobCount = extract_listings(page_soup)
        print("[INFO] Found {} links in page index {}".format(jobCount, page_index))

        for listing_url in tqdm(listings_set):
            # to implement cache here

            returned_tuple = extract_listing(listing_url)
            list_returnedTuple.append(returned_tuple)
            # print(returned_tuple)

        fileWriter(listOfTuples=list_returnedTuple, output_fileName=output_fileName)

        # done with page, moving onto next page
        total_listingCount = total_listingCount + jobCount
        print("[INFO] Finished processing page index {}; Total number of jobs processed: {}".format(page_index, total_listingCount))
        page_index = page_index + 1
        prev_url = new_url