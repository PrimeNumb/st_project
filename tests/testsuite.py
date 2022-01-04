import unittest
from unittest.case import expectedFailure
import bs4
from bs4 import BeautifulSoup, diagnose, SoupStrainer

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

  # Test clear simple with decompose ADDITION FOR COVERAGE
  def test_clear_simple_with_decompose_without_tag(self):
    simple_tag = "<div>Test</div>"
    soup = BeautifulSoup(simple_tag, 'html.parser')

    #Assure tag is not empty
    self.assertEqual(soup.div.contents, ["Test"])
    self.assertEqual(len(soup.div.contents), 1)

    #Check simple clear
    soup.div.clear(decompose=True)
    self.assertEqual(str(soup), "<div></div>")
    self.assertEqual(len(soup.div), 0)

    #Clear empty tag
    soup.div.clear(decompose=True)
    self.assertEqual(str(soup), "<div></div>")
    self.assertEqual(len(soup.div), 0)

  # Test clear simple with decompose ADDITION FOR COVERAGE
  def test_clear_simple_with_decompose_with_tag(self):
    simple_tag = "<div><h1>Test</h1></div>"
    soup = BeautifulSoup(simple_tag, 'html.parser')

    #Assure tag is not empty
    self.assertEqual(soup.div.h1.contents, ["Test"])
    self.assertEqual(len(soup.div.h1.contents), 1)

    #Check simple clear
    soup.div.clear(decompose=True)
    self.assertEqual(str(soup), "<div></div>")
    self.assertEqual(len(soup.div), 0)

    #Clear empty tag
    soup.div.clear(decompose=True)
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


class BsoupFunctionsBlackboxTest(unittest.TestCase):

    def test_smooth_basic(self):
        soup = BeautifulSoup('<p>A paragraph!</p>', 'html.parser')
        soup.p.append('Another paragraph')
        self.assertEqual(soup.p.contents[0], 'A paragraph!')
        self.assertEqual(soup.p.contents[1], 'Another paragraph')

        soup.p.smooth()
        self.assertEqual(soup.p.contents[0], 'A paragraph!Another paragraph')
    
    def test_smooth_one_element(self):
        soup = BeautifulSoup('<h1>Useless heading 1</h1>', 'html.parser')
        soup.h1.smooth()
        self.assertEqual(soup.h1.contents[0], 'Useless heading 1')

    def test_smooth_many(self):
        soup = BeautifulSoup('<h1>Useless heading 1</h1>', 'html.parser')

        for i in range(1000):
            soup.h1.append(str(i))
        
        self.assertEqual(soup.h1.contents[1000], '999')
        soup.h1.smooth()
        self.assertEqual(soup.h1.contents[0][-3:], '999')

    def test_get_text_basic(self):
        soup = BeautifulSoup('<h1>Hello <i>world</i>!</h1>', 'html.parser')
        text = soup.get_text()
        self.assertEqual(text, 'Hello world!')
    
    def test_get_text_join(self):
        soup = BeautifulSoup('<h1>Hello<i>world</i>!</h1>', 'html.parser')
        text = soup.get_text('|')
        self.assertEqual(text, 'Hello|world|!')
    
    def test_get_text_strip(self):
        soup = BeautifulSoup('<h1> Hello <i> world </i> ! </h1>', 'html.parser') 
        text_unstripped = soup.get_text()
        self.assertEqual(text_unstripped, ' Hello  world  ! ')
        text_stripped = soup.get_text(strip = True)
        self.assertEqual(text_stripped, 'Helloworld!')

    def test_get_text_stripped_strings(self):
        soup = BeautifulSoup('<h1> Hello <i> world </i> ! </h1>', 'html.parser') 
        res = [text for text in soup.stripped_strings]
        
        self.assertEqual(res[0], 'Hello')
        self.assertEqual(res[1], 'world')
        self.assertEqual(res[2], '!')

