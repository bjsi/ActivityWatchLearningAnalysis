import spacy

from UnitAnalysis.SuperMemo.ElementContent import remove_references

nlp = spacy.load("en_core_web_sm")


def get_entities(x: str):
    doc = nlp(remove_references(x))
    return ", ".join(ent.text for ent in doc.ents)


if __name__ == '__main__':
    pass
