# WebScraping-CVSMinuteClinics

This is web scraping project that was done for a client on Upwork - the project posting can be found here https://www.upwork.com/jobs/Scrape-website_~0161b578d3c9ad7074

### Objective:
* Visit the [CVS website clinic directory](https://www.cvs.com/minuteclinic/clinic-locator/clinic-directory)
![cvs_mc](https://user-images.githubusercontent.com/35023657/155669328-1f1c7cfd-a516-4167-98c9-99bed34dbeb0.png)

<br>

* Visit every city in every state and scrape each clinic's address and services offered
![cvs_mc_services](https://user-images.githubusercontent.com/35023657/155670244-537dc56f-726b-4bfb-a36e-d8c2bd9b3953.png)


<br>

### Caveats:
  1) The client wanted only 2 columns in the output: the address and the services
  2) All of the services for each clinic had to be placed in the same, multi-line cell (this proved to be surprisingly difficult)
  3) Autofit the column height and width to accomodate the services column

### Output:
* Final Output
![cvs_mc_output](https://user-images.githubusercontent.com/35023657/155679900-4254079c-4f63-412f-841b-33e09415b396.png)
