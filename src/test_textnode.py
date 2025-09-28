import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_same_properties(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_eq_different_text(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("Different text", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_text_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_url(self):
        node1 = TextNode("This is a link", TextType.LINK, url="https://example.com")
        node2 = TextNode("This is a link", TextType.LINK, url="https://another.com")
        self.assertNotEqual(node1, node2)

    def test_eq_with_none_url(self):
        node1 = TextNode("Plain text", TextType.TEXT, url=None)
        node2 = TextNode("Plain text", TextType.TEXT, url=None)
        self.assertEqual(node1, node2)

    def test_repr_output(self):
        node = TextNode("Hello", TextType.CODE, url=None)
        expected_repr = "TextNode(Hello, code, None)"
        self.assertEqual(repr(node), expected_repr)


if __name__ == "__main__":
    unittest.main()
