import requests
from bs4 import BeautifulSoup
import csv
import re
from urllib.parse import urljoin

def scrape_muscle_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    p_tags = soup.find_all('p', class_='elementor-heading-title elementor-size-default')
    links = []
    
    for p in p_tags:
        a_tag = p.find('a')
        if a_tag and 'href' in a_tag.attrs:
            link = a_tag['href']
            if 'muscle' in link:
                links.append(link)

    # print("scrape_mucle_page returns: ", links) this one works
    return links

def scrape_exercise_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    articles = soup.find_all('article', class_=lambda x: x and 'elementor-post' in x.split())
    print(" articlesc :", articles)
    exercises = []
    
    for article in articles:
        exercise = {}
        
        # Extract exercise name and URL
        name_tag = article.select_one('h4.elementor-heading-title a')
        if name_tag:
            exercise['name'] = name_tag.text.strip()
            exercise['url'] = name_tag['href']
                
        # Extract muscle group
        muscle_tag = article.select_one('.elementor-text-editor:contains("Muscle Group:")')
        if muscle_tag:
            muscle_link = muscle_tag.find('a')
            exercise['muscle_group'] = muscle_link.text.strip() if muscle_link else ''
        
        # Extract equipment
        equipment_tag = article.select_one('.elementor-text-editor:contains("Equipment:")')
        if equipment_tag:
            equipment_link = equipment_tag.find('a')
            exercise['equipment'] = equipment_link.text.strip() if equipment_link else ''
        
        
        exercises.append(exercise)
    
    # Check for next page
    next_page = None
    pagination = soup.select_one('.elementor-pagination')
    if pagination:
        current_page = pagination.select_one('.page-numbers.current')
        if current_page:
            next_page_element = current_page.find_next_sibling('a', class_='page-numbers')
            if next_page_element:
                next_page = urljoin(url, next_page_element['href'])
    print("exercices", exercises)
    return exercises, next_page

def save_to_csv(exercises, filename='exercises.csv'):
    keys = exercises[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(exercises)


def main():
    base_url = "https://www.hevyapp.com/muscle"
    muscle_links = scrape_muscle_page(base_url)

    all_exercises = []
    
    for link in muscle_links:
        # print("going to this muscle link: ", link)
        page_url = link
        while page_url:
            print(f"Scraping: {page_url}")
            exercises, next_page = scrape_exercise_page(page_url)
            all_exercises.extend(exercises)
            page_url = next_page
    
    # Save to CSV
    # with open('exercises.csv', 'w', newline='', encoding='utf-8') as csvfile:
    #     fieldnames = ['name', 'url', 'muscle_group', 'equipment']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
    #     writer.writeheader()
    #     for exercise in all_exercises:
    #         writer.writerow(exercise)

    # Save to CSV
    if all_exercises:
        save_to_csv(all_exercises)
    
    print(f"Scraped {len(all_exercises)} exercises and saved to exercises.csv")

if __name__ == "__main__":
    main()
