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

def get_output_values(component):
    output_names = get_outputs(component)
    outputs = {}
    for name in output_names:
        outputs[name] = getattr(component, name)
    return outputs

def get_inputs(component):
    # Get inputs from component
    my_inputs = component.list_inputs()

    # Defined standard outputs we don't want to see
    standard_inputs = ['directory', 'force_execute', 'force_fd', 'missing_deriv_policy']

    # Subtract out the standard outputs
    return list(set(my_inputs) - set(standard_inputs))

def get_input_values(component):
    input_names = get_inputs(component)
    inputs = {}
    for name in input_names:
        inputs[name] = getattr(component, name)
    return inputs