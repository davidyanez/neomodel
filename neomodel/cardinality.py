from .relationship_manager import RelationshipManager, ZeroOrMore # noqa


class ZeroOrOne(RelationshipManager):
    """
    A relationship to zero or one node
    """
    description = "zero or one relationship"

    def single(self):
        nodes = super(ZeroOrOne, self).all()
        if len(nodes) == 1:
            return nodes[0]
        if len(nodes) > 1:
            raise CardinalityViolation(self, len(nodes))

    def all(self):
        node = self.single()
        return [node] if node else []

    def connect(self, obj, properties=None):
        if len(self):
            raise AttemptedCardinalityViolation(
                    "Node already has {0} can't connect more".format(self))
        else:
            return super(ZeroOrOne, self).connect(obj, properties)


class OneOrMore(RelationshipManager):
    """
    A relationship to zero or more nodes
    """
    description = "one or more relationships"

    def single(self):
        nodes = super(OneOrMore, self).all()
        if nodes:
            return nodes[0]
        raise CardinalityViolation(self, 'none')

    def all(self):
        nodes = super(OneOrMore, self).all()
        if nodes:
            return nodes
        raise CardinalityViolation(self, 'none')

    def disconnect(self, obj):
        if super(OneOrMore, self).__len__() < 2:
            raise AttemptedCardinalityViolation("One or more expected")
        return super(OneOrMore, self).disconnect(obj)


class One(RelationshipManager):
    """
    A relationship to a single node
    """
    description = "one relationship"

    def single(self):
        nodes = super(One, self).all()
        if nodes:
            if len(nodes) == 1:
                return nodes[0]
            else:
                raise CardinalityViolation(self, len(nodes))
        else:
            raise CardinalityViolation(self, 'none')

    def all(self):
        return [self.single()]

    def disconnect(self, obj):
        raise AttemptedCardinalityViolation("Cardinality one, cannot disconnect use reconnect")

    def connect(self, obj, properties=None):
        if not hasattr(self.source, 'id'):
            raise ValueError("Node has not been saved cannot connect!")
        if len(self):
            raise AttemptedCardinalityViolation("Node already has one relationship")
        else:
            return super(One, self).connect(obj, properties)


class AttemptedCardinalityViolation(Exception):
    pass


class CardinalityViolation(Exception):
    def __init__(self, rel_manager, actual):
        self.rel_manager = str(rel_manager)
        self.actual = str(actual)

    def __str__(self):
        return "CardinalityViolation: Expected {0} got {1}".format(self.rel_manager, self.actual)
