# Glassdoor job scraper
Web scraping the popular job listing site "Glassdoor" with Python and BeautifulSoup.
* Intended to work without sign-in. User to provide a 'base url' to scrape from, based on desired job role and country.
* User to set a 'target job size' i.e. number of individual job listings to scrape from.
* Python script scrapes job link, role, company and job description from glassdoor results. 
* Scrapped information are returned to users in the form of an output csv.

## Collection of unstructured data
1. This script serves as a means of collecting unstructured data of job descriptions provided in job listings.
2. With some programming knowledge, one can easily modify the script to work for job listing sites with similar layouts.
3. Output data can then be analysed and visualised to generate useful insights.

## Disclosures
1. The intended audience of this repository is people with some programming experience to improve on and/ or incorporate into their own data science pipelines. 
2. Script has been tested and verified to work up to a target job size of <2000, of >10 pages of job listing links.

## Prerequisites
Core Library: [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)</br>
Please refer to requirements.txt for list of requirements.

## How it works
1. HTML parser (Beautiful Soup) extracts job listing links (to individual job listing pages) from result page(s).
2. HTML parser extracts information from individual job listing pages.
3. Loop conditions control the 'movement' from job listing page-to-page.
4. Loop conditions control the 'movement' from result page-to-page.

## Definitions
![](https://github.com/kelvinxuande/glassdoor-job-scrapper/blob/master/img/definition_%201.PNG)

![](https://github.com/kelvinxuande/glassdoor-job-scrapper/blob/master/img/definition_%202.png)

## Running tests and deployment
Original **configuration.json** file has been set to run tests.
1. **output_sample.txt** contains expected results from tests.
2. Run command to install prerequisites
   ```pip install -r requirements.txt```
3. Run command to execute script
   ```python main.py```
4. Verify that the resulting **output.txt** file is as expected.
5. Modify the **configuration.json** file as necessary for deployment.</br>
The following gif shows how a base_url can be obtained.

![](https://github.com/kelvinxuande/glassdoor-job-scrapper/blob/master/img/basehtml.gif)

## Built With

* [Python](https://www.python.org/downloads/)
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## Future work

There are plans to create a data processing pipeline to analyse and visualise to generate useful insights from extracted data in the future. Feel free to collaborate and contribute to this project, or open an issue to suggest more useful features for implementation.

## Author

[Kelvin Tan Xuan De](https://github.com/kelvinxuande)
