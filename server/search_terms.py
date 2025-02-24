KEYWORDS = [
    "me/cfs",
    "mecfs",
    "mcas",
    "pots",
    "myalgice",
    "myalgicencephalomyelitis",
    "fibro",
    "fibromyalgia",
    "neisvoid",
    "dysautonomia",
    "longcovid",
    "iacc",
    "iaccs",
    "pem",
    "pwme",
    "pwlc",
    "eds",
    "ehlers-danlos",
    "cfsme",
    "cfs/me",
    "endometriosis",
]

HASHTAG_KEYWORDS = ['#' + word for word in KEYWORDS]

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
    text_words = [word.lower() for word in record.text.split()]
    text_bigrams = [text_words[i] + ' ' + text_words[i+1] for i in range(len(text_words) - 1)]

    return any(keyword in text_words for keyword in KEYWORDS + HASHTAG_KEYWORDS) or any(bigram in text_bigrams for bigram in BIGRAMS)