# Looking for an RDF ontology of the Buddhist key concepts/words/notions

## The problem

The [Buddhist teachings](https://en.wikipedia.org/wiki/Dharma#Buddhism) (Pali: dhamma) are based on (rely on, use a key vocabulary) a core set of key concepts/notion. In the [Theravada school](https://en.wikipedia.org/wiki/Theravada) they are Pali terms. But modern english teachings targeting the layman quite often use english words in place of the Pali terms. Because the mapping between those english terms and the original Pali words is quite loose (for example refer to [Dukkha is A Bummer](https://www.leighb.com/bummer.htm) by Leigh Brasington) we need to point to some, arbitrary yet practical, referential (be it [controlled vocabulary](https://en.wikipedia.org/wiki/Controlled_vocabulary), [lexicon](https://en.wikipedia.org/wiki/Lexicon), [thesaurus](https://en.wikipedia.org/wiki/Thesaurus), [ontology (information science)](https://en.wikipedia.org/wiki/Ontology_(information_science))) of English terms.

The problem boils down to comparing the words/terms [`equanimity`](https://en.wikipedia.org/wiki/Equanimity) (originating in Latin) with [`upekkhā`](https://en.wikipedia.org/wiki/Upek%E1%B9%A3%C4%81) (Pali term) whose respective semantics are probably not aligned. Yet both terms appear at the same entry of the [Wikipedia's glossary of buddhism](https://en.wikipedia.org/wiki/Glossary_of_Buddhism)...

## Non existence of widely-adopted RDF ontology specifically for core Buddhist philosophical concepts

There does not appear to be a comprehensive, widely-adopted RDF ontology specifically for core Buddhist philosophical concepts like anicca, dukkha, anatta, dependent origination...

This absence is actually quite interesting and relates to several challenges:

- Philosophical complexity: Buddhist philosophical concepts are highly contextualized and interpreted differently across traditions (Theravada, Mahayana, Vajrayana, etc.). Terms like "dharma" have multiple meanings depending on context.
- Scholastic diversity: Different Buddhist schools have fundamentally different ontological commitments. For example, the Sarvāstivāda held that dharmas exist in past, present, and future, while Theravada held they only exist in the present.
- The paradox of formalizing emptiness: Creating a rigid ontological structure for concepts like śūnyatā (emptiness) or anattā (non-self) somewhat contradicts the very nature of these teachings, which resist essentialist categorization.

## Current solution

[Wikipedia's glossary of buddhism](https://en.wikipedia.org/wiki/Glossary_of_Buddhism).

Limitation: the glossary itself cannot be referred to with an URL (it has no index). For example, pointing to the term `dharma` within [Wikipedia's glossary of buddhism](https://en.wikipedia.org/wiki/Glossary_of_Buddhism) is not possible. Although that glossary lists the `dharma` term, it simply refers to the [`Dharma` wikipedia page](https://en.wikipedia.org/wiki/Dharma#Buddhism) (that can be referred to). Maybe the convention could be that we only use 

## Informal glossaries

- [Wikipedia's glossary of buddhism](https://en.wikipedia.org/wiki/Glossary_of_Buddhism)

## Dead ends

- The [Buddhist Digital Ontology vocabulary](https://github.com/buda-base/owl-schema) purpose is fundamentally archival and organizational (cataloging and organizing Buddhist texts, manuscripts, and related materials) rather than philosophical.
