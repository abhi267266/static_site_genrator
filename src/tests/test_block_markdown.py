import unittest
import textwrap
from src.block_markdown import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = textwrap.dedent("""
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
        """).strip()

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_whitespace(self):
        self.assertEqual(markdown_to_blocks("   \n   \n"), [])

    def test_single_paragraph(self):
        md = "Just a single line paragraph with **bold** text."
        self.assertEqual(markdown_to_blocks(md), [md])

    def test_multiple_blank_lines(self):
        md = "Para one\n\n\n\nPara two"
        self.assertEqual(markdown_to_blocks(md), ["Para one", "Para two"])

    def test_leading_and_trailing_blank_lines(self):
        md = "\n\nFirst block\n\nSecond block\n\n"
        self.assertEqual(markdown_to_blocks(md), ["First block", "Second block"])

    def test_only_list_block(self):
        md = "- item1\n- item2"
        self.assertEqual(markdown_to_blocks(md), ["- item1\n- item2"])

    def test_indented_text(self):
        md = textwrap.dedent("""
            Line with indent
                Still indented
        """).strip()
        self.assertEqual(
            markdown_to_blocks(md),
            ["Line with indent\n    Still indented"],
        )

    def test_paragraph(self):
        block = "This is a normal paragraph with text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block2 = "### Subheading level 3"
        self.assertEqual(block_to_block_type(block2), BlockType.HEADING)

    def test_code(self):
        block = "```\nprint('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> This is a quote\n> continued on next line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_numbers(self):
        block = "1. First item\n3. Second item\n4. Third item"
        # Should fallback to paragraph since numbers aren't sequential
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_mixed_block(self):
        block = "> Quote line\n- Not a list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_like_paragraph(self):
        block = "```\nNot a real code block"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title(self):
        from src.block_markdown import extract_title

        # Test with a valid H1 header
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")

        # Test with leading and trailing whitespace
        md = "  #   Hello World   "
        self.assertEqual(extract_title(md), "Hello World")

        # Test with no H1 header
        md = "## Subheading\nSome content"
        with self.assertRaises(ValueError):
            extract_title(md)

        # Test with multiple lines, only the first H1 should be considered
        md = "# First Title\n## Subheading\n# Another Title"
        self.assertEqual(extract_title(md), "First Title")

        # Test with no markdown content
        md = ""
        with self.assertRaises(ValueError):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()