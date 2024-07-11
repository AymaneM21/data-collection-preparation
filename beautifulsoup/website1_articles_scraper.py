import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
   
    # Extract main article info
    hero_section = soup.find('section', class_='shopify-section hero-basic')
    title = hero_section.find('h1').text.strip() if hero_section else "No title found"
   
    byline = soup.find('p', class_='byline text-xs')
    author_date = byline.text.strip() if byline else "No author or date found"
   
    description_div = hero_section.find('div', class_='hero-basic__description') if hero_section else None
    if description_div:
        description_span = description_div.find('span')
        description = description_span.text.strip() if description_span else "No description found"
    else:
        description = "No description found"
   
    # Extract article content
    article_section = soup.find('article', class_='shopify-section article')
    content = []
   
    if article_section:
        # Get the general content (first p tag before any h2)
        general_content = article_section.find('p').text.strip() if article_section.find('p') else "No general content found"
        content.append(("General Content", general_content))
       
        # Get all h2 and following p tags
        current_heading = None
        for element in article_section.find_all(['h2', 'p']):
            if element.name == 'h2':
                current_heading = element.text.strip()
            elif element.name == 'p' and current_heading:
                content.append((current_heading, element.text.strip()))
   
    return title, author_date, description, content

def save_to_csv(data, filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(parent_dir, 'Data')
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, filename)
   
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Title', 'Author and Date', 'Description', 'Link', 'Content Heading', 'Content'])
        writer.writerow([data[0], data[1], data[2], data[3], 'General Content', data[4][0][1]])
        for heading, content in data[4][1:]:
            writer.writerow(['', '', '', '', heading, content])
   
    print(f"Data has been appended to {file_path}")

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
data_dir = os.path.join(parent_dir, 'Data')
input_csv = "mjfitness_articles.csv"
Input_file_path = os.path.join(data_dir, input_csv)
output_csv = f"mjfitness_articles_details.csv"
Output_file_path = os.path.join(data_dir, output_csv)

with open(Input_file_path, 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header
    for row in reader:
        link = row[3]  # Assuming the link is in the 4th column
        try:
            title, author_date, description, content = scrape_website(link)
            # Save the data to the output CSV
            save_to_csv((title, author_date, description, link, content), Output_file_path)
        except Exception as e:
            print(f"Error processing {link}: {str(e)}")