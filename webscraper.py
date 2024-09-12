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

# Function to detect and scrape forms from the page
def scrape_forms(url):
    html_content = get_html_content(url)
    if not html_content:
        return None

    soup = BeautifulSoup(html_content, 'html.parser')

    forms = soup.find_all('form')

    if not forms:
        print("No forms found on the page.")
        return None

    print(f"Found {len(forms)} form(s) on the page.")

    # Iterate over forms and extract fields
    for i, form in enumerate(forms):
        print(f"\nForm {i+1}:")
        form_action = form.get('action')
        form_method = form.get('method', 'get').lower()  # Default method is GET

        print(f"Action: {form_action}")
        print(f"Method: {form_method.upper()}")

        # Get all input fields
        form_inputs = form.find_all('input')
        form_data = {}

        for input_element in form_inputs:
            input_name = input_element.get('name')
            input_type = input_element.get('type')
            input_value = input_element.get('value', '')

            # Fill the form automatically (this is where you customize)
            if input_type == 'text':
                # Default text field value
                form_data[input_name] = 'default_text_value'
            elif input_type == 'email':
                form_data[input_name] = 'example@example.com'
            elif input_type == 'password':
                form_data[input_name] = 'password123'
            elif input_type == 'hidden':
                # Hidden fields, use their default value
                form_data[input_name] = input_value
            else:
                # Add a placeholder for unhandled input types
                form_data[input_name] = input_value

        print("Form data to be submitted:")
        print(form_data)

        # Submit the form
        submit_form(url, form_action, form_method, form_data)

# Function to submit the form with the data
def submit_form(base_url, form_action, form_method, form_data):
    if not form_action.startswith("http"):
        # If form action is relative, build the full URL
        form_action = f"{base_url.rstrip('/')}/{form_action.lstrip('/')}"

    try:
        if form_method == 'post':
            response = requests.post(form_action, data=form_data)
        else:
            response = requests.get(form_action, params=form_data)

        # Print the response from the form submission
        if response.status_code == 200:
            print("Form submitted successfully!")
            print("Response:")
            print(response.text[:500])  # Print the first 500 characters of the response
        else:
            print(f"Form submission failed with status code: {response.status_code}")
    except Exception as e:
        print(f"Error during form submission: {e}")

# Main function to get user input and perform scraping
def main():
    url = input("Enter the URL to scrape: ")
    soup = scrape_entire_page(url)
    form = scrape_forms(url)

    if soup:
        print("Scraping successful! Exporting to PDF...")
        export_to_pdf(soup, "scraped_content.pdf")
    else:
        print("Forms submitted successfully.")
        export_to_pdf(form, "submitted_forms.pdf")

if __name__ == "__main__":
    main()
