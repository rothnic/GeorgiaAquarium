__author__ = 'Nick'


def get_outputs(component):
    '''
    Retrieves the user-defined outputs from an OpenMDAO component.

    :param component: Initialized OpenMDAO component
    :return: Pure list of only user-defined outputs as strings
    '''

    # Get outputs from component
    my_outputs = component.list_outputs()

    # Defined standard outputs we don't want to see
    standard_outputs = ['derivative_exec_count', 'exec_count', 'itername']

    # Subtract out the standard outputs
    return list(set(my_outputs) - set(standard_outputs))


def print_outputs(component):
    '''
    Prints only the user-defined outputs from an OpenMDAO component

    :param component: Initialized OpenMDAO component
    :return: None, prints to console
    '''

    # Get only the outputs we want to see
    outputs = get_outputs(component)
    print "## Outputs for " + type(component).__name__ + " ##"

    # Print out each output name and value
    for output in outputs:
        print output + ": " + str(getattr(component, output))

    print ""

def get_output_values(component):
    '''
    Retrieves the user-defined outputs form an OpenMDAO component and stores them into a python dict. It could be
    used as followed:

    .. code-block:: python

        comp = MyComponent()
        outputs = get_output_values(comp)
        for output in outputs:
            this_value = outputs[output]
            do_something_with_value(this_value)

    :param component: Initialized OpenMDAO component
    :return: Python dict with keys of the output parameter names, with associated values
    '''

    output_names = get_outputs(component)
    outputs = {}
    for name in output_names:
        outputs[name] = getattr(component, name)
    return outputs

def get_inputs(component):
    '''
    Retrieves the user-defined inputs from an OpenMDAO component as a list of strings. This is required since
    retrieving them directly from the component will include other attributes that were not defined by the user.

    :param component: Initialized OpenMDAO component
    :return: Pure list of only user-defined inputs as strings
    '''

    # Get inputs from component
    my_inputs = component.list_inputs()

    # Defined standard outputs we don't want to see
    standard_inputs = ['directory', 'force_execute', 'force_fd', 'missing_deriv_policy']

    # Subtract out the standard outputs
    return list(set(my_inputs) - set(standard_inputs))

def get_input_values(component):
    '''
    Retrieves the user-defined inputs form an OpenMDAO component and stores them into a python dict. It could be
    used as followed:

    .. code-block:: python

        comp = MyComponent()
        inputs = get_input_values(comp)
        for input in inputs:
            this_value = inputs[input]
            do_something_with_value(this_value)

    :param component: Initialized OpenMDAO component
    :return: Python dict with keys of the input parameter names, with associated values
    '''

    input_names = get_inputs(component)
    inputs = {}
    for name in input_names:
        inputs[name] = getattr(component, name)
    return inputs