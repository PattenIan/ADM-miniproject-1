import datascraper
import dill

def main():
    #links = datascraper.gather_all_links()
    #aptions, length = datascraper.clean_captions(datascraper.get_captions("https://web.archive.org/web/20151114014941/http://www.newyorksocialdiary.com/party-pictures/2015/celebrating-the-neighborhood"))
    #print(captions)
    #print(datascraper.regex_comma_separate(captions))

    links = datascraper.get_links('nysd-links.pkd')
    print(links)
    print(len(links))

    datascraper.get_all_captions()

if __name__ == "__main__":
    main()