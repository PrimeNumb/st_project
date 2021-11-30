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

if __name__ == '__main__':
    unittest.main()