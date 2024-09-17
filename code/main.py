import datascraper

def main():
    #datascraper.gather_all_links()
    print(datascraper.clean_captions(datascraper.get_captions("https://web.archive.org/web/20151114014941/http://www.newyorksocialdiary.com/party-pictures/2015/celebrating-the-neighborhood")))

if __name__ == "__main__":
    main()