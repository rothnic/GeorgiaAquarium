.. cost model documentation

Cost Model
==========

CostModel Component
-------------------
The Cost Model developed as an OpenMDAO component, which defines inputs, outputs, and calls calculation functions.

*CostModel Class Input Attributes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Cost\Cost.py
    :language: python
    :start-after: # set up inputs
    :end-before: # set up outputs

*CostModel Class Output Attributes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Cost\Cost.py
    :language: python
    :start-after: # set up outputs
    :end-before: # set up constants

*CostModel Class Constants*
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Cost\Cost.py
    :language: python
    :start-after: # set up constants
    :end-before: # primary model method

*CostModel Class Definition*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: Cost.Cost.CostModel
    :members: execute
    :show-inheritance:

CostModel Calculations
----------------------
.. autofunction:: Cost.calc_cost.total_energy_produced
.. autofunction:: Cost.calc_cost.total_energy_consumed
.. autofunction:: Cost.calc_cost.total_energy_cost
.. autofunction:: Cost.calc_cost.original_energy_cost
.. autofunction:: Cost.calc_cost.total_energy_saved
.. autofunction:: Cost.calc_cost.calc_roi
.. autofunction:: Cost.calc_cost.get_break_even
.. autofunction:: Cost.calc_cost.total_capital_cost
.. autofunction:: Cost.calc_cost.total_utility

CostModel Tests
---------------
.. autofunction:: Cost.test_cost.test_model_with_print
.. autofunction:: Cost.test_cost.test_roi
.. autofunction:: Cost.test_cost.test_break_even
.. autofunction:: Cost.test_cost.test_cost_component