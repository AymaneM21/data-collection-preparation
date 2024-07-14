import csv
import os
import requests
from bs4 import BeautifulSoup
import re
import html2text


def clean_filename(filename):
    return re.sub(r'[^\w\-_\. ]', '_', filename)

def scrape_page(url, name, muscle_group, equipment):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract title
    title_div = soup.find('div', class_='elementor-page-title')
    title = title_div.find('h1').text.strip() if title_div else 'No title found'
    
    # Extract content
    content_div = soup.find('div', class_='elementor-widget-theme-post-content')
    if content_div:
        # Convert HTML to Markdown while preserving structure
        h = html2text.HTML2Text()
        h.body_width = 0  # Disable line wrapping
        content = h.handle(str(content_div))

        # Clean up the content
        content = re.sub(r'\n{3,}', '\n\n', content)  # Remove excess newlines
        content = content.strip()

        filename = clean_filename(f"{name}_{muscle_group}_{equipment}.md")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n{content}")

        
        # Extract video links
        video_links = []
        videos = content_div.find_all('video')
        for video in videos:
            if 'src' in video.attrs:
                video_links.append(video['src'])
        
        return title, video_links
    else:
        print(f"No content found for {url}")
        return None, []

def main():
    input_file = './data/hevyapp_exercises.csv'
    output_file = './data/exercices/video_links.csv'
    
    with open(input_file, 'r') as csvfile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(csvfile)
        writer = csv.writer(outfile)
        writer.writerow(['Name', 'Muscle Group', 'Equipment', 'Title', 'Video URL'])
        
        for row in reader:
            name = row['name']
            url = row['url']
            muscle_group = row['muscle_group']
            equipment = row['equipment']
            
            print(f"Scraping {url}...")
            title, video_links = scrape_page(url, name, muscle_group, equipment)
            
            if title:
                for video_link in video_links:
                    writer.writerow([name, muscle_group, equipment, title, video_link])
            
    print("Scraping completed!")

if __name__ == "__main__":
    main()