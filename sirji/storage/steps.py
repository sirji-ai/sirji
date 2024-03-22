# Define a global variable to store the steps array
steps_array = []

# Function to initialize the steps array
def initialize_steps(steps):
    global steps_array
    steps_array = steps

# Function to retrieve the steps array
def get_steps():
    return steps_array