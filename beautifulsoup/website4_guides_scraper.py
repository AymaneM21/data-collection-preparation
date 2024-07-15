import re
import requests
from bs4 import BeautifulSoup
import csv
import html2text
import os

def scrape_guides_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all divs with the class "elementor-image"
    divs = soup.find_all('div', class_='elementor-image')
    
    links = []
    
    for div in divs:
        a_tag = div.find('a')
        if a_tag and 'href' in a_tag.attrs:
            href = a_tag['href']
            # Extract the title from the second part of the link
            if href.startswith('https://www.hevyapp.com/'):
                title = href[len('https://www.hevyapp.com/'):].strip('/')
                links.append((href, title))
    
    return links

def save_links_to_csv(links, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['URL', 'Title'])
        writer.writerows(links)


def read_links_from_csv(filename):
    links = []
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        next(reader)  # Skip first link 
        links = [(row[0], row[1]) for row in reader]
    return links


def save_content_to_md(url, title):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Remove header, footer, and navigation
    for tag in soup(['header', 'footer', 'nav']):
        tag.decompose()
    
    # Remove scripts and styles
    for script in soup(["script", "style"]):
        script.decompose()
    
    main_content = soup.find('div', class_=lambda x: x and 'elementor-column' in x.split() and 'elementor-col-50' in x.split() and 'elementor-top-column' in x.split())
    
    if not main_content:
        main_content = soup.body
        print("using option no 2 for ", title)
                # Convert the filtered HTML to Markdown
        h = html2text.HTML2Text()
        h.ignore_links = False
        content_md = h.handle(str(main_content))
        
                # Save to Markdown file
        filename = f"{title}.md"
        with open(filename, 'w', encoding='utf-8') as md_file:
            md_file.write(content_md)
        print(f"Saved {filename}")


    if main_content:
        print("using option no 1 for ", title)
        # Remove any remaining unneeded elements
        for nav in main_content.find_all(['nav', 'aside']):
            nav.decompose()
        for section in main_content.find_all('section', class_=lambda x: x and ('elementor-section' in x.split() and 'elementor-inner-section' in x.split() and 'elementor-element' in x.split()) or ('elementor-section' in x.split() and 'elementor-top-section' in x.split() and 'elementor-element' in x.split())):
            section.decompose()


        def remove_specified_divs(main_content):
            if not main_content:
                return
            
            # Use lambda functions to match divs containing the static parts of the class names
            class_sets = [
                ('elementor-share-buttons--view-icon',),
                ('elementor-widget-author-box',),
                ('elementor-widget', 'elementor-widget-post-comments')
            ]
            
            for class_set in class_sets:
                for div in main_content.find_all('div', class_=lambda x, class_set=class_set: x and all(cls in x.split() for cls in class_set)):
                    div.decompose()
            
            print("Specified divs removed!")
        remove_specified_divs(main_content)


        # Convert the filtered HTML to Markdown
        h = html2text.HTML2Text()
        h.ignore_links = False
        content_md = h.handle(str(main_content))
        
        # Save to Markdown file
        filename = f"{title}.md"
        with open(filename, 'w', encoding='utf-8') as md_file:
            md_file.write(content_md)
        print(f"Saved {filename}")
    else:
        print("Could not find the main content.")

        
def main():
    url = 'https://www.hevyapp.com/guides/'
    links = scrape_guides_links(url)
    filename='./data/guides/links.csv'

    save_links_to_csv(links, filename)
    print(f"Links saved to links.csv")

    links = read_links_from_csv(filename)

    os.makedirs('./data/guides/output_guides', exist_ok=True)
    os.chdir('./data/guides/output_guides')

    # Extract content and save to Markdown files
    for url, title in links:
        save_content_to_md(url, title)

if __name__ == "__main__":
    main()