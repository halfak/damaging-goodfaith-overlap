"""
Scores a set of revisions

Usage:
    score_revisions (-h|--help)
    score_revisions <ores-host> <context> <model>...
                    [--debug]
                    [--verbose]

Options:
    -h --help    Prints this documentation
    <ores-host>  The host name for an ORES instance to use in scoring
    <context>    The name of the wiki to execute model(s) for
    <model>      The name of a model to use in scoring
"""
import json
import logging
import sys

import docopt
from ores import api

logger = logging.getLogger(__name__)


def main():
    args = docopt.docopt(__doc__)

    logging.basicConfig(
        level=logging.INFO if not args['--debug'] else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

    ores_host = args['<ores-host>']
    context = args['<context>']
    model_names = args['<model>']
    verbose = args['--verbose']

    rev_docs = [json.loads(l) for l in sys.stdin]

    run(ores_host, context, model_names, rev_docs, verbose)


def run(ores_host, context, model_names, rev_docs, verbose):
    session = api.Session(ores_host, user_agent="ahalfaker@wikimedia.org")

    rev_ids = [d['rev_id'] for d in rev_docs]
    scores = session.score(context, model_names, rev_ids)

    for rev_doc, score_doc in zip(rev_docs, scores):
        rev_doc['score'] = score_doc
        json.dump(rev_doc, sys.stdout)
        sys.stdout.write("\n")
        if verbose:
            sys.stderr.write(".")
            sys.stderr.flush()


if __name__ == "__main__":
    main()
