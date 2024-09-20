import datascraper

def main():
    #datascraper.gather_all_links()
    captions, length = datascraper.clean_captions(datascraper.get_captions("https://web.archive.org/web/20151114014941/http://www.newyorksocialdiary.com/party-pictures/2015/celebrating-the-neighborhood"))
    print(captions)
    print(datascraper.regex_comma_separate(captions))
if __name__ == "__main__":
    main()