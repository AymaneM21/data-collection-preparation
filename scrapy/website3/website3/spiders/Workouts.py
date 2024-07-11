import scrapy

class Workouts(scrapy.Spider):
    name = "workout_routines"
    start_urls = ['https://www.muscleandstrength.com/workout-routines']

    def parse(self, response):
        # Scraping for data to yield
        for data in self.scrape_data(response):
            yield data

    def scrape_data(self, response):
        in_best_workouts = False
        in_new_workouts = False
        in_tips_advice = False
        titles = []
        summaries = []
        for category in response.css('div.cell'):
            category_name = category.css('div.category-name::text').get()
            if category_name:
                yield{
                        'section': 'categories',
                        'category_name': category_name,
                }
        for element in response.xpath('//h2 | //div[@class="node-title"] | //div[@class="node-short-summary"]'):
            text = element.xpath('text()').get()

            if text == 'Best Workouts':
                in_best_workouts = True
                in_new_workouts = False
                in_tips_advice = False
                titles.clear()
                summaries.clear()
            elif text == 'New Workouts':
                in_new_workouts = True
                in_best_workouts = False
                in_tips_advice = False
                titles.clear()
                summaries.clear()
            elif text == 'Workout Tips & Advice':
                in_tips_advice = True
                in_best_workouts = False
                in_new_workouts = False
                titles.clear()
                summaries.clear()

            if in_best_workouts or in_new_workouts:
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
                            'section': 'Best Workouts' if in_best_workouts else 'New Workouts',
                            'title': title,
                            'description': summary
                        }
                    titles.clear()
                    summaries.clear()

        # Collect remaining titles and summaries in case not yet yielded
        if len(titles) == len(summaries):
            for title, summary in zip(titles, summaries):
                yield {
                    'section': 'Best Workouts' if in_best_workouts else 'New Workouts',
                    'title': title,
                    'description': summary
                }

        # Scraping Workout Tips & Advice section
        if in_tips_advice:
            content_elements = response.css('div.field-item.even *::text').getall()
            content = ' '.join(content_elements).strip()

            # Yielding the extracted content
            yield {
                'Tips': content
            }

