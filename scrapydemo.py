import scrapy

class FantasyStatsSpider(scrapy.Spider):
    name = "fantasy_stats"

    # Start on the 2023 fantasy stats page
    start_urls = [
        'https://www.pro-football-reference.com/years/2023/fantasy.htm'
    ]

    def parse(self, response):
        # Select the fantasy stats table
        rows = response.css('table#fantasy tbody tr')

        for row in rows:
            # Skip empty rows (if any)
            if row.css('th::text').get() is None:
                continue

            yield {
                'Player': row.css('td[data-stat="player"] a::text').get(),
                'Team': row.css('td[data-stat="team"] a::text').get(),
                'Position': row.css('td[data-stat="fantasy_pos"]::text').get(),
                'Points': row.css('td[data-stat="fantasy_points"]::text').get(),
            }

        # If there's a "Next" page for more stats, follow it
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
