## Definitions
![](https://github.com/kelvinxuande/glassdoor-scraper/blob/master/docs/def-1.jpg)

![](https://github.com/kelvinxuande/glassdoor-scraper/blob/master/docs/def-2.jpg)

## How it works
1. Understand how the maximum number of jobs, number of pages and page indices relate to its corresponding result page url. 
    - Loop page indices and query for the associated result page.
3. For each result page, use HTML parser to extract all listing URLs.
4. Loop and query each listing URL for its job listing page
5. For each listing page, use HTML parser to extract desired information.
