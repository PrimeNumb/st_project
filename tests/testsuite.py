import unittest
from unittest.case import expectedFailure
import bs4
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

class AppendClearTests(unittest.TestCase):
  def test_append_empty(self):
    simple_empty_tag = "<a></a>"
    soup = BeautifulSoup(simple_empty_tag, 'html.parser')

    #Assure that the tag is empty
    self.assertEqual(soup.string, None)

    #Check if a normal string is appended as expected
    soup.a.append("Test")
    self.assertEqual(soup.a.string, "Test")

    #Reset tag
    soup = BeautifulSoup(simple_empty_tag, 'html.parser')
    #Test empty string appended
    soup.a.append("")
    self.assertEqual(soup.a.string, "")


  def test_append_non_empty(self):
    simple_tag = "<a>Test</a>"
    soup = BeautifulSoup(simple_tag, 'html.parser')
    #Check that the tag contains multiple strings if
    soup.a.append("")
    self.assertEqual(soup.a.string, None)
    expected_strings = ["Test", ""]
    for string in soup.strings:
      self.assertTrue(string in expected_strings)

    #Assure that strings are appended as the last of the tag's contents
    soup.a.append("Banana")
    self.assertEqual(soup.a.contents[-1], "Banana")
    self.assertNotEqual(soup.a.contents[0], "Banana")
    self.assertNotEqual(soup.a.contents[1], "Banana")

  def test_append_tags(self):
    #Define input data
    simple_tag1 = "<div></div>"
    simple_tag2 = "<a>Test</a>"
    simple_tag3 = "<div>Test2</div>"
    tag1 = BeautifulSoup(simple_tag1, 'html.parser')
    tag2 = BeautifulSoup(simple_tag2, 'html.parser')
    tag3 = BeautifulSoup(simple_tag3, 'html.parser')

    #Assure contetnts of <a> is empty
    self.assertEqual(tag1.div.contents, [])
    self.assertEqual(len(tag1.div.contents), 0)
    tag1.div.append(tag2)

    #Check that the tag was inserted
    self.assertEqual(str(tag1), "<div><a>Test</a></div>")
    self.assertEqual(len(tag1.div.contents), 1)
    
    #Append a second tag
    tag1.div.append(tag3)
    self.assertEqual(str(tag1), "<div><a>Test</a><div>Test2</div></div>")
    self.assertEqual(len(tag1.div.contents), 2)

  def test_clear_simple(self):
    simple_tag = "<div>Test</div>"
    soup = BeautifulSoup(simple_tag, 'html.parser')

    #Assure tag is not empty
    self.assertEqual(soup.div.contents, ["Test"])
    self.assertEqual(len(soup.div.contents), 1)

    #Check simple clear
    soup.div.clear()
    self.assertEqual(str(soup), "<div></div>")
    self.assertEqual(len(soup.div), 0)

    #Clear empty tag
    soup.div.clear()
    self.assertEqual(str(soup), "<div></div>")
    self.assertEqual(len(soup.div), 0)
    
    
  def test_clear_w_append(self):
    simple_tag = "<div><a>Test</a></div>"
    banana_tag= "<div>Banana</div>"
    soup = BeautifulSoup(simple_tag, 'html.parser')
    banana_soup = BeautifulSoup(banana_tag, 'html.parser')

    #Ensure banana div has been appended
    soup.div.append(banana_soup)
    self.assertEqual(str(soup), "<div><a>Test</a><div>Banana</div></div>")

    #Check that only the <a> tag is cleared
    soup.div.a.clear()
    self.assertEqual(str(soup.div.a), "<a></a>")
    self.assertEqual(len(soup.div.a), 0)
    #Check that the other component was unaffected
    self.assertEqual(str(soup.div.div), "<div>Banana</div>")
    self.assertEqual(len(soup.div.div), 1)
    self.assertEqual(str(soup), "<div><a></a><div>Banana</div></div>")

    #Ensure that all children are removed
    soup.div.clear() 
    self.assertEqual(str(soup), "<div></div>")
    self.assertEqual(len(soup.div), 0)

class TreeNavigationBlackboxTest(unittest.TestCase):
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
        
        self.assertEqual(body[0].string, '\n')
        self.assertEqual(body[1].string, 'This is a paragraph.')
        self.assertEqual(body[2].string, '\n')
        self.assertEqual(body[3].string, None) # If a tag contains more than one string element, then .string is defined to be None:
        self.assertEqual(body[4].string, '\n')

    def test_body_children_tag_name(self):
        soup = BeautifulSoup(self.html_text, 'html.parser')
        body = []

        for child in soup.body.children:
            body.append(child)
        
        self.assertEqual(body[0].name, None)
        self.assertEqual(body[1].name, 'p')
        self.assertEqual(body[2].name, None)
        self.assertEqual(body[3].name, 'p')
        self.assertEqual(body[4].name, None)

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

    def test_next_sibling(self):
        soup = BeautifulSoup(self.html_text, 'html.parser')
        a = soup.a

        self.assertEqual(a.string, 'This is a hyperlink to wikipedia!')
        self.assertEqual(a.next_sibling.string, '\n')
        self.assertEqual(a.next_sibling.next_sibling.string, 'This is a hyperlink to facebook!')

    
    def test_next_siblings(self):
        soup = BeautifulSoup(self.html_text, 'html.parser')
        a = soup.a

        siblings = []
        for sibling in a.next_siblings:
            siblings.append(repr(sibling))

        
        self.assertEqual(siblings[0], "'\\n'")
        self.assertEqual(siblings[1], '<a href="https://www.facebook.com/">This is a hyperlink to facebook!</a>')
        self.assertEqual(siblings[2], "'\\n'")

    def test_next_and_previous_element(self):
        soup = BeautifulSoup(self.html_text, 'html.parser')
        a = soup.a

        next = a.next_element
        previous = next.previous_element

        self.assertEqual(a, previous)

    def test_next_elements(self):
        soup = BeautifulSoup(self.html_text, 'html.parser')
        a = soup.a

        elements = []
        for element in a.next_elements:
            elements.append(repr(element))
        self.assertEqual(elements[0], "'This is a hyperlink to wikipedia!'")
        self.assertEqual(elements[1], "'\\n'")
        self.assertEqual(elements[2], '<a href="https://www.facebook.com/">This is a hyperlink to facebook!</a>')
        self.assertEqual(elements[3], "'This is a hyperlink to facebook!'")
        self.assertEqual(elements[4], "'\\n'")

if __name__ == '__main__':
    unittest.main()