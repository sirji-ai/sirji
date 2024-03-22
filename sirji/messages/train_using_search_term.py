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
            "term": "The search term that needs to be crawled and trained on."
        })

    def description(self):
        return "Train using a search term:"

    @staticmethod
    def properties():
        return ['FROM', 'TO', 'ACTION', 'TERM']
