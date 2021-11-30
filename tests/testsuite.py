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

if __name__ == '__main__':
    unittest.main()