from random import seed as seed_, random

from rdflib import Graph as Graph_
from pykeen.triples import CoreTriplesFactory


def encode(obj, obj_to_id: dict, id_to_obj: dict, next_id: int):
    if (id_ := obj_to_id.get(obj)) is not None:
        return id_, next_id

    obj_to_id[obj] = next_id
    id_to_obj[next_id] = obj

    return next_id, next_id + 1


class Graph:
    def __init__(self, graph: Graph_, train: float = 0.8, test: float = 0.5, seed: int = 17):
        entity_to_id = {}
        id_to_entity = {}
        next_entity_id = 0

        relation_to_id = {}
        id_to_relation = {}
        next_relation_id = 0

        train_triples = []
        test_triples = []
        dev_triples = []

        seed_(seed)

        for h, r, t in graph:
            h_id, next_entity_id = encode(h, entity_to_id, id_to_entity, next_entity_id)
            r_id, next_relation_id = encode(r, relation_to_id, id_to_relation, next_relation_id)
            t_id, next_entity_id = encode(t, entity_to_id, id_to_entity, next_entity_id)

            if random() <= train:
                train_triples.append((h_id, r_id, t_id))
            elif random() <= test:
                test_triples.append((h_id, r_id, t_id))
            else:
                dev_triples.append((h_id, r_id, t_id))

        self.train = CoreTriplesFactory.create(mapped_triples = train_triples, num_entities = next_entity_id, num_relations = next_relation_id)
        self.test = CoreTriplesFactory.create(mapped_triples = test_triples, num_entities = next_entity_id, num_relations = next_relation_id)
        self.dev = CoreTriplesFactory.create(mapped_triples = dev_triples, num_entities = next_entity_id, num_relations = next_relation_id)
