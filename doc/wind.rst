.. wind model documentation

Wind Model
==========

WindModel Component
-------------------
The solar model component is developed in OpenMDAO, but the calculation functions have been developed as stand-alone
units. The primary OpenMDAO element that would be executed is the Solar Model Component,
which is can be loaded by other OpenMDAO structures for automated execution.

*WindModel Class Input Attributes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Energy\Sources\Wind\Wind.py
    :start-after: # set up inputs
    :end-before: # set up outputs

*WindModel Class Output Attributes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Energy\Sources\Wind\Wind.py
    :start-after: # set up outputs
    :end-before: # set up constants

*WindModel Class Definition*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: Energy.Sources.Wind.Wind.WindModel
    :members:
    :undoc-members:
    :private-members:
    :show-inheritance:

WindModel Calculations
----------------------

.. autofunction:: Energy.Sources.Wind.calc_wind.calc_power
.. autofunction:: Energy.Sources.Wind.calc_wind.calc_power_fast
.. autofunction:: Energy.Sources.Wind.calc_wind.calc_cost

WindModel Optimization
----------------------
An OpenMDAO assembly, configured to use a pyOpt optimization driver, and configured with parameters corresponding to
the :class:`~Energy.Sources.Wind.Wind.WindModel` inputs. This can be used for testing the model before integration
with other models.

.. autoclass:: Energy.Sources.Wind.Wind.WindOptimization
    :members:
    :undoc-members:
    :private-members:
    :show-inheritance:

WindModel Tests
---------------
