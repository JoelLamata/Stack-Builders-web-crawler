# YCombinator News Web-Scraper by Joel Lamata

This project is a news scraper for the Hacker News website. It extracts news and filters them based on the number of words in the title.

## Project Structure
The project consists of two main files:

### Main.py
This file contains the main logic of the news scraper. This is where the news are extracted from the website, filtered, and displayed on the console.
It will start by getting the news, this will fetch the https://news.ycombinator.com/ webpage, then parse it, extracting the posts and their subtexts.
After that, it will extract the title, the points and the comments from every post and subtext, creating an object News for everyone.

When all the news have been collected, the function filter_news is called, with the function for more than five words, and
the one for less or equal than five words. It filters the news by the filter given, and is sorted by the key chosen.
Then, after every filter, it prints all the news.

### Test.py
This file contains unit tests for the functions in main.py. This file was created to ensure the functionality of main.py.

The test cover, the new to string, the get title, points, and comments functions, and the two filters and filter new functions.

## Dependencies
This project depends on the following Python libraries:
````
requests
beautifulsoup4
````

## How to Run the Project
To run the project, simply run the main.py file with Python:

````commandline
python main.py
````

This will display the Hacker News on the console. The news will be displayed in two categories:

Entries with more than five words in the title ordered by comments.
Entries with five words or fewer in the title ordered by points.

## How to Run the Tests
To run the tests, run the test.py file with Python:

````commandline
python test.py
````