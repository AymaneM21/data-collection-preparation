import os
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# URL of the website
url = "https://mjfitness.au/pages/articles"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object
soup = BeautifulSoup(response.content, 'html.parser')

articles = soup.find_all('article', class_='card-article card')

data = []

# Loop through each article and extract the description and link
for article in articles:
    link = article.find('a')['href']
    full_link = f"https://mjfitness.au{link}"
    
    # Extract the description
    description = article.find('p', class_='card__description').text.strip()
    
    # Extract the title
    title = article.find('p', class_='card__title').text.strip()
    
    # Extract the author
    author = article.find('p', class_='card__blog-title').text.strip().replace('by ', '')
    
    # Add to data list
    data.append([title, author, description, full_link])

filename = f"mjfitness_articles.csv"

# Create the path for the Data folder
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
data_dir = os.path.join(parent_dir, 'Data')

# Create the Data folder if it doesn't exist
os.makedirs(data_dir, exist_ok=True)

# Full path for the CSV file
file_path = os.path.join(data_dir, filename)

# Write data to CSV file
with open(file_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Author', 'Description', 'Link'])  # Write header
    writer.writerows(data)

print(f"Data has been saved to {filename}")


'''<article class="card-article card ">
  <a href="/blogs/supplements/alcohol-fitness-balancing-your-health-goals-and-social-life"><figure class="figure--landscape style--padding" role="none">
        <img src="//mjfitness.au/cdn/shop/articles/alcohol-fitness-balancing-your-health-goals-and-social-life-475039.jpg?v=1709150232&amp;width=800" alt="Alcohol &amp; Fitness: Balancing Your Health Goals And Social Life - MJ Fitness" srcset="//mjfitness.au/cdn/shop/articles/alcohol-fitness-balancing-your-health-goals-and-social-life-475039.jpg?v=1709150232&amp;width=352 352w, //mjfitness.au/cdn/shop/articles/alcohol-fitness-balancing-your-health-goals-and-social-life-475039.jpg?v=1709150232&amp;width=400 400w" width="400" class="img-absolute loaded">
      </figure><div class="card__content">
          
          

            <p class="card__blog-title text-xs">by Brandon Verde</p>
          
          <p class="card__title">Alcohol &amp; Fitness: Balancing Your Health Goals And Social Life
</p><p class="card__description text-md">Explore the balance between socialising and fitness goals when it comes to alcohol consumption. Learn about the impact of alcohol on muscle growth, dehydration, metabolism, and sleep, and discover strategies for making smarter drink choices while still enjoying a night out. With moderation and mindfulness, you can maintain your fitness progress without sacrificing your social life.</p></div><div class="card__bottom">
      <p class="button--plain swiper-no-swiping">
        Read more
      </p>
    </div>
  </a>
</article> '''