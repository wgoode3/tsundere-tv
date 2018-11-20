import re

CRC32_HASH = re.compile('^[0-9A-F]{8}$')


def unbracket(path):
    """ 
    splits up the filename 
    """
    path = path.split( "/" )[-1]

    brackets = []
    parenthesis = []
    rest_of_name = ''
    paren = False
    bracket = False

    for letter in path:
        if letter == '(':
            paren = True
            parenthesis.append( '' )
        elif letter == ')':
            paren = False
        elif letter == '[':
            bracket = True
            brackets.append( '' )
        elif letter == ']':
            bracket = False
        elif paren:
            parenthesis[-1] += letter
        elif bracket:
            brackets[-1] += letter
        elif letter == "_":
            rest_of_name += " "
        else:
            rest_of_name += letter

    # TODO: investigate how this works with more filenames
    # this can do weird things if the path has many "." in it
    return brackets, parenthesis, rest_of_name.split( "." )[0]


def parse_filename( file ):
    """ 
    parses filename to determine information about the file 
    """

    d = {}

    """ 
    determines the fansub group 
    """
    if file.startswith( "[" ) and file.find( "]" ) > 0:
        d['fansub_group'] = file[1:file.find("]")]

    """ 
    removes underscores 
    """
    file = file.replace( "_", " " )

    """ 
    filters out text inside of brackets and parenthesis 
    """
    b, p, r = unbracket( file )

    """ 
    finds the CRC32 hash value 
    """
    for val in reversed(p + b):
        if CRC32_HASH.match(val):
            d['crc32_hash'] = val
            break

    """ 
    checks for season 
    """
    season = re.findall("((1st|2nd|3rd|4th|5th|first|second|third|forth|fifth)\ season)|(s\d)|(season\ \d)", file, flags=re.IGNORECASE)
    if len(season) > 0:
        season = max(season[0], key=len)
        r = r.replace(season, '')
        d['season'] = season

    episode = ''

    """ 
    checks if it is an op or an ed 
    """
    op_ed = re.findall("(\ op|\ ed|\ ncop|\ nced|\ OP|\ ED|\ NCOP|\ NCED)[\ ]?(\d+)?", r)
    op_ed = [''.join(o for o in op).strip() for op in op_ed]
    if len(op_ed) > 0:
        episode = max(op_ed, key=len)

    """ 
    checks if it is an ova or oad 
    """
    if len(episode) < 1:
        ova = re.findall("(\ \d+\ |\ \d+\ -\ )?(\ ova|\ oad|\ ona|\ OVA|\ OAD|\ ONA)(\ \d+|\ -\ \d+)?", r)
        ova = [''.join(o for o in ov).strip() for ov in ova]
        if len(ova) > 0:
            episode = max(ova, key=len)

    """ 
    checks if it is a special 
    """
    if len(episode) < 1:
        special = re.findall("(\ sp\ |\ special\ )(\d+|-\ \d+)?", r, flags=re.IGNORECASE)
        special = [''.join(s for s in sp).strip() for sp in special]
        if len(special) > 0:
            episode = max(special, key=len)

    """ 
    finds the episode number if it isn't an op/ed, ova/oad, or a special  
    """
    if len(episode) < 1:
        episode = re.findall( r'(episode\ \d+|ep\d+|e\d+|\ \d+)(\.\d)?(v\d+)?', r, flags=re.IGNORECASE ) 
        episode = [''.join(e for e in ep).strip() for ep in episode]
        if len(episode) == 1:
            episode = episode[0]
        elif len(episode) < 1:
            episode = None
        else:
            # I am assuming that if there is more than one number the last is probably the episode
            # works for 2 out of 2 of my real world test cases
            episode = episode[-1]
    
    # by now we know what the episode is or we know nothing
    d['episode_number'] = episode

    """ 
    removes some things from the rest of the string 
    """
    if episode is not None:
        r = r.split(episode)[0]
    else:
        print("EPISODE NOT FOUND: {}".format(path))
        d['episode_number'] = "???"

    r = r.split(" - ")[0]
    to_remove = ("BD", "bd", "Blu-ray", "blu-ray", "Bluray", "bluray", "TV", "tv")
    for thing in to_remove:
        if thing in r:
            r = r.replace(thing, "")

    d['anime_name'] = r.strip()

    return d