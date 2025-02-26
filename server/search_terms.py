from string import punctuation

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
    "neisvoid",
    "brainfog",
    "migraine",
    "pain",
    "headache",
    "insomnia",
    "immune",
    "immunocompromise",
    "immunocompromised",
    "cfs",
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
]

def post_contains_any(record):
    text_words = [word.lower().strip(punc) for word in record.text.split()]
    text_bigrams = [text_words[i] + ' ' + text_words[i+1] for i in range(len(text_words) - 1)]

    if any(keyword in text_words for keyword in HASHTAG_KEYWORDS):
        return True, True

    return any(keyword in text_words for keyword in KEYWORDS + EXPANDED_KEYWORDS + HASHTAG_EXPANDED_KEYWORDS) or any(bigram in text_bigrams for bigram in BIGRAMS), False

    #return any(keyword in text_words for keyword in KEYWORDS + HASHTAG_KEYWORDS) or any(bigram in text_bigrams for bigram in BIGRAMS)
