import unittest
from bs4 import BeautifulSoup

class SampleTestCase(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

class TreeNavigationTest(unittest.TestCase):
    html_text = """<html><head><title>The test title</title></head>
        <body>
            <p>This is a paragraph.</p>
                <p>This is a paragraph with hyperlinks
                    <a href="https://www.wikipedia.org/">This is a hyperlink to wikipedia!</a>
                    <a href="https://www.facebook.com/">This is a hyperlink to facebook!</a>
                </p>
        </body>
    """

    def test_find_strings_of_tags(self):
        soup = BeautifulSoup(self.html_text, 'html.parser')
        head, body, p, a, title = soup.head.string, soup.body.string, soup.p.string, soup.a.string, soup.title.string

        self.assertEqual(head, 'The test title')
        self.assertEqual(title, 'The test title')
        self.assertEqual(body, None) # If a tag contains more than one string element, then .string is defined to be None:
        self.assertEqual(p, 'This is a paragraph.')
        self.assertEqual(a, 'This is a hyperlink to wikipedia!')

    def test_replace_string_of_tag(self):
        soup = BeautifulSoup(self.html_text, 'html.parser')
        head = soup.head
        soup.head.string = soup.p.string

        self.assertEqual(head.string, 'This is a paragraph.')
        self.assertNotEqual(head.string, 'The test title')

    def test_body_children(self):
        soup = BeautifulSoup(self.html_text, 'html.parser')
        body = []
        for child in soup.body.children:
            body.append(child)
        
        self.assertEqual(body[1].string, 'This is a paragraph.')
        self.assertEqual(body[2].string, '\n')
        self.assertEqual(body[3].string, None) # If a tag contains more than one string element, then .string is defined to be None:
        self.assertEqual(body[4].string, '\n')

    def test_strings_for_all_body_children(self):
        soup = BeautifulSoup(self.html_text, 'html.parser')
        body = []
        for string in soup.body.stripped_strings:
            body.append(string)

        self.assertEqual(body[0], 'This is a paragraph.')
        self.assertEqual(body[1], 'This is a paragraph with hyperlinks')
        self.assertEqual(body[2], 'This is a hyperlink to wikipedia!')
        self.assertEqual(body[3], 'This is a hyperlink to facebook!')

    def test_parent_from_tag(self):
        soup = BeautifulSoup(self.html_text, 'html.parser')
        title = soup.title
        self.assertEqual(title.parent.string, 'The test title')
    
    def test_parents_from_tag(self):
        soup = BeautifulSoup(self.html_text, 'html.parser')
        a = soup.a

        parents = []
        for parent in a.parents:
            parents.append(parent.name)
        
        self.assertEqual(parents[0], 'p')
        self.assertEqual(parents[1], 'body')
        self.assertEqual(parents[2], 'html')



if __name__ == '__main__':
    unittest.main()