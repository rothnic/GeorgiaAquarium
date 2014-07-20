.. Covers all the aggregating components setup specifically for integrated analysis

Analysis Components
===================

Custom Uncertainties Driver
---------------------------
 This component is used to wrap the model we are trying to optimize, and can be useful when there is little to no data
 that exists on some set of uncertain variables, but it is also a certainty that it is
 not a single finite value. For example, let's say that for some reason we have no access to wind data. Instead of
 choosing a value, we can instead represent the distribution by asking ourselves a series of questions,
 which results in generating a cumulative distribution function (CDF). Afterwards,
 we can use the CDF while optimizing the system design to generate all possible outcomes,
 which then enables us to select the outcome that is most likely to product the best results.

*Uncertainties Component*
^^^^^^^^^^^^^^^^^^^^^^^^^
The Uncertainties Component is the part of the Uncertainties Driver that creates Distributions from stored
user-provided information that best represents the actual distribution.

*Uncertainties Class Input Attributes*
""""""""""""""""""""""""""""""""""""""
.. literalinclude:: ..\Uncertainties\Uncertainties.py
    :language: python
    :start-after: # set up inputs
    :end-before: # set up outputs

*Uncertainties Class Output Attributes*
"""""""""""""""""""""""""""""""""""""""
.. literalinclude:: ..\Uncertainties\Uncertainties.py
    :language: python
    :start-after: # set up outputs
    :end-before: # set up constants

*Uncertainties Class Constants*
"""""""""""""""""""""""""""""""
.. literalinclude:: ..\Uncertainties\Uncertainties.py
    :language: python
    :start-after: # set up constants
    :end-before: # initialization

*Uncertainties Class Definition*
""""""""""""""""""""""""""""""""
.. autoclass:: Uncertainties.Uncertainties.UncertaintiesModel
    :members: __init__,execute,init_distributions
    :show-inheritance:

*Distribution Class*
""""""""""""""""""""
.. autoclass:: Uncertainties.calc_uncertainties.Distribution
    :members: __init__,sample,make_cdf,make_pdf
    :show-inheritance:

*Uncertainties Class Tests*
"""""""""""""""""""""""""""
.. autofunction:: Uncertainties.test_uncertainties.test_uncertainties_component

*Run Aggregator Component*
^^^^^^^^^^^^^^^^^^^^^^^^^^
*Run Aggregator Class Input Attributes*
"""""""""""""""""""""""""""""""""""""""
.. literalinclude:: ..\Common\RunAggregator\RunAggregator.py
    :language: python
    :start-after: # set up inputs
    :end-before: # set up outputs

*Run Aggregator Class Output Attributes*
""""""""""""""""""""""""""""""""""""""""
.. literalinclude:: ..\Common\RunAggregator\RunAggregator.py
    :language: python
    :start-after: # set up outputs
    :end-before: # set up constants

*Run Aggregator Class Constants*
""""""""""""""""""""""""""""""""
.. literalinclude:: ..\Common\RunAggregator\RunAggregator.py
    :language: python
    :start-after: # set up constants
    :end-before: # initialization

*Run Aggregator Class Definition*
"""""""""""""""""""""""""""""""""
.. autoclass:: Common.RunAggregator.RunAggregator.RunAggregator
    :members: __init__,execute
    :show-inheritance:

Georgia Aquarium Model
----------------------
.. automodule:: GeorgiaAquarium
    :members:
    :undoc-members:

Georgia Aquarium Global Optimization
------------------------------------
.. autoclass:: GeorgiaAquariumOptimizer.GeorgiaAquariumGlobalOptimization
    :members:

