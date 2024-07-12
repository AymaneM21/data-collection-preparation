import scrapy

class recipes(scrapy.Spider):
    name = "recipes"
    start_urls = ['https://www.muscleandstrength.com/recipes']

    def parse(self, response):
        # Scraping for data to yield
        for data in self.scrape_data(response):
            yield data

    def scrape_data(self, response):
        in_trending_recipes = False
        in_new_recipes = False
        titles = []
        summaries = []
        for category in response.css('div.cell'):
            category_name = category.css('div.category-name::text').get()
            if category_name:
                yield{
                        'section': 'Recipe Categories',
                        'category_name': category_name,
                }
        for element in response.xpath('//h2 | //div[@class="node-title"] | //div[@class="node-short-summary"]'):
            text = element.xpath('text()').get()

            if text == 'New Recipes':
                in_new_recipes = True
                in_trending_recipes = False
                titles.clear()
                summaries.clear()
            elif text == 'Trending Recipes':
                in_new_recipes = True
                in_trending_recipes = False
                titles.clear()
                summaries.clear()

            if in_trending_recipes or in_new_recipes:
                if 'node-title' in element.xpath('@class').get():
                    title = element.xpath('.//a/text()').get()
                    if title:
                        titles.append(title)
                elif 'node-short-summary' in element.xpath('@class').get():
                    summary = element.xpath('text()').get()
                    if summary:
                        summaries.append(summary)

                # Yield the titles and summaries in pairs
                if len(titles) == len(summaries):
                    for title, summary in zip(titles, summaries):
                        yield {
                            'section': 'New Recipes' if in_trending_recipes else 'Trending Recipes',
                            'title': title,
                            'description': summary
                        }
                    titles.clear()
                    summaries.clear()

        # Collect remaining titles and summaries in case not yet yielded
        if len(titles) == len(summaries):
            for title, summary in zip(titles, summaries):
                yield {
                    'section': 'New Recipes' if in_trending_recipes else 'Trending Recipes',
                    'title': title,
                    'description': summary
                }

