import requests
from bs4 import BeautifulSoup
import operator


# Idea from https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module
def fetch_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout as timeout:
        print("Timeout Error:", timeout)
    except requests.exceptions.TooManyRedirects as too_many_redirects:
        print("Timeout Error:", too_many_redirects)
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        raise SystemExit(e)


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    posts = soup.select('.athing')
    subtexts = soup.select('.subtext')
    return posts, subtexts


def extract_news(posts, subtexts):
    news = []
    for index in range(len(posts)):  # The length is always 30.
        title = get_title(posts[index])
        points = get_points(subtexts[index])
        num_comments = get_num_comments(subtexts[index])

        news.append({'title': title, 'order': index + 1, 'comments': num_comments, 'points': points})
    return news


def get_news():
    url = 'https://news.ycombinator.com/'
    html = fetch_webpage(url)
    posts, subtexts = parse_html(html)
    news = extract_news(posts, subtexts)

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


def more_than_five_words_function(new):
    if len(new['title'].split()) > 5:
        return True
    else:
        return False


def less_than_equal_five_words_function(new):
    if len(new['title'].split()) <= 5:
        return True
    else:
        return False


if __name__ == '__main__':
    news = get_news()

    # Filter all previous entries with more than five words in the title ordered by the number of comments first.
    more_than_five_words = filter_news(news, more_than_five_words_function, 'comments')
    print("Entries with more than five words in the title ordered by comments:")
    for new in more_than_five_words:
        print(new)

    # Filter all previous entries with less than or equal to five words in the title ordered by points.
    less_than_equal_five_words = filter_news(news, less_than_equal_five_words_function, 'points')
    print("\nEntries with less than or equal to five words in the title ordered by points:")
    for new in less_than_equal_five_words:
        print(new)
