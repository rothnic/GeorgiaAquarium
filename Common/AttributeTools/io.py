__author__ = 'Nick'


def get_outputs(component):
    # Get outputs from component
    my_outputs = component.list_outputs()

    # Defined standard outputs we don't want to see
    standard_outputs = ['derivative_exec_count', 'exec_count', 'itername']

    # Subtract out the standard outputs
    return list(set(my_outputs) - set(standard_outputs))


def print_outputs(component):
    # Get only the outputs we want to see
    outputs = get_outputs(component)
    print "## Outputs for " + type(component).__name__ + " ##"

    # Print out each output name and value
    for output in outputs:
        print output + ": " + str(getattr(component, output))

    print ""