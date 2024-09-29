import datascraper
import dill
import regex_patterns
import graph

def main():
    #regex_patterns.process_shared_last_names("Removed_empty_brackets.txt", "Short_caption_couple_names.txt")
    #regex_patterns.remove_titles("All_couples_together2.txt", "Removed_titles.txt")


    graph.separate_potential_unreleated_captions("../Removed_titles.txt")
    d = graph.parse_caption("Ron Iervolino, Trish Iervolino, Russ Middleton, and Lisa Middleton")
    print(d)

if __name__ == "__main__":
    main()