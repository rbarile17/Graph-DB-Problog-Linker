# -*- coding: utf-8 -*-
## @package Data
# Implements class for Data representation
# @author Pasquale De Marinis, Barile Roberto, Caputo Sergio
from collections import defaultdict
from problog.program import SimpleProgram
from problog.logic import Constant, Var, Term, AnnotatedDisjunction

##
# Implements class for Data representation
from src.Distribution import Distribution, Normal, Multinomial


class Data:

    ## The constructor
    # @param: triples: list of subject - predicate - object tuples
    # @param: length: number of tuples in triples
    def __init__(self, triples, length):
        self.__triples = triples
        self.__length = length
        self.__property_types = None

    ## doc
    #
    def set_property_types(self, property_types):
        self.__property_types = property_types

    ## Set the triples of Data object
    # @param: triples: list of subject - predicate - object tuples
    def set_triples(self, triples):
        self.__triples = triples

    def get_triples(self):
        return self.__triples

    def learn_distributions(self):
        distributions = defaultdict(dict)
        distribution = Distribution()
        normal = Normal()
        multinomial = Multinomial()

        for prop, value in self.__triples:
            if prop in distributions.keys():
                distribution.add(value)
                distributions[prop] = distribution
            else:
                if prop in self.__property_types.keys():
                    distributions[prop] = self.__property_types[prop]()
                    distributions[prop].add(value)
                else:
                    if type(value) is float:
                        normal.add(value)
                        distributions[prop] = normal
                    else:
                        multinomial.add(value)
                        distributions[prop] = multinomial

        return distributions

        # usare property types per capire che distribuziona apprendere per la proprietà
        # se non c'è nel map, usare di default discrete se è una stringa o un intero e normal se è un double

        # da completare, costruire lista di property (CON DISTRIBUZIONE)

    def parse(self):
        ###Modifica commento succesivo
        """Parse a list of triples/quadruples into a SimpleProgram"""
        program = SimpleProgram()
        term_dict = dict()
        const_dict = dict()
        for triple in self.__data:
            if term_dict.get(triple[1]) is None:
                term_dict[triple[1]] = Term(triple[1])
            if const_dict.get(triple[0]) is None:
                const_dict[triple[0]] = Constant(triple[0])
            if const_dict.get(triple[2]) is None:
                const_dict[triple[2]] = Constant(triple[2])
            pred = term_dict.get(triple[1])
            c1 = const_dict[triple[0]]
            c2 = const_dict[triple[2]]
            program += pred(c1, c2)

            return program


class PropertyList:

    def __init__(self, properties):
        self.__properties = properties

    def to_simple_program(self):
        program = SimpleProgram()
        for property in self.__properties:
            pass


class Property:

    def __init__(self, name, distribution, property_type):
        self.__name = name
        self.__distribution = distribution
        self.__property_type = property_type

    def to_atom(self):
        pass
        # to implement
