.. common components documentation

Common Utilities
================

Surrogate Model Tools
---------------------

*Decision Tree Surrogate*
~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: Common.DecisionTreeSurrogate.DecisionTreeSurrogate.DecisionTreeSurrogate
    :members: __init__,test,train,sim,print_sim

*Neural Network (Ffnet) Surrogate*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: Common.FfnetSurrogate.FfnetSurrogate.FfnetSurrogate
    :members: __init__,test,train,sim,save,load,print_sim

*Neural Network (Neurolab) Surrogate*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: Common.NeurolabSurrogate.NeurolabSurrogate.NeurolabSurrogate
    :members: __init__,create_norm_func,test,train,sim,print_sim

Helper Utilities
----------------
.. automodule:: Common.AttributeTools.io
    :members: get_outputs, print_outputs, get_output_values, get_inputs, get_input_values

