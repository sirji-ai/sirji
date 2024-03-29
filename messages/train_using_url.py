import textwrap

from base import BaseMessages

class TrainUsingUrlMessage(BaseMessages):

    def template(self):
        return textwrap.dedent("""
          ```
          FROM: {interactor}
          TO: {implementor}
          ACTION: train-using-url
          URL: {url}
          ```
          """)

    def sample(self, interactor):
        return self.generate(interactor, {
            "url": "The URL that needs to be crawled, parsed, and trained to answer questions."
        })

    def description(self):
        return "Train using a URL:"

    @staticmethod
    def properties():
        return ['FROM', 'TO', 'ACTION', 'URL']
