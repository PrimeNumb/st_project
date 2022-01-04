import unittest
from unittest.case import expectedFailure
import bs4
from bs4 import BeautifulSoup

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

class TreeModificationTests(unittest.TestCase):

    test_tree = """
    <html><head><title>Title text</title></head>
    <body>
    <p class="p_class1"></p>
    <p class="p_class2"></p>
    <a href="https://www.google.com/">Google link></a>
    </body>
    """

    # insert()
    def test_insert_empty_into_invalid_index(self):
        empty_tree = BeautifulSoup("", "html.parser")
        with self.assertRaises(IndexError):
            empty_tree.insert(-1, "")

    def test_insert_empty_into_valid_index(self):
        tree = BeautifulSoup(self.test_tree, "html.parser")
        expected = BeautifulSoup(self.test_tree, "html.parser").string
        tree.insert(0, "")
        self.assertEqual(tree.string, expected)
    
    def test_insert_nonetype(self):
        tree = BeautifulSoup(self.test_tree, "html.parser")
        with self.assertRaises(ValueError):
            tree.insert(0, None)

    def test_insert_parent_element(self):
        tree = BeautifulSoup(self.test_tree, "html.parser")
        expected_contents = "abc123"
        tree.insert(0, expected_contents)
        self.assertEqual(tree.contents[0], expected_contents)
    
    def test_insert_child_element(self):
        tree = BeautifulSoup(self.test_tree, "html.parser")
        expected_contents = "abc123"
        tree.body.insert(0, expected_contents)
        self.assertEqual(tree.body.contents[0], expected_contents)

    #insert_before()
    def test_insert_before_nonetype(self):
        tree = BeautifulSoup(self.test_tree, "html.parser")
        with self.assertRaises(ValueError):
            tree.contents[0].insert_before(None)

    def test_insert_before_empty_insert(self):
        tree = BeautifulSoup(self.test_tree, "html.parser")
        expected = BeautifulSoup(self.test_tree, "html.parser")
        tree.contents[0].insert_before("")
        self.assertEqual(tree.prettify(), expected.prettify())

    def test_insert_before_parent_element(self):
        tree = BeautifulSoup(self.test_tree, "html.parser")
        expected = "<p>Test paragraph</p>"
        tree.contents[0].insert_before(expected)
        self.assertEqual(tree.contents[0].string, expected)

    def test_insert_before_child_element(self):
        tree = BeautifulSoup(self.test_tree, "html.parser")
        expected = "<p>Test paragraph</p>"
        tree.body.contents[0].insert_before(expected)
        self.assertEqual(tree.body.contents[0].string, expected)
    
    #insert_after()
    def test_insert_after_nonetype(self):
        tree = BeautifulSoup(self.test_tree, "html.parser")
        with self.assertRaises(ValueError):
            tree.contents[0].insert_after(None)

    def test_insert_after_empty_insert(self):
        tree = BeautifulSoup(self.test_tree, "html.parser")
        expected = BeautifulSoup(self.test_tree, "html.parser")
        tree.contents[0].insert_after("")
        self.assertEqual(tree.prettify(), expected.prettify()) #parses to same HTML output

    def test_insert_after_parent_element(self):
        tree = BeautifulSoup(self.test_tree, "html.parser")
        expected = "<p>Test paragraph</p>"
        tree.contents[0].insert_after(expected)
        self.assertEqual(tree.contents[1].string, expected)

    def test_insert_after_child_element(self):
        tree = BeautifulSoup(self.test_tree, "html.parser")
        expected = "<p>Test paragraph</p>"
        tree.body.contents[0].insert_after(expected)
        self.assertEqual(tree.body.contents[1].string, expected)

    #extract()
    def test_extract_empty_tree(self):
        empty_tree = BeautifulSoup("", "html.parser")
        self.assertEqual(empty_tree.extract(), empty_tree)
    
    def test_extract_populated_tree(self):
        tree = BeautifulSoup(self.test_tree, "html.parser")
        expected = BeautifulSoup('<p class="p_class1"></p>', "html.parser")
        returned = tree.body.p.extract()
        self.assertEqual(expected.contents[0], returned)

    #decompose()
    def test_decompose_empty_tree(self):
        empty_tree = BeautifulSoup("", "html.parser")
        expected = BeautifulSoup("", "html.parser")
        empty_tree.decompose()
        # behavior of a decomposed element is undefined according to the documentation,
        # hence why we check the 'decomposed' property instead
        self.assertTrue(empty_tree.decomposed)
    
    def test_decompose_child_element(self):
        tree = BeautifulSoup("<body><p>Paragraph contents</p></body>", "html.parser")
        expected = BeautifulSoup("<body></body>", "html.parser")
        tree.body.p.decompose()
        self.assertEqual(tree, expected)


    #replace_with()
    def test_replace_string_with_string(self):
        tree = BeautifulSoup('<a><b>test string</b></a>', 'html.parser')
        b = tree.b
        tree.b.contents[0].replace_with('new string')
        self.assertEqual(tree.decode(), '<a><b>new string</b></a>')
    
    def test_replace_tag(self):
        tree = BeautifulSoup('<a><b>test</b></a>', 'html.parser')
        b = tree.b
        new_tag = tree.new_tag("c")
        new_tag.string = "new string"
        tree.b.replace_with(new_tag)
        self.assertEqual(tree.decode(), '<a><c>new string</c></a>')

    def test_replace_with_itself(self):
        tree = BeautifulSoup('<a><b><c>test</c></b></a>', 'html.parser')
        c = tree.c
        tree.c.replace_with(c)
        self.assertEqual(tree.decode(), '<a><b><c>test</c></b></a>')

    def test_replace_with_parent(self):
        tree = BeautifulSoup('<a><b></b></a>', 'html.parser')
        with self.assertRaises(ValueError):
            tree.b.replace_with(tree.a)

    #wrap()
    def test_wrap(self):
        tree = BeautifulSoup('Test', 'html.parser')
        tree.string.wrap(tree.new_tag('a'))
        self.assertEqual(tree.decode(), '<a>Test</a>')
        
    def test_wrap_excisting_tag(self):
        tree = BeautifulSoup('<a></a>Test', 'html.parser')
        tree.a.next_sibling.wrap(tree.a)
        self.assertEqual(tree.decode(), '<a>Test</a>')

    def test_wrap_excisting_tag_keep_content(self):
        tree = BeautifulSoup('<a>Test</a>String', 'html.parser')
        tree.a.next_sibling.wrap(tree.a)
        self.assertEqual(tree.decode(), '<a>TestString</a>')
        
    #unwrap()
    def test_unwrap(self): 
        tree = BeautifulSoup('<a><b>Test</b></a>', 'html.parser')
        tree.b.unwrap()
        self.assertEqual(tree.b, None)
        self.assertEqual(tree.decode(), '<a>Test</a>')

    def test_unwrap_return(self): 
        tree = BeautifulSoup('<a><b><c></c></b></a>', 'html.parser')
        a = tree.a
        new_a = tree.a.unwrap()
        self.assertEqual(a, new_a)

    

if __name__ == '__main__':
    unittest.main()