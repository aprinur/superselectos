# Super Selectos Scraper

This program is designed to automate the process of extracting data from superselectos.com. It will scrape information such as product names, prices, brands, and product URLs.


## How Does The Code Work?

This program uses Playwright to automate the process of hovering and clicking through categories. Then, it uses the request-html library for HTML request and parsing. Continue with SQLAlchemy to insert the data into the database, followed by pandas to extract the database
table into an Excel and CSV file to your Downloads directory. Without any limitation, this script will gather every product's information listed on the site. 


## Requirements
- Python 3.9+
- Command Prompt, Windows PowerShell, Terminal, or similar tool
- SQLite database

## How to Use?
1. Download and extract the project to your device
2. After navigating to the project, create a virtual environment first to keep your global environment clean. <br>Type this code on your terminal
   <br>``` python -m venv .venv ```
   <br> .venv is the directory name, you can change it to any name you want, but usually it is named .venv
4. Then, activate the virtual environment.
   * For Windows OS (Windows PowerShell & Command Prompt)
     <br>``` .venv\Scripts\activate ```
   * For linux and mac (Terminal)
     <br>``` source myvenv/bin/activate ```
5. After activating the virtual environment, we can continue to download all the required libraries with
   <br> ``` pip install -r requirements.txt ```
6. Since this program uses Playwright, we need to install the required browser first
   <br> ``` playwright install ```
7. Finally, we can start to run the program
   <br> ``` python main.py ```

## Note
1. If there are any issue with the code, you can contact me [here](aprinur.carrd.co)
2. If you want me to create scraping program based on your needs, you can hire me on [Upwork](https://www.upwork.com/freelancers/~01b277338ca2623008)
