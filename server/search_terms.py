from string import punctuation
from server.database import session, Feed
import sqlalchemy

punc = ''.join([elem for elem in punctuation if elem != '#'])


KEYWORDS = [
    "me/cfs",
    "mecfs",
    "mcas",
    "pots",
    "myalgice",
    "myalgicencephalomyelitis",
    "fibro",
    "fibromyalgia",
    "dysautonomia",
    "longcovid",
    "iacc",
    "iaccs",
    "pwme",
    "pwlc",
    "cfsme",
    "cfs/me",
    "neisvoid",
]

HASHTAG_KEYWORDS = ['#' + word for word in KEYWORDS]

EXPANDED_KEYWORDS = [
    "endometriosis",
    "chronicillness",
    "eds",
    "pem",
    "ehlers-danlos",
    "hypermobile",
    "hypermobility",
    "brainfog",
    "migraine",
    #"pain",
    #"headache",
    "insomnia",
    "immune",
    "immunocompromise",
    "immunocompromised",
    "cfs",
    "chiari",
]

HASHTAG_EXPANDED_KEYWORDS = ['#' + word for word in KEYWORDS]

BIGRAMS = [
    "myalgic encephalomyelitis,"
    "long covid",
    "mild me",
    "mild me/cfs",
    "mild mecfs",
    "moderate me",
    "moderate me/cfs",
    "moderate mecfs",
    "severe me",
    "severe me/cfs",
    "severe mecfs",
    "mast cell",
    "chronic fatigue",
    "infection-associated chronic",
    "infection associated",
    "chronic illness",
    "brain fog",
    "ehlers danlos",
    "joint pain",
    "muscle pain",
    "chronic pain",
    "tethered cord",
    "epstein barr",
]

LINK_TERMS = [
    "nih",
    "cdc",
    "fatigue",
    #"pain",
    "sleep",
    "headache",
    "mitochondria",
    "blood",
    "dna",
    "rna",
    "protein",
    "gene",
    "infection",
    "covid",
    "flu",
    "influenza",
    "ebv",
]

'''
SUBFEED_NAMES = [
    'Test1',
    'Test2'
]
'''

SUBFEED_CMDS = {
    '#IaccAddTo': 'add',
    '#IaccRemoveFrom': 'remove',
}

stmt = sqlalchemy.select(Feed)
SUBFEED_NAMES = {row.feed_name: row.id for row in session.scalars(stmt).all()}


SUBFEED_CMD_DICT = {''.join([cmd, subfeed_name]).lower(): (action, subfeed_name) for subfeed_name in SUBFEED_NAMES for cmd, action in SUBFEED_CMDS.items()}

print(SUBFEED_CMD_DICT)

def post_contains_any(record):
    text_words = [word.lower().strip(punc) for word in record.text.split()]
    text_bigrams = [text_words[i] + ' ' + text_words[i+1] for i in range(len(text_words) - 1)]

    if any(keyword in text_words for keyword in HASHTAG_KEYWORDS):
        return True, True

    return any(keyword in text_words for keyword in KEYWORDS + EXPANDED_KEYWORDS + HASHTAG_EXPANDED_KEYWORDS) or any(bigram in text_bigrams for bigram in BIGRAMS), False

    #return any(keyword in text_words for keyword in KEYWORDS + HASHTAG_KEYWORDS) or any(bigram in text_bigrams for bigram in BIGRAMS)

def post_contains_link_term(record):
    text_words = [word.lower().strip(punc) for word in record.text.split()]
    return any(keyword in text_words for keyword in LINK_TERMS)


def post_contains_feed_cmd(record):
    text_words = list(set([word.lower().strip(punc) for word in record.text.split()]))

    #if any(cmd in text_words for cmd in SUBFEED_CMD_DICT):
    #    cmd, action = SUBFEED_CMD_DICT
    #    return True, 

    words_in_cmds_dict = [SUBFEED_CMD_DICT[word] for word in text_words if word in SUBFEED_CMD_DICT]

    cmds = {}

    for action, subfeed_name in words_in_cmds_dict:

        if action not in cmds:
            cmds[action] = []

        cmds[action].append(SUBFEED_NAMES[subfeed_name])

    #if len(words_in_cmds_dict) > 1:
    #    raise ValueError

    return cmds