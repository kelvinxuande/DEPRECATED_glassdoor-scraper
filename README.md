# [DEPRECATED] Glassdoor job scraper
This project web scrapes the popular job listing site "Glassdoor" for information from job listings
* Functions without any authentication e.g. user sign-ins/ API tokens and keys. Users simply modifies a config file to provide: 
   - A 'base url' to scrape from, based on desired job role and country.
   - A 'target job size' i.e. number of individual job listings to scrape from.
* Script scrapes:
   - Job link, role, company and job description from glassdoor job listing results. 
* Information collected are accessible to users in the form of an output csv.
* Script has been tested and verified to be working as expected for a job with: 
   - A target job size of < 2000 individual listings, 
   - Multiple pages > 10 pages of job listing links.

## Extracted data
![](https://github.com/kelvinxuande/glassdoor-scraper/blob/master/docs/def-3.jpg)
   
## Purpose
1. A means of collecting unstructured data of job descriptions provided in job listings.
   - Data collected can then be analysed and visualised to generate useful insights
2. With some technical knowledge and [familiarity on how it works](https://github.com/kelvinxuande/glassdoor-scraper/blob/master/docs/README.md#how-it-works), developers can:
   - Modify the script to work for other job listing sites with similar layouts.
   - Incorporate this script into their own data science pipelines and workflows

## Prerequisites

Refer to requirements.txt for a comprehensive list of requirements.

## Usage
1. [Optional] but recommended to work in a virtual environment
2. Clone repository: `git clone https://github.com/kelvinxuande/glassdoor-scraper.git`
3. Navigate to repository: `cd glassdoor-scraper/`
4. Install prerequisites: `pip install -r requirements.txt`
5. Navigate to entry-point: `cd src/`
6. Run: `python main.py`
7. Check for and verify the output csv, which can be found in the created `output/` directory
5. Modify the **config.json** file as necessary for deployment.</br>

The following gif shows how a base_url can be obtained:

![](https://github.com/kelvinxuande/glassdoor-scraper/blob/master/docs/baseURL.gif)

## Future work

There are plans to create a data processing pipeline to analyse and visualise to generate useful insights from extracted data in the future. Feel free to collaborate and contribute to this project, or open an issue to suggest more useful features for implementation.
