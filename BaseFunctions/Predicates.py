# from: https://stackoverflow.com/questions/48491525/implement-query-language-on-python
class Or:
    def __init__(self, *predicates):
        self.predicates = predicates

    def __call__(self, record):
        return any(predicate(record) for predicate in self.predicates)


class And:
    def __init__(self, *predicates):
        self.predicates = predicates

    def __call__(self, record):
        return all(predicate(record) for predicate in self.predicates)

