import unittest
from unittest.mock import patch, Mock
from main import *


class TestNewsScraper(unittest.TestCase):
    def setUp(self):
        self.new = News('Test Title', 1, 10, 100)
        self.news = [
            News('A more than five words title', 1, 10, 100),
            News('Les than five', 2, 10, 100),
            News('New to order by comments with more than five words', 3, 20, 50),
            News('To order by points', 3, 20, 50),
        ]

    def test_news_str(self):
        self.assertEqual(str(self.new), 'Order: 1, Title: "Test Title", Points: 100, Comments: 10')

    def test_get_title(self):
        post_html = ('<tr class="athing" id="38505211">'
                         '<td align="right" valign="top" class="title">'
                            '<span class="rank">1.</span>'
                         '</td>      '
                         '<td valign="top" class="votelinks">'
                             '<center>'
                             '<a id="up_38505211" href="vote?id=38505211&amp;how=up&amp;goto=news">'
                                 '<div class="votearrow" title="upvote"></div>'
                             '</a></center></td><td class="title">'
                             '<span class="titleline">'
                                 '<a href="https://bbycroft.net/llm" rel="noreferrer">Test Title</a>'
                                 '<span class="sitebit comhead"> '
                                    '(<a href="from?site=bbycroft.net">'
                                        '<span class="sitestr">bbycroft.net</span>'
                                    '</a>)'
                                 '</span>'
                             '</span>'
                         '</td>'
                     '</tr>')
        post = BeautifulSoup(post_html, 'html.parser')
        self.assertEqual(get_title(post), 'Test Title')

    def test_get_points(self):
        subtext_html = ('<td class="subtext">'
                            '<span class="subline">'
                                '<span class="score" id="score_38513643">100 points</span>'
                                ' by <a href="user?id=PaulHoule" class="hnuser">PaulHoule</a> '
                                '<span class="age" title="2023-12-04T04:08:22">'
                                    '<a href="item?id=38513643">6 hours ago</a>'
                                '</span> '
                                '<span id="unv_38513643"></span>'
                                ' | <a href="hide?id=38513643&amp;goto=news">hide</a>'
                                ' | <a href="item?id=38513643">10&nbsp;comments</a>'
                            '</span>'
                        '</td>')
        subtext = BeautifulSoup(subtext_html, 'html.parser')
        self.assertEqual(get_points(subtext), 100)

    def test_get_num_comments(self):
        subtext_html = ('<td class="subtext">'
                            '<span class="subline">'
                                '<span class="score" id="score_38513643">16 points</span>'
                                ' by <a href="user?id=PaulHoule" class="hnuser">PaulHoule</a> '
                                '<span class="age" title="2023-12-04T04:08:22">'
                                    '<a href="item?id=38513643">6 hours ago</a>'
                                '</span> '
                                '<span id="unv_38513643"></span>'
                                ' | <a href="hide?id=38513643&amp;goto=news">hide</a>'
                                ' | <a href="item?id=38513643">10&nbsp;comments</a>'
                            '</span>'
                        '</td>')
        subtext = BeautifulSoup(subtext_html, 'html.parser')
        self.assertEqual(get_num_comments(subtext), 10)

    def test_more_than_five_words_function(self):
        self.assertTrue(more_than_five_words_function(self.news[0]))
        self.assertFalse(more_than_five_words_function(self.news[1]))

    def test_less_than_equal_five_words_function(self):
        self.assertFalse(less_than_equal_five_words_function(self.news[0]))
        self.assertTrue(less_than_equal_five_words_function(self.news[1]))

    def test_filter_news(self):
        self.assertEqual([self.news[2], self.news[0]], filter_news(self.news, more_than_five_words_function, 'comments'))
        self.assertEqual([self.news[1], self.news[3]], filter_news(self.news, less_than_equal_five_words_function, 'points'))



if __name__ == '__main__':
    unittest.main()
