import datascraper
import dill
import regex_patterns

def main():
    #regex_patterns.process_shared_last_names("Removed_empty_brackets.txt", "Short_caption_couple_names.txt")
    regex_patterns.process_shared_last_names("All_couples_together.txt", "All_couples_together2.txt")

if __name__ == "__main__":
    main()