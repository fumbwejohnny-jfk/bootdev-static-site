# Boot.dev Static Site

A simple static website project built as part of the Boot.dev curriculum. This project demonstrates foundational front-end web development concepts using plain HTML and CSS, with deployment through GitHub Pages.

🌐 Live Site: https://fumbwejohnny-jfk.github.io/bootdev-static-site/

---

## Features

- Responsive static web page
- Clean semantic HTML structure
- Custom CSS styling
- Lightweight and fast-loading
- Hosted with GitHub Pages

---

## Tech Stack

- HTML5
- CSS3
- GitHub Pages
- Python

---

## Project Structure

```text
bootdev-static-site/
├── content/
│    ├── blog/
│       ├── glorfindel/
│           ├── index.md
│       ├── majesty/
│           ├── index.md
│       ├── tom/
│           ├── index.md
├── docs/
│    ├── blog/
│       ├── glorfindel/
│           ├── index.html
│       ├── majesty/
│           ├── index.html
│       ├── tom/
│           ├── index.html
├── src/
│   ├── index.html
│   ├── helpers.py
│   ├── htmlnode.py
│   ├── textnode.py
│   ├── test_htmlnode.py
│   ├── test_textnode.py
├── static/
│    ├── images/
│       ├── glorfindel.png
│       ├── rivendell.png
│       ├── tolkien.png
│       ├── tom.png
│    ├── index.css
├── main.py
├── template.html
├── main.sh
├── test.sh
└── .gitignore
```

> Folder names may vary depending on your implementation.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/fumbwejohnny-jfk/bootdev-static-site.git
```

### 2. Navigate into the project folder

```bash
cd bootdev-static-site
```

### 3. Open the project

Or run a local development server:

```bash
./main.sh
```

Then visit:

```text
http://localhost:8000
```

---

## Deployment

This project is deployed using **GitHub Pages**.

To deploy updates:

1. Push changes to the `main` branch
2. GitHub Pages will automatically rebuild and publish the site

---

## Learning Objectives

This project was created to practice:

- Structuring web pages with semantic HTML
- Styling layouts with CSS
- Organizing static site assets
- Deploying projects with GitHub Pages
- Basic responsive design principles
- Generating web pages using python

---

## Future Improvements

- Add JavaScript interactivity
- Improve responsive mobile layout
- Add animations and transitions
- Optimize accessibility
- Expand content sections

---

## Author

Created by **Johnny Fumbwe**

GitHub: https://github.com/fumbwejohnny-jfk

---

## License

This project is open source and available under the MIT License.
