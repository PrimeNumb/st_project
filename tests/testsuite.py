import unittest
from bs4 import BeautifulSoup


class TreeNavigationTest(unittest.TestCase):
    html_text_gabe = """
    <html>
    <head>
        <title>The test title</title>
    </head>
    <body>
        <p>This is a paragraph.</p>
        <p>This is a paragraph with hyperlinks
            <a href="https://www.wikipedia.org/">This is a hyperlink to wikipedia!</a>
            <a href="https://www.facebook.com/">This is a hyperlink to facebook!</a>
        </p>
        <div id="test_id">Find me!</div>
        <main id="main_tag">
            <img src="https://www.python.org/static/community_logos/python-logo.png" width="200px" height="130px" />
        </main>
        <a href="https://creativecommons.org/">Site goes under Creative Commons</a>
    </body>
    </html>
    """

    # Test find a single object by id
    def test_find(self):
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        div = str(soup.find(id='test_id'))
        
        self.assertEqual(div, '<div id="test_id">Find me!</div>')

    # Test find a single object with nested calls
    def test_find_nested(self):
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        img_src = soup.find(id='main_tag').find("img")['src']

        print(img_src)
        
        self.assertEqual(img_src, 'https://www.python.org/static/community_logos/python-logo.png')

    # Test find a single object but it doesn't exist one
    def test_find_empty(self):
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        header = soup.find('header')

        self.assertIsNone(header)

    # Test finding all objects of a type
    def test_find_all(self):
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        links = soup.find_all('a')
        expected_links = [
            '<a href="https://www.wikipedia.org/">This is a hyperlink to wikipedia!</a>',
            '<a href="https://www.facebook.com/">This is a hyperlink to facebook!</a>',
            '<a href="https://creativecommons.org/">Site goes under Creative Commons</a>'
        ]

        for (i, link) in enumerate(links):
            self.assertEqual(str(link), expected_links[i])

    # Test find all objects of a type but there are none
    def test_find_all_empty(self):
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        li = soup.find_all('li')

        self.assertTrue(len(li) == 0)

    # Test find parent to find an object's parent
    def test_find_parent(self):
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        img = soup.find("img")
        img_parent = img.find_parent('main').name

        self.assertEqual(img_parent, 'main')

    # Test find parent to find an object's parent - empty
    def test_find_parent_empty(self):
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        html = soup.find("html")
        html_parent = html.find_parent('html')

        self.assertIsNone(html_parent)

    # Test find all parents of an object
    def test_find_parents(self):
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        text = soup.find(string='Find me!')
        div = text.find_parents('div')

        self.assertEqual(str(div[0]), '<div id="test_id">Find me!</div>')

    # Test find all parents of an object - empty
    def test_find_parents_empty(self):
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        body = soup.find('body')
        head = body.find_parents('head')

        self.assertTrue(len(head) == 0)

    # Test find sibling of an object
    def test_find_next_sibling(self):
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        a = soup.find('a')
        sibling = a.find_next_sibling("a")

        self.assertEqual(str(sibling), '<a href="https://www.facebook.com/">This is a hyperlink to facebook!</a>')
    
    # Test find sibling of an object - empty
    def test_find_next_sibling_empty(self):
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        img = soup.find('img')
        sibling = img.find_next_sibling("img")

        self.assertIsNone(sibling)

    # Test find siblings of an object
    def test_find_next_siblings(self):
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        a = soup.find('a')
        siblings = a.find_next_siblings("a")
        expected_siblings = ['<a href="https://www.facebook.com/">This is a hyperlink to facebook!</a>']

        for (i, sibling) in enumerate(siblings):
            # Should fail if there are more than one sibling
            if i > 0:
                self.assertTrue(False)
            self.assertEqual(str(sibling), expected_siblings[i])

    # Test find siblings of an object - empty
    def test_find_next_siblings(self):
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        title = soup.find('title')
        siblings = title.find_next_siblings("meta")

        self.assertTrue(len(siblings) == 0)


if __name__ == '__main__':
    unittest.main()