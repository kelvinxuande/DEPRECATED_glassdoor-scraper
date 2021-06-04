# Import necessary libraries
# standard libraries
import json
import os
from time import time
from sys import stdout

from packages.common import requestAndParse


def extract_listingBanner(listing_soup):
    listing_bannerGroup_valid = False
    try:
        listing_bannerGroup = listing_soup.find("div", class_="css-ur1szg e11nt52q0")
        listing_bannerGroup_valid = True
    except:
        print("[ERROR] error occurred in function extract_listingBanner")
        companyName = "NA"
        company_starRating = "NA"
        company_offeredRole = "NA"
        company_roleLocation = "NA"

    if listing_bannerGroup_valid:

        try:
            company_starRating = listing_bannerGroup.find("span", class_="css-1pmc6te e11nt52q4").getText()
        except:
            company_starRating = "NA"

        if company_starRating != "NA":
            try:
                companyName = listing_bannerGroup.find("div", class_="css-16nw49e e11nt52q1").getText().replace(company_starRating,'')
            except:
                companyName = "NA"
            # company_starRating.replace("★", "")
            company_starRating = company_starRating[:-1]
        else:
            try:
                companyName = listing_bannerGroup.find("div", class_="css-16nw49e e11nt52q1").getText()
            except:
                companyName = "NA"

        try:
            company_offeredRole = listing_bannerGroup.find("div", class_="css-17x2pwl e11nt52q6").getText()
        except:
            company_offeredRole = "NA"

        try:
            company_roleLocation = listing_bannerGroup.find("div", class_="css-1v5elnn e11nt52q2").getText()
        except:
            company_roleLocation = "NA"

    return companyName, company_starRating, company_offeredRole, company_roleLocation


def extract_listingDesc(listing_soup):
    extract_listingDesc_tmpList = []
    try:
        listing_jobDesc_raw = listing_soup.find("div", id="JobDescriptionContainer")
        jobDesc_items = listing_jobDesc_raw.findAll('li')
        for jobDesc_item in jobDesc_items:
            extract_listingDesc_tmpList.append(jobDesc_item.text)

        listing_jobDesc = " ".join(extract_listingDesc_tmpList)
    except:
        print("[ERROR] error occurred in function extract_listingDesc")
        listing_jobDesc = "NA"

    return listing_jobDesc


def extract_listing(url):
    listing_soup, requested_url = requestAndParse(url)
    companyName, company_starRating, company_offeredRole, company_roleLocation = extract_listingBanner(listing_soup)
    listing_jobDesc = extract_listingDesc(listing_soup)

    return (companyName, company_starRating, company_offeredRole, company_roleLocation, listing_jobDesc, requested_url)


if __name__ == "__main__":
    # feed in a single test url
    url = "https://www.glassdoor.sg/job-listing/senior-software-engineer-java-scala-nosql-rakuten-asia-pte-JV_KO0,41_KE42,58.htm?jl=1006818844403&pos=104&ao=1110586&s=58&guid=00000179d5112735aff111df641c01be&src=GD_JOB_AD&t=SR&vt=w&ea=1&cs=1_c8e7e727&cb=1622777342179&jobListingId=1006818844403&cpc=AF8BC9077DDDE68D&jrtk=1-1f7ah29sehimi801-1f7ah29t23ogm000-80a84208d187d367&jvt=aHR0cHM6Ly9zZy5pbmRlZWQuY29tL3JjL2dkL3BuZz9hPUh5MlI4ekNxUWl3d19sM3FuaUJHaFh3RlZEYUJyUWlpeldIM2VBR1ZHTUVSeUk5VEo1ZTEzWWl5dU1sLWJWX0NIeGU4NjBDc3o0dE5sV3ZLT2pRTHFIZU5KTHpPLUhLeEFRSERmeE5CdHNUTUc1RV9FSFR2VW5FNldmWWxJQVp5dXIzNFRZZjIzLWNWNXE0NnRhSTF3V1pKeW54dHhNUkxVRlhEekI2djYwMVZGWl9vbGU5andSYjVhX3BvT0cza0JJb0NYQXo0TVZhNWdvUFY4dXY3WVJTYlMySUpZTVpyR252dEc3ZFM1aXlFQ09icHI0YVRKU2ZLUzkzMUxmLXpyQjFlZHZxbHBxbElZMXhpRksxZmdIMEhFLTJBN2pySHRZa1g0aDJCWGRxTzBCdDM0bDNzWlJDLWIxaUlCT0xnZFh6bjg4cnNjZ1N0V1BHdVhNVm5xT3A3Q0s1UEEtb0QxWDl0WFhkY19WM3Fic0dSS0tfZi1oVUZyUUlrc0o2ZV9yVHNjaFpRVkIyV2V1bmRBejNYQWVPcFZNb3lqZFlONWpLUTdVbDUxTlU5LXFVWnZIT19VWlNEWDVtdVYwR3dNbWpXVDFyaHhMM3ZkcUZqcnM4WDZuc3BYYUhYcHg1dXNUVTVJODdzQk12Q2owaXkxTmRjUmhNXzU2TF9KbXNlY0VzajNWWmFOMDQ3QmNSWU5HSGNFNmctcXUzRUV4bHJrdjQxQ3QteW02ZFo5bE45XzBfb3prR2NBVkdqQU9kaS1UNWRwVnllYzA1OU53Q3Aya2QwdHdoRU5kUnU5UzNlTUR5WmJOSFZGb0t3MnR6V1lKbTllaGxuS3hTMEdoMDhLekVBWGg4OW9BblZGR2U2ajRtMUw3T29CSVNvZWVZaC0wRHRoSTV4eUV0ODJCRERkeTV3QlREUVNTUUZ1Mkp3WUEyRE9qZk5udk5xbzQwaVZKRmF0VWFlVDc2TFl6bnIwQTB2RWRGZlNORE41QmlUaHI3VmgyUWs3bkRGaVFibmUzcWlqZE1ZYzR5TmVYZUhnUFFmOHEwc1Q2aHJrX0hPX1RwbWI5M21hd2hxOEd6a2lEaFMtUQ&ctt=1622777391568"
    start_time = time()
    returned_tuple = extract_listing(url)
    time_taken = time() - start_time
    print(returned_tuple)
    print("[INFO] listing extracted in {} seconds".format(time_taken))