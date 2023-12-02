import requests
from bs4 import BeautifulSoup
import operator

def get_news():
    url = 'https://news.ycombinator.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.select('.athing')
    metadata = soup.select('.subtext')
    news = []

    for index in range(len(posts)):
        post = posts[index]
        title = post.select_one('.titleline').select_one('a').get_text()
        points = int(metadata[index].select_one('.score').get_text().split()[0])
        comments = int(metadata[index].select('a')[-1].get_text().split()[0])

        news.append({'title': title, 'order': index, 'comments': int(comments), 'points': int(points)})

    return news

def filter_news(news, filter_func, sort_key):
    filtered_news = filter(filter_func, news)
    return sorted(filtered_news, key=operator.itemgetter(sort_key), reverse=True)

if __name__ == '__main__':
    news = get_news()

    # Filter all previous entries with more than five words in the title ordered by the number of comments first.
    more_than_five_words = filter_news(news, lambda x: len(x['title'].split()) > 5, 'comments')
    print("Entries with more than five words in the title ordered by comments:")
    for entry in more_than_five_words:
        print(entry)

    # Filter all previous entries with less than or equal to five words in the title ordered by points.
    less_than_equal_five_words = filter_news(news, lambda x: len(x['title'].split()) <= 5, 'points')
    print("\nEntries with less than or equal to five words in the title ordered by points:")
    for entry in less_than_equal_five_words:
        print(entry)