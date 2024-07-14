import scrapy

class diet_plans(scrapy.Spider):
    name = "diet_plans"
    start_urls = ['https://www.muscleandstrength.com/diet-plans']

    def parse(self, response):
        # Scraping for data to yield
        for data in self.scrape_data(response):
            yield data

    def scrape_data(self, response):
        in_diet_guides = False
        in_trending_nutrition_articles = False
        titles = []
        summaries = []
        for category in response.css('div.cell'):
            category_name = category.css('div.category-name::text').get()
            if category_name:
                yield{
                        'section': 'Healthy Recipes',
                        'category_name': category_name,
                }
        for element in response.xpath('//h2 | //div[@class="node-title"] | //div[@class="node-short-summary"]'):
            text = element.xpath('text()').get()

            if text == 'Diet Guides':
                in_diet_guides = True
                in_trending_nutrition_articles = False
                titles.clear()
                summaries.clear()
            elif text == 'Trending Nutrition Articles':
                in_trending_nutrition_articles = True
                in_diet_guides = False
                titles.clear()
                summaries.clear()

            if in_diet_guides or in_trending_nutrition_articles:
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
                            'section': 'Diet Guides' if in_diet_guides else 'Trending Nutrition Articles',
                            'title': title,
                            'description': summary
                        }
                    titles.clear()
                    summaries.clear()

        # Collect remaining titles and summaries in case not yet yielded
        if len(titles) == len(summaries):
            for title, summary in zip(titles, summaries):
                yield {
                    'section': 'Diet Guides' if in_diet_guides else 'Trending Nutrition Articles',
                    'title': title,
                    'description': summary
                }

