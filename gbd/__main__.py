from click import group, argument, option
from pykeen.pipeline import pipeline
from pathlib import Path

from .Document import Document


@group()
def main():
    pass


@main.command()
@argument('path', type = str, default = 'assets/student.docx')
@option('--epochs', '-e', type = int, default = 100)
@option('--dim', '-d', type = int, default = 100)
@option('--seed', '-s', type = int, default = 17)
def grab(path: str, epochs: int, dim: int, seed: int):
    # 1. Parse document

    doc = Document(path)

    # 2. Generate graph

    graph = doc.graph

    # 3. Train graph embeddings

    model = pipeline(
        training = graph.train,
        testing = graph.test,
        validation = graph.dev,
        model = 'TransE',
        training_kwargs = {
            'num_epochs': epochs
        },
        model_kwargs = {
            'embedding_dim': dim
        },
        random_seed = seed
    )

    # 4. Save the result

    model.save_to_directory(
        Path(path).with_suffix('.model')
    )


if __name__ == '__main__':
    main()
