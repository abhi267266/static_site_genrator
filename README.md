# Static Site Generator

## Overview
The Static Site Generator is a Python-based tool that converts Markdown files into static HTML pages. It supports nested folder structures, allowing you to organize your content efficiently. The generator uses a customizable HTML template to ensure consistent styling across all pages.

## Features
- Converts Markdown files to HTML.
- Supports nested folder structures in the `content` directory.
- Uses a customizable HTML template.
- Copies static assets (e.g., CSS, images) from the `static` directory to the `public` directory.
- Outputs the generated site to the `public` directory.

## Project Structure
```
static_site_genrator/
├── content/          # Markdown files to be converted
├── public/           # Generated HTML files and copied static assets
├── static/           # Static assets (CSS, images, etc.)
├── template.html     # HTML template with placeholders for title and content
├── main.py           # Entry point for the generator
├── src/              # Source code for the generator
│   ├── block_markdown.py
│   ├── htmlnode.py
│   ├── inline_markdown.py
│   ├── textnode.py
│   └── tests/        # Unit tests
└── README.md         # Project documentation
```

## How It Works
1. **Delete Existing Output**: Clears the `public` directory.
2. **Copy Static Files**: Copies all files from the `static` directory to the `public` directory.
3. **Process Markdown Files**: Recursively processes all Markdown files in the `content` directory, converting them to HTML using the `template.html` file.
4. **Generate HTML**: Replaces `{{ Title }}` and `{{ Content }}` placeholders in the template with the page title and content.

## Usage
### Prerequisites
- Python 3.8 or higher

### Running the Generator
1. Place your Markdown files in the `content` directory.
2. Place your static assets (CSS, images, etc.) in the `static` directory.
3. Customize the `template.html` file as needed.
4. Run the generator:
   ```bash
   python main.py
   ```
5. The generated site will be available in the `public` directory.

## Example
### Input
**content/index.md**:
```
# Welcome

This is the homepage of the static site.
```

**template.html**:
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ Title }}</title>
</head>
<body>
    <h1>{{ Title }}</h1>
    <div>{{ Content }}</div>
</body>
</html>
```

### Output
**public/index.html**:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Welcome</title>
</head>
<body>
    <h1>Welcome</h1>
    <div>
        <p>This is the homepage of the static site.</p>
    </div>
</body>
</html>
```

## Testing
Run the unit tests to ensure everything is working correctly:
```bash
python -m unittest discover src/tests
```
