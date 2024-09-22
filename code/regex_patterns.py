import re

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

    # Find the match
    match = re.search(pattern, caption)
    captured_text = match.group(1).strip() if match else None

    return captured_text

def potential_couple(captions):

    if not ' ' in captions[0]:
        match = re.search(r'\s+(.+)', captions[1])

        if match:
            captions[0] = captions[0] + " " + match.group(1)
    return captions