from docx import Document as Document_
from rdflib import Graph as Graph_, BNode, Namespace, RDFS, Literal
from .Graph import Graph


gbd = Namespace('http://zeio.nara/grabbed')


class Document:
    def __init__(self, path: str):
        self.doc = Document_(path)

    @property
    def graph(self):
        graph = Graph_()

        last_section = None

        for paragraph in self.doc.paragraphs:
            if paragraph.style.style_id in ('1', ):
                last_section_ = BNode()

                if last_section is not None:
                    graph.add((last_section, gbd.nextSection, last_section_))

                graph.add((last_section_, RDFS.label, Literal(paragraph.text)))
                last_section = last_section_
            elif last_section is not None:
                paragraph_node = BNode()

                graph.add((last_section, gbd.hasParagraph, paragraph_node))
                graph.add((paragraph_node, RDFS.label, Literal(paragraph.text)))

        return Graph(graph)