class TreeModificationTests(unittest.TestCase):

    test_tree = """
    <html><head><title>Title text</title></head>
    <body>
    <p class="p_class1"></p>
    <p class="p_class2"></p>
    <a href="https://www.google.com/">Google link></a>
    </body>
    </html>
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
        tree.contents[0].insert_before()
        self.assertEqual(tree.prettify(), expected.prettify())

    def test_insert_before_PageElement_multiple(self):
        tree = BeautifulSoup(self.test_tree, "html.parser")
        expected = [BeautifulSoup("<p>Test paragraph</p>", "html.parser"), BeautifulSoup("<p>Test paragraph 2</p>", "html.parser")]
        tree.contents[0].insert_before(expected[0], expected[1])
        self.assertEqual(str(tree.contents[0]), "<p>Test paragraph</p>")
        self.assertEqual(str(tree.contents[1]), "<p>Test paragraph 2</p>")

    def test_insert_before_string_multiple(self):
        tree = BeautifulSoup(self.test_tree, "html.parser")
        expected = ["<p>Test paragraph</p>", "<p>Test paragraph 2</p>"]
        tree.body.contents[0].insert_before(expected[0], expected[1])
        self.assertEqual(tree.body.contents[0].string, expected[0])
        self.assertEqual(tree.body.contents[1].string, expected[1])

    def test_insert_before_self_in_args(self):
        tree = BeautifulSoup(self.test_tree, "html.parser")
        with self.assertRaises(ValueError):
            tree.contents[0].insert_before(tree.contents[0])
    
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

# st_gabe 
class TreeFindTest(unittest.TestCase):
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
        <aside:colon>Hello, World!</aside:colon>
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
            self.assertTrue(i < 3)
            self.assertEqual(str(link), expected_links[i])

    # Test find all objects of a type but there are none
    def test_find_all_empty(self):
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        li = soup.find_all('li')

        self.assertTrue(len(li) == 0)
 
    #Test find all with limit ADDITION FOR COVERAGE
    def test_find_all_limit(self):
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        links = soup.find_all('a', limit=2)
        expected_links = [
            '<a href="https://www.wikipedia.org/">This is a hyperlink to wikipedia!</a>',
            '<a href="https://www.facebook.com/">This is a hyperlink to facebook!</a>'
        ]
        
        for (i, link) in enumerate(links):
            self.assertTrue(i < 2)
            self.assertEqual(str(link), expected_links[i])

    # Test SoupStrainer ADDITION FOR COVERAGE
    def test_find_all_soup_strainer(self):
        only_a_tags = SoupStrainer('a')
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        links = soup.find_all(only_a_tags)
        expected_links = [
            '<a href="https://www.wikipedia.org/">This is a hyperlink to wikipedia!</a>',
            '<a href="https://www.facebook.com/">This is a hyperlink to facebook!</a>',
            '<a href="https://creativecommons.org/">Site goes under Creative Commons</a>'
        ]
        
        for (i, link) in enumerate(links):
            self.assertTrue(i < 3)
            self.assertEqual(str(link), expected_links[i])

    # Test name ADDITION FOR COVERAGE
    def test_find_all_name(self):
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        links = soup.find_all(True)
        self.assertIsNotNone(links)

    # Test colon name ADDITION FOR COVERAGE
    def test_find_all_colon_name(self):
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        aside = soup.find_all('aside:colon')

        self.assertEqual(str(aside[0]), '<aside:colon>Hello, World!</aside:colon>')

    # Test non recursive call ADDITION FOR COVERAGE
    def test_find_all_non_recursive(self):
        soup = BeautifulSoup(self.html_text_gabe, 'html.parser')
        links = soup.find_all('a', recursive=False)
        expected_links = [
            '<a href="https://www.wikipedia.org/">This is a hyperlink to wikipedia!</a>',
            '<a href="https://www.facebook.com/">This is a hyperlink to facebook!</a>',
            '<a href="https://creativecommons.org/">Site goes under Creative Commons</a>'
        ]

        for (i, link) in enumerate(links):
            self.assertTrue(i < 3)
            self.assertEqual(str(link), expected_links[i])

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