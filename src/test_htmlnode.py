import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def setUp(self):
        # Set up a sample HTMLNode for testing
        self.node = HTMLNode(tag="div", value="Hello, World!", props={"class": '"container"'})
        print(self.node.__repr__())

    def test_tag_initialization(self):
        # Test if the tag is initialized correctly
        self.assertEqual(self.node.tag, "div")

    def test_value_initialization(self):
        # Test if the value is initialized correctly
        self.assertEqual(self.node.value, "Hello, World!")

    def test_props_initialization(self):
        # Test if the props are initialized correctly
        self.assertEqual(self.node.props, {"class": '"container"'})

    def test_prop_to_html(self):
        # Test the prop_to_html method
        expected_output = ' class="container"'
        self.assertEqual(self.node.prop_to_html(), expected_output)

    def test_children_initialization(self):
        # Test if children are initialized correctly
        self.assertEqual(self.node.children, [])

if __name__ == "__main__":
    unittest.main()
