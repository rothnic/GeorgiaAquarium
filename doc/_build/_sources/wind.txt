.. wind model documentation

Wind Model
==========

WindModel Component
-------------------
The solar model component is developed in OpenMDAO, but the calculation functions have been developed as stand-alone
units. The primary OpenMDAO element that would be executed is the Solar Model Component,
which is can be loaded by other OpenMDAO structures for automated execution.

Attributes of the component are where the explicit inputs and outputs are defined, and come in the following format::

    attribute_name = attribute_type(default_value, iotype='in/out', desc='description of the attribute')

*WindModel Class Input Attributes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Energy\Sources\Wind\Wind.py
    :language: python
    :start-after: # set up inputs
    :end-before: # set up outputs

*WindModel Class Output Attributes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Energy\Sources\Wind\Wind.py
    :language: python
    :start-after: # set up outputs
    :end-before: # set up constants

*WindModel Class Constants*
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Energy\Sources\Wind\Wind.py
    :language: python
    :start-after: # set up constants
    :end-before: # primary model method

*WindModel Class Definition*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: Energy.Sources.Wind.Wind.WindModel
    :members: execute
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
.. autofunction:: Energy.Sources.Wind.test_wind.test_wind_power_calc
.. autofunction:: Energy.Sources.Wind.test_wind.test_wind_component
.. autofunction:: Energy.Sources.Wind.test_wind.run_print_test
.. autofunction:: Energy.Sources.Wind.test_wind.test_wind_optimization