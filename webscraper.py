import requests
from bs4 import BeautifulSoup
from fpdf import FPDF

# Function to get HTML content from a URL
def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

# Function to scrape the entire page and return the content with formatting
def scrape_entire_page(url):
    html_content = get_html_content(url)
    if not html_content:
        return None

    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

# Function to export content to a PDF with proper formatting and UTF-8 handling
def export_to_pdf(soup, filename):
    pdf = FPDF()
    pdf.add_page()

    # Load UTF-8 compatible fonts
    pdf.add_font("DejaVu", '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)  # Regular font
    pdf.add_font("DejaVu", 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', uni=True)  # Bold font
    pdf.set_font("DejaVu", '', 12)

    # Extract elements from the soup and preserve the formatting
    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'li']):
        if element.name == 'h1':
            pdf.set_font("DejaVu", 'B', 16)  # Heading 1 - Bold
            pdf.multi_cell(0, 10, element.get_text(strip=True))
            pdf.ln(5)
        elif element.name == 'h2':
            pdf.set_font("DejaVu", 'B', 14)  # Heading 2 - Bold
            pdf.multi_cell(0, 10, element.get_text(strip=True))
            pdf.ln(5)
        elif element.name == 'h3':
            pdf.set_font("DejaVu", 'B', 12)  # Heading 3 - Bold
            pdf.multi_cell(0, 10, element.get_text(strip=True))
            pdf.ln(5)
        elif element.name == 'p':
            pdf.set_font("DejaVu", '', 12)  # Paragraph - Regular
            pdf.multi_cell(0, 10, element.get_text(strip=True))
            pdf.ln(5)
        elif element.name == 'li':
            pdf.set_font("DejaVu", '', 12)  # List item - Regular
            pdf.multi_cell(0, 10, f"- {element.get_text(strip=True)}")
            pdf.ln(5)

    pdf.output(filename)
    print(f"Content exported to {filename}")

# Main function to get user input and perform scraping
def main():
    url = input("Enter the URL to scrape: ")
    soup = scrape_entire_page(url)

    if soup:
        print("Scraping successful! Exporting to PDF...")
        export_to_pdf(soup, "scraped_content.pdf")
    else:
        print("Scraping was not successful.")


if __name__ == "__main__":
    main()
