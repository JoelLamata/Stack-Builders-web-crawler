import requests
from bs4 import BeautifulSoup
import operator


def get_news():
    url = 'https://news.ycombinator.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.select('.athing')
    subtexts = soup.select('.subtext')
    news = []

    for index in range(len(posts)):
        title = get_title(posts[index])
        points = get_points(subtexts[index])
        num_comments = get_num_comments(subtexts[index])

        news.append({'title': title, 'order': index, 'comments': num_comments, 'points': points})

    return news


def get_title(post):
    return post.select_one('.titleline').select_one('a').get_text()


def get_points(subtext):
    score = subtext.select_one('.score')
    if score is not None:
        return int(score.get_text().split()[0])
    else:
        return 0


def get_num_comments(subtext):
    anchors = subtext.select('a')
    if len(anchors) == 3:
        comments = anchors[-1].get_text()
        if comments != 'discuss':
            return int(anchors.split()[0])
    return 0


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
