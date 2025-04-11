# bsky-feed-db

Python feeds for IACC community based on [https://github.com/MarshalX/bluesky-feed-generator](https://github.com/MarshalX/bluesky-feed-generator) with separate script for firehose handling.

## IACC Following

[https://bsky.app/profile/iaccsky-updates.bsky.social/feed/iacc-following](https://bsky.app/profile/iaccsky-updates.bsky.social/feed/iacc-following)

**Logic:** Posts including any of these keywords from people you follow:

```
['#cfs/me', '#cfsme', '#dysautonomia', '#fibro', '#fibromyalgia', '#iacc', '#iaccs', '#longcovid', '#longcovidkids', '#lyme', '#mcas', '#me/cfs', '#mecfs', '#myalgice', '#myalgicencephalomyelitis', '#neisvoid', '#pots', '#pwlc', '#pwme', '#severeme', '#thereforme', '#verysevereme', 'able-bodied', 'abled', 'autoimmune', 'brain fog', 'brainfog', 'cfs', 'cfs/me', 'cfsme', 'chiari', 'chronic fatigue', 'chronic illness', 'chronic pain', 'chronically ill', 'chronicillness', 'chronicpain', 'disability', 'disabled', 'disease', 'diseases', 'dysautonomia', 'eds', 'ehlers danlos', 'ehlers-danlos', 'endometriosis', 'energy limit', 'energy limiting', 'energy limits', 'energy-limiting', 'epstein barr', 'fibro', 'fibromyalgia', 'gastroparesis', 'hypermobile', 'hypermobility', 'iacc', 'iaccs', 'immune', 'immunocompromise', 'immunocompromised', 'infection associated', 'infection-associated', 'infection-associated chronic', 'inflammation', 'insomnia', 'joint pain', 'lc symptom', 'lc symptoms', 'long covid', 'longcovid', 'longcovidkids', 'lyme', 'mast cell', 'mcas', 'me symptom', 'me symptoms', 'me/cfs', 'mecfs', 'migraine', 'mild me', 'mild me/cfs', 'mild mecfs', 'moderate me', 'moderate me/cfs', 'moderate mecfs', 'muscle pain', 'myalgic encephalomyelitis', 'myalgice', 'myalgicencephalomyelitis', 'neisvoid', 'neurological', 'neuropathy', 'onset', 'pace trial', 'pacing', 'pem', 'post exertion', 'post exertional', 'post viral', 'post-exertional', 'post-viral illness', 'post-viral illnesses', 'pots', 'pwlc', 'pwme', 'severe me', 'severe me/cfs', 'severe mecfs', 'severeme', 'tethered cord', 'thereforme', 'verysevereme', 'viral illness']
```

## IACC Discover

[https://bsky.app/profile/iaccsky-updates.bsky.social/feed/iacc-discover](https://bsky.app/profile/iaccsky-updates.bsky.social/feed/iacc-discover)

**Logic:** Posts including any of these keywords from people you do NOT follow:

````
['#cfs/me', '#cfsme', '#dysautonomia', '#fibro', '#fibromyalgia', '#iacc', '#iaccs', '#longcovid', '#longcovidkids', '#lyme', '#mcas', '#me/cfs', '#mecfs', '#myalgice', '#myalgicencephalomyelitis', '#neisvoid', '#pots', '#pwlc', '#pwme', '#severeme', '#thereforme', '#verysevereme']
````

## IACC Links

[https://bsky.app/profile/iaccsky-updates.bsky.social/feed/iacc-links](https://bsky.app/profile/iaccsky-updates.bsky.social/feed/iacc-links)

**Logic:** Posts from people you follow including any of these keywords **AND** containing a link:

````
['#cfs/me', '#cfsme', '#dysautonomia', '#fibro', '#fibromyalgia', '#iacc', '#iaccs', '#longcovid', '#longcovidkids', '#lyme', '#mcas', '#me/cfs', '#mecfs', '#myalgice', '#myalgicencephalomyelitis', '#neisvoid', '#pots', '#pwlc', '#pwme', '#severeme', '#thereforme', '#verysevereme', 'able-bodied', 'abled', 'autoimmune', 'brain fog', 'brainfog', 'cdc', 'cfs', 'cfs/me', 'cfsme', 'chiari', 'chronic fatigue', 'chronic illness', 'chronic pain', 'chronically ill', 'chronicillness', 'chronicpain', 'covid', 'covid-19', 'disability', 'disabled', 'disease', 'diseases', 'dna', 'dysautonomia', 'ebv', 'eds', 'ehlers danlos', 'ehlers-danlos', 'endometriosis', 'energy limit', 'energy limiting', 'energy limits', 'energy-limiting', 'epstein barr', 'fatigue', 'fibro', 'fibromyalgia', 'flu', 'gastroparesis', 'genes', 'genetic', 'genomic', 'headache', 'hhs', 'hypermobile', 'hypermobility', 'iacc', 'iaccs', 'immune', 'immunocompromise', 'immunocompromised', 'infection', 'infection associated', 'infection-associated', 'infection-associated chronic', 'inflammation', 'influenza', 'insomnia', 'joint pain', 'lab', 'labs', 'lc symptom', 'lc symptoms', 'long covid', 'longcovid', 'longcovidkids', 'lyme', 'mast cell', 'mcas', 'me symptom', 'me symptoms', 'me/cfs', 'mecfs', 'migraine', 'mild me', 'mild me/cfs', 'mild mecfs', 'mitochondria', 'moderate me', 'moderate me/cfs', 'moderate mecfs', 'muscle pain', 'myalgic encephalomyelitis', 'myalgice', 'myalgicencephalomyelitis', 'neisvoid', 'neurological', 'neuropathy', 'nih', 'onset', 'pace trial', 'pacing', 'pem', 'post exertion', 'post exertional', 'post viral', 'post-exertional', 'post-viral illness', 'post-viral illnesses', 'pots', 'protein', 'pwlc', 'pwme', 'research', 'rna', 'sars-cov-2', 'severe me', 'severe me/cfs', 'severe mecfs', 'severeme', 'tethered cord', 'thereforme', 'verysevereme', 'viral illness', 'virus', 'viruses']
````

**OR** posts from people you do NOT follow including any of these keywords **AND** containing a link:

````
['#cfs/me', '#cfsme', '#dysautonomia', '#fibro', '#fibromyalgia', '#iacc', '#iaccs', '#longcovid', '#longcovidkids', '#lyme', '#mcas', '#me/cfs', '#mecfs', '#myalgice', '#myalgicencephalomyelitis', '#neisvoid', '#pots', '#pwlc', '#pwme', '#severeme', '#thereforme', '#verysevereme']
````

## IACC Mutual Aid

[https://bsky.app/profile/iaccsky-updates.bsky.social/feed/iacc-ma](https://bsky.app/profile/iaccsky-updates.bsky.social/feed/iacc-ma)

**Logic:** Posts from people who have added themselves to the feed including any of these keywords:

````
['#cfs/me', '#cfsme', '#dysautonomia', '#fibro', '#fibromyalgia', '#iacc', '#iaccs', '#longcovid', '#longcovidkids', '#lyme', '#mcas', '#me/cfs', '#mecfs', '#myalgice', '#myalgicencephalomyelitis', '#neisvoid', '#pots', '#pwlc', '#pwme', '#severeme', '#thereforme', '#verysevereme', 'able-bodied', 'abled', 'autoimmune', 'bill', 'bills', 'brain fog', 'brainfog', 'cash', 'cashapp', 'cfs', 'cfs/me', 'cfsme', 'chiari', 'chronic fatigue', 'chronic illness', 'chronic pain', 'chronically ill', 'chronicillness', 'chronicpain', 'disability', 'disabled', 'disease', 'diseases', 'donate', 'donation', 'dysautonomia', 'eds', 'ehlers danlos', 'ehlers-danlos', 'endometriosis', 'energy limit', 'energy limiting', 'energy limits', 'energy-limiting', 'epstein barr', 'fibro', 'fibromyalgia', 'fundraise', 'fundraiser', 'fundraising', 'gastroparesis', 'gofundme', 'helpsky', 'hypermobile', 'hypermobility', 'iacc', 'iaccs', 'immune', 'immunocompromise', 'immunocompromised', 'infection associated', 'infection-associated', 'infection-associated chronic', 'inflammation', 'insomnia', 'joint pain', 'lc symptom', 'lc symptoms', 'long covid', 'longcovid', 'longcovidkids', 'lyme', 'mast cell', 'mcas', 'me symptom', 'me symptoms', 'me/cfs', 'mecfs', 'migraine', 'mild me', 'mild me/cfs', 'mild mecfs', 'moderate me', 'moderate me/cfs', 'moderate mecfs', 'muscle pain', 'mutual aid', 'mutualaid', 'myalgic encephalomyelitis', 'myalgice', 'myalgicencephalomyelitis', 'neisvoid', 'neurological', 'neuropathy', 'onset', 'pace trial', 'pacing', 'paypal', 'pem', 'post exertion', 'post exertional', 'post viral', 'post-exertional', 'post-viral illness', 'post-viral illnesses', 'pots', 'pwlc', 'pwme', 'rent', 'severe me', 'severe me/cfs', 'severe mecfs', 'severeme', 'tethered cord', 'thereforme', 'venmo', 'verysevereme', 'viral illness']
````

For your posts to appear on this feed, post or reply "@iaccsky-updates.bsky.social AddToMutualAid" without the quotes and you should get an automatic notification within a few minutes that you are added. To remove yourself from this feed so your posts will no longer appear, post or reply "@iaccsky-updates.bsky.social RemoveFromMutualAid" without the quotes.

## IACC United Kingdom

[https://bsky.app/profile/iaccsky-updates.bsky.social/feed/iacc-unitedkingdom](https://bsky.app/profile/iaccsky-updates.bsky.social/feed/iacc-unitedkingdom)

**Logic:** Posts from people who have added themselves to the feed including any of these keywords:

````
['#cfs/me', '#cfsme', '#dysautonomia', '#fibro', '#fibromyalgia', '#iacc', '#iaccs', '#longcovid', '#longcovidkids', '#lyme', '#mcas', '#me/cfs', '#mecfs', '#myalgice', '#myalgicencephalomyelitis', '#neisvoid', '#pots', '#pwlc', '#pwme', '#severeme', '#thereforme', '#verysevereme', 'able-bodied', 'abled', 'autoimmune', 'brain fog', 'brainfog', 'cfs', 'cfs/me', 'cfsme', 'chiari', 'chronic fatigue', 'chronic illness', 'chronic pain', 'chronically ill', 'chronicillness', 'chronicpain', 'disability', 'disabled', 'disease', 'diseases', 'dysautonomia', 'eds', 'ehlers danlos', 'ehlers-danlos', 'endometriosis', 'energy limit', 'energy limiting', 'energy limits', 'energy-limiting', 'epstein barr', 'fibro', 'fibromyalgia', 'gastroparesis', 'hypermobile', 'hypermobility', 'iacc', 'iaccs', 'immune', 'immunocompromise', 'immunocompromised', 'infection associated', 'infection-associated', 'infection-associated chronic', 'inflammation', 'insomnia', 'joint pain', 'lc symptom', 'lc symptoms', 'long covid', 'longcovid', 'longcovidkids', 'lyme', 'mast cell', 'mcas', 'me symptom', 'me symptoms', 'me/cfs', 'mecfs', 'migraine', 'mild me', 'mild me/cfs', 'mild mecfs', 'moderate me', 'moderate me/cfs', 'moderate mecfs', 'muscle pain', 'myalgic encephalomyelitis', 'myalgice', 'myalgicencephalomyelitis', 'neisvoid', 'neurological', 'neuropathy', 'onset', 'pace trial', 'pacing', 'pem', 'post exertion', 'post exertional', 'post viral', 'post-exertional', 'post-viral illness', 'post-viral illnesses', 'pots', 'pwlc', 'pwme', 'severe me', 'severe me/cfs', 'severe mecfs', 'severeme', 'tethered cord', 'thereforme', 'verysevereme', 'viral illness']
````

For your posts to appear on this feed, post or reply "@iaccsky-updates.bsky.social AddToUnitedKingdom" without the quotes and you should get an automatic notification within a few minutes that you are added. To remove yourself from this feed so your posts will no longer appear, post or reply "@iaccsky-updates.bsky.social RemoveFromUnitedKingdom" without the quotes.

## IACC Secret Lists

[https://bsky.app/profile/iaccsky-updates.bsky.social/feed/iacc-secret](https://bsky.app/profile/iaccsky-updates.bsky.social/feed/iacc-secret)

**Logic:** Posts about anything from people on your secret list, if you have one. To set up a secret list, follow [these instructions](https://bsky.app/profile/iaccsky-updates.bsky.social/post/3lkozm675ws2h).
