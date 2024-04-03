import sys
import argparse

from sirji_messages import MessageFactory, ActionEnum

def generate_problem_statement_message(problem_statement):
    message = MessageFactory[ActionEnum.PROBLEM_STATEMENT.name]()
    return message.generate({"details": problem_statement})

if __name__ == "__main__":

    # Create the parser
    parser = argparse.ArgumentParser(description='')
    
    # Add arguments
    parser.add_argument('-ps', '--problem_statement', type=str, help='User problem statement', required=True)
    
    # Parse arguments
    args = parser.parse_args()

    response = generate_problem_statement_message(args.problem_statement)

    print(response)

    sys.exit(0)