# Need: Formalize Knowledge Graphs by using RDF and OWL

As the [Demystifying Knowledge Graphs: a deep dive into RDF and beyond](https://medium.com/@tarekhaled/demystifying-knowledge-graphs-a-deep-dive-into-rdf-and-beyond-55bdcf093d65) states it

> Knowledge Graphs (KGs as opposed to RDBMSs) prioritize flexibility, semantic richness, and domain-specific relevance:
>
> - **Flexibility**: KGs accommodating diverse and evolving data structures by not rigidly separating the schema from the data, allowing for dynamic modeling and representation.
> - **Explicit/[Formal semantics](https://en.wikipedia.org/wiki/Semantics_(logic))**: KG's flexibility raises the need for explicit formalism (schema-like components, such as ontologies, providing well-defined meanings for relationships and entities) to guide their construction and maintain logical consistency through embedding explicit (rich and deep) semantics.
> - **Domain relevance**: KGs must serve its intended application domain purpose which we can assert by enforcing some domain specific ontologies while rejecting others.

A direct consequence if the need for enforcing the usage of

- [RDF](Database/Readme.md)
- [OWL](https://en.wikipedia.org/wiki/Web_Ontology_Language) (Web Ontology Language)

## References and strings to read

- Finish the [Practical Guide to Building OWL Ontologies - Using Protégé 5.5 and Plugins](https://drive.google.com/file/d/1A3Y8T6nIfXQ_UQOpCAr_HFSCwpTqELeP/view) tutorial by Michael DeBellis (Edition 3.2, 2021)
- Are they reasons for adopting OWL instead of the simpler (SKOS Simple Knowledge Organisation System) ? Side questions
  - SKOS is expressed in RDF and thus no need new tools beyond the ones used for the individuals (OWL terminology). Are they python libraries and tools for OWL ? (Protégé, ...) Read the [combined usage OF SKOS and OWL](https://medium.com/@nfigay/combined-usage-of-skos-and-owl-an-experimentation-on-the-digital-europa-thesaurus-41ae9d488512) article again ?
  - Do we need reasoning ? Should we use [OWLAPY](https://github.com/dice-group/owlapy), the `The Python Framework for Modern Ontology Engineering and Knowledge Graph Development`
