from crawler.yahoo_crawler import YahooCrawler

if __name__ == "__main__":
    region = input("Digite a região: ")
    crawler = YahooCrawler(region)
    crawler.run()
