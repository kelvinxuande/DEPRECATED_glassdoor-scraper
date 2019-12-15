'''
Import necessary libraries
'''
import re
import csv
import os
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup

'''
Function to request page html from given URL
'''
def page_html(requested_url):
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
        # make request, read request object to get page html and return it.
        request_obj = Request(url = requested_url, headers = headers)
        opened_url = urlopen(request_obj)
        page_html = opened_url.read()
        opened_url.close()
        return page_html
    except Exception as e:
        # print(e)
        pass

'''
Function to acquire the maximum number of jobs (only applicable for the base/ first html)
'''
def max_num_jobs(page_html):
    page_soup = soup(page_html, "html.parser")
    max_ = page_soup.find("p", {"class": "jobsCount"})
    return(max_.get_text())

'''
Function to return a list of job page links from a given html page
'''
def get_listing_links(page_html):
    try:
        # use of dictionary to make sure that there are no duplicates
        obj_links = {}
        id_temp_dict = {}
        page_soup = soup(page_html, "html.parser")
        #grab all divs with a class of result
        results = page_soup.findAll("ul", {"class": "jlGrid hover"})
        for result in results:
            links = result.findAll('a')
            for a in links:
                formatted_link = "http://www.glassdoor.sg" + a['href']
                id_temp = formatted_link[-10:]
                if id_temp not in id_temp_dict.keys():
                    id_temp_dict[id_temp] = None
                    obj_links[formatted_link] = None
        return list(obj_links.keys())
    except Exception as e:
        # print(e)
        pass

'''
Function to return a dictionary of scrapped information from a single job page link 
'''
def jobpage_scrape(extracted_link, page_html):
    jobpage_info = {}
    page_soup = soup(page_html, "html.parser")
    try:
        jobpage_info['job_link'] = extracted_link
    except Exception as e:
        # print(e)
        jobpage_info['job_link'] = None

    try:
        job_title = page_soup.find("div", {"class": "jobViewJobTitleWrap"})
        jobpage_info['job_title'] = job_title.get_text()
    except Exception as e:
        # print(e)
        jobpage_info['job_title'] = None

    try:
        sum_col = page_soup.find("div", {"class": "summaryColumn"})
        summary_column = sum_col.get_text()
        summary_column = summary_column.replace("\xa0–\xa0", ' ')
        jobpage_info['summary_column'] = summary_column
    except Exception as e:
        # print(e)
        jobpage_info['summary_column'] = None

    try:
        j_d = page_soup.find("div", {"class": "jobDescriptionContent desc"})
        job_desc = j_d.get_text()
        pattern = '\n' + '{2,}'
        job_desc = re.sub(pattern, '\n', job_desc)
        job_desc = job_desc.replace('\n', " ")
        jobpage_info['job_description'] = job_desc
    except Exception as e:
        # print(e)
        jobpage_info['job_description'] = None

    return jobpage_info

'''
Function to write a dictionary of scrapped information onto a csv file
'''
def write_to_file(jobpage_info):
    with open('output.csv', 'a', newline='', encoding="utf-8") as f:
        try:
            writer = csv.writer(f)
            writer.writerow(jobpage_info.values())
        except Exception as e:
            # print(e)
            pass