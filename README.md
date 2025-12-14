# Cyberlab-2
1. Retrieving HTML pages

The script sends an HTTP GET request to the website using the requests library. The HTML content of the page is downloaded and returned as text. A simple user-agent header is added so the request looks like it is coming from a real browser.

2. Getting the list of books on the page

After retrieving the HTML, BeautifulSoup parses it into a searchable structure.
Each book on the page is contained inside an HTML element <article class="product_pod">.
The script locates all such elements and treats each one as a single book entry.

3. Extracting book links and converting them to absolute URLs

For every book element:

The <a> tag inside <h3> is used to extract the book title and the link (href).

These links are relative paths (for example catalogue/book_1/index.html).

The urljoin() function converts each relative link into a full absolute URL so the book page can be accessed directly.

At this stage, the script builds a list of books containing:

title

price

absolute URL to the book page

4. Parsing a specific book page

When a book’s URL is opened:

The title, price, and availability are extracted from the main product section.

The book description is read from the paragraph following the product_description anchor.

Additional details such as UPC, product type, and tax information are extracted from the product information table and stored in a dictionary.

This allows the script to fully analyze an individual book page rather than just the listing view.
