from string import punctuation

punc = ''.join([elem for elem in punctuation if elem != '#'])


KEYWORDS = [
    'cfs/me',
    'cfsme', 
    'dysautonomia', 
    'fibro', 
    'fibromyalgia', 
    'iacc', 
    'iaccs', 
    'longcovid', 
    'longcovidkids',
    'lyme',
    'mcas', 
    'me/cfs', 
    'mecfs', 
    'myalgice', 
    'myalgicencephalomyelitis', 
    'neisvoid', 
    'pots', 
    'pwlc', 
    'pwme', 
    'thereforme',
]

HASHTAG_KEYWORDS = ['#' + word for word in KEYWORDS]

EXPANDED_KEYWORDS = [
    'able-bodied', 
    'abled', 
    'autoimmune', 
    'brainfog', 
    'cfs', 
    'chiari', 
    'chronicillness', 
    'chronicpain',
    'disability', 
    'disabled', 
    'disease', 
    'diseases', 
    'eds', 
    'ehlers-danlos', 
    'endometriosis', 
    'energy', 
    'gastroparesis', 
    'hypermobile', 
    'hypermobility', 
    'immune', 
    'immunocompromise', 
    'immunocompromised', 
    'infection-associated',
    'inflammation', 
    'insomnia', 
    'migraine', 
    'neurological', 
    'neuropathy', 
    'onset', 
    'pem',
    'post-exertional',
]

HASHTAG_EXPANDED_KEYWORDS = ['#' + word for word in KEYWORDS]

BIGRAMS = [
    'brain fog', 
    'chronic fatigue', 
    'chronic illness', 
    'chronic pain', 
    'ehlers danlos', 
    'epstein barr', 
    'infection associated', 
    'infection-associated chronic', 
    'joint pain', 
    'long covid', 
    'mast cell', 
    'mild me', 
    'mild me/cfs', 
    'mild mecfs', 
    'moderate me', 
    'moderate me/cfs', 
    'moderate mecfs', 
    'muscle pain', 
    'myalgic encephalomyelitis', 
    'post exertion', 
    'post exertional', 
    'severe me', 
    'severe me/cfs', 
    'severe mecfs', 
    'tethered cord']

LINK_TERMS = [
    #'blood', 
    'cdc', 
    'covid', 
    'covid-19', 
    'dna', 
    'ebv', 
    'fatigue', 
    'flu', 
    'gene', 
    'headache', 
    'hhs', 
    'infection', 
    'influenza', 
    'lab', 
    'labs', 
    'mitochondria', 
    'nih', 
    'protein', 
    'research', 
    'rna', 
    'sars-cov-2', 
    'sleep', 
    'virus', 
    'viruses'
]

SUBFEED_TERMS = {
    'mutualaid': {
        'terms': ['bill', 'bills', 'cash', 'cashapp', 'donate', 'donation', 'helpsky', 'fundraise', 'fundraiser', 'fundraising', 'gofundme', 'mutualaid', 'paypal', 'rent', 'venmo'],
        'bigrams': ['mutual aid'],
    }
}


def post_contains_any(record):
    text_words = [word.lower().strip(punc) for word in record.text.split()]
    text_bigrams = [text_words[i] + ' ' + text_words[i+1] for i in range(len(text_words) - 1)]

    if any(keyword in text_words for keyword in HASHTAG_KEYWORDS):
        return True, True

    return any(keyword in text_words for keyword in KEYWORDS + EXPANDED_KEYWORDS + HASHTAG_EXPANDED_KEYWORDS) or any(bigram in text_bigrams for bigram in BIGRAMS), False


def post_contains_link_term(record):
    text_words = [word.lower().strip(punc) for word in record.text.split()]
    return any(keyword in text_words for keyword in LINK_TERMS)


def post_contains_subfeed_term(record, subfeed_name):
    if subfeed_name not in SUBFEED_TERMS:
        return False
    text_words = [word.lower().strip(punctuation) for word in record.text.split()]
    text_bigrams = [text_words[i] + ' ' + text_words[i+1] for i in range(len(text_words) - 1)]

    return any(keyword in text_words for keyword in SUBFEED_TERMS[subfeed_name]['terms']) or any(bigram in text_bigrams for bigram in SUBFEED_TERMS[subfeed_name]['bigrams'])
