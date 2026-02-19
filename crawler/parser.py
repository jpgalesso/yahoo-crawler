from bs4 import BeautifulSoup


class YahooParser:

    def parse(self, html):
        soup = BeautifulSoup(html, "html.parser")

        data = []
        rows = soup.find_all("tr")

        for row in rows:
            cols = row.find_all("td")

            if len(cols) >= 3:
                symbol = cols[1].text.strip()
                name = cols[2].text.strip()
                price = cols[4].text.strip()

                data.append({
                    "symbol": symbol,
                    "name": name,
                    "price": price
                })

        return data
