import re

def extract_names(captions):
    pattern = r'(?<=\[)[^][.]*?(?=\])'
    filtered_captions = []

    for caption in captions:
        matches = re.findall(pattern, caption)

        cleaned_matches = [match.strip() for match in matches]
        
        filtered_captions.extend(cleaned_matches)
    
    return filtered_captions

import re

def fix_and_remove_empty_brackets(input_file, output_file):
    filtered_captions = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines() 

    combined_caption = "" 
    inside_brackets = False

    # Open output file to write cleaned captions
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespaces

            if '[' in line:
                inside_brackets = True
                combined_caption = line 

            elif inside_brackets:
                combined_caption += " " + line  # Append the line to the caption

            # If the line contains a closing bracket ']', finalize the caption
            if ']' in line:
                inside_brackets = False
                combined_caption = combined_caption.replace('[', '').replace(']', '').strip()
                if combined_caption:  # Avoid empty captions
                    filtered_captions.append(f"[{combined_caption}]")
                    f_out.write(f"[{combined_caption}]\n") 
                combined_caption = ""
    f_out.close()
    print(len(filtered_captions))
    return filtered_captions



def regex_comma_separate(captions):
    matches_caption= []
    for caption in captions:
        # Pattern to match names separated by commas
        pattern = r'[^,]+?(?=(?:,| and|$))'

        # Find all matches
        matches = re.findall(pattern, caption)

        matches = [match.strip() for match in matches]
        if not matches[-1]:
            matches.pop()


        print(matches)
        for index, match in enumerate(matches):
            if match.startswith("and"):
                matches[index] = (regex_with_and(matches[index]))

        if len(matches) == 2:
            matches = potential_couple(matches)

        matches_caption.append(matches)

    return matches_caption

def regex_with_and(caption):
    pattern = r'(?<=and\s)(.*)'

    match = re.search(pattern, caption)
    captured_text = match.group(1).strip() if match else None

    return captured_text

def potential_couple(captions):

    if not ' ' in captions[0]:
        match = re.search(r'\s+(.+)', captions[1])

        if match:
            captions[0] = captions[0] + " " + match.group(1)
    return captions

def alone_shared_last_name(caption): #This is only for captions with a single couple in the photo noone else.
    # Remove brackets temporarily for matching, cause it has to be annoying
    caption_no_brackets = caption.strip().strip('[]')

    match = re.match(r'([A-Za-z]+)\s+and\s+([A-Za-z]+)\s+([A-Za-z]+)', caption_no_brackets)
    
    if match:
        first_name = match.group(1)  # First name (e.g., "Kelly")
        second_name = match.group(2)  # Second name (e.g., "Tom")
        last_name = match.group(3)  # Last name (e.g., "Murro")

        expanded_caption = f"{first_name} {last_name} and {second_name} {last_name}"
        
        return f"[{expanded_caption}]"
    
    return caption.strip()

def couples_in_groups_shared_last_name(caption): # This is for captions with couples in the end or in the middle
    caption_no_brackets = caption.strip().strip('[]')

    match = re.search(r'(.*?)(\,|\sand|\swith)\s([A-Za-z\-]+)\s+and\s+([A-Za-z\-]+)\s+([A-Za-z\-]+)', caption_no_brackets)
    
    if match: # Bumped the numbers up by 1 to account for the first group "," or "and"
        first_name = match.group(3) 
        second_name = match.group(4)
        last_name = match.group(5)

        expanded_couple = f"{first_name} {last_name} and {second_name} {last_name}"

        caption_modified = caption_no_brackets.replace(match.group(0), match.group(1) + ", " + expanded_couple)

        return f"[{caption_modified}]"
    
    return caption.strip()




def process_shared_last_names(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        captions = f.readlines()

    with open(output_file, 'w', encoding='utf-8') as f_out:
        for caption in captions:
            processed_caption = couples_in_groups_shared_last_name(caption)
            f_out.write(processed_caption + '\n')
            
def remove_photographers(input_file, output_file):
    pattern = r'[Pp]hoto'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        captions = f.readlines()

    with open(output_file, 'w', encoding='utf-8') as f_out:
        for caption in captions:
            caption_no_brackets = caption.strip().strip('[]')
            match = re.match(pattern, caption_no_brackets)
            if not match:
                f_out.write("[" + caption_no_brackets + "]" + '\n')
                
def remove_titles(input_file, output_file):
    pattern = r'\b(?:Mayor|Lord|Lady|Mr|Mrs|Dr|Sir|Dame|Ms|Miss|General|Captain|Doctor|Father|Mother|Son|Daughter|Professor)\b\.?\s*'
    with open (input_file, 'r', encoding='utf-8') as f:
        captions = f.read()
    
    