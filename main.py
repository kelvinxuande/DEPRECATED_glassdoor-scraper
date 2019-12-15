'''
Import necessary libraries
'''
import json
import os
from sys import stdout
from time import sleep
from time import time

from functions import page_html, max_num_jobs, get_listing_links, jobpage_scrape, write_to_file

'''
Script entry point. Start by loading user defined configurations
'''
with open('config.json') as config_file:
    configurations = json.load(config_file)

base_url = configurations['base_url']
target_num = int(configurations["target_num"])
run = True
page_num = 1
job_num = 0
base_html = page_html(base_url)

while run:

    if page_num == 1:
        max_num_jobs = max_num_jobs(base_html)
        max_num_jobs = int(''.join([c for c in max_num_jobs if c in '1234567890']))
        print("\nMaximum number of jobs in range: {}".format(max_num_jobs))
        if (target_num >= max_num_jobs):
            print("Error: Target number larger than maximum number of jobs. Exiting program...\n")
            os._exit(0)
    elif page_num == 2:
        base_url = base_url[:-4:]
        base_url = base_url + "_IP2.htm"
    elif page_num < 10:
        base_url = base_url[:-5:]
        base_url = base_url + '{}.htm'.format(page_num)
    elif page_num < 100:
        base_url = base_url[:-6:]
        base_url = base_url + '{}.htm'.format(page_num)
    else:   # maximum page number = 999
        base_url = base_url[:-7:]
        base_url = base_url + '{}.htm'.format(page_num)
    
    toc = time()
    base_html = page_html(base_url)
    extracted_links = get_listing_links(base_html)
    tic = time()

    print("Found {} job links in page {}: {}". format(len(extracted_links), page_num, base_url))
    print("Time taken to extract page links: {}".format(tic - toc))
    print("Starting scape and writing to csv...\n")

    i = 0
    toc = time()
    for extracted_link in extracted_links:
        scraped_html = None
        scraped_html = page_html(extracted_link)
        if scraped_html != None:
            job_num = job_num + 1
            jobpage_info = jobpage_scrape(extracted_link, scraped_html)
            write_to_file(jobpage_info)
            i = i + 1
            if (job_num >= target_num):
                run = False
                print('\n')
                print("Job done! Exiting program...")
                break
            else:
                stdout.write("\rPage scrape progress: %d/ %d" % (i, len(extracted_links)))
                stdout.flush()
                # stdout.write("\n") # move the cursor to the next line
        else:
            # print("Error detected in one link")
            continue
    tic = time()
    print('\nTime taken to scrape page: {}\n'. format(tic - toc))
    print("Total jobs scraped: {}\n".format(job_num))
    if run == True:
        print("Moving onto next page...")
    page_num = page_num + 1