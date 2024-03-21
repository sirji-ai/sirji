import textwrap

from sirji.messages.base import BaseMessages


class TrainUsingSearchTermMessage(BaseMessages):

    def template(self):
        return textwrap.dedent("""
          ```
          FROM: {interactor}
          TO: {implementor}
          ACTION: train-using-search-term
          TERM: {term}
          ```
          """)

    def sample(self, interactor):
        return self.generate(interactor, {
            "term": "The search term that needs to be searched on a search engine and use the first few URLs to be crawled, parsed, and trained to answer questions."
        })

    def description(self):
        return "Train RA on a search term:"

    @staticmethod
    def properties():
        return ['FROM', 'TO', 'ACTION', 'TERM']
