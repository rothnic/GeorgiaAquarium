.. Documentation for all model components, excluding aggregations

Solar Model
===========

SolarModel Component
--------------------
The solar model component is developed in OpenMDAO, but the calculation functions have been developed as stand-alone
units. The primary OpenMDAO element that would be executed is the Solar Model Component,
which is can be loaded by other OpenMDAO structures for automated execution.

*SolarModel Class Input Attributes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Energy\Sources\Solar\Solar.py
    :start-after: # set up inputs
    :end-before: # set up outputs

*SolarModel Class Output Attributes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Energy\Sources\Solar\Solar.py
    :start-after: # set up outputs
    :end-before: # set up constants

*SolarModel Class Definition*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: Energy.Sources.Solar.Solar.SolarModel
    :members:
    :undoc-members:
    :private-members:
    :show-inheritance:

SolarModel Calculations
-----------------------

.. autofunction:: Energy.Sources.Solar.calc_solar.calc_power
.. autofunction:: Energy.Sources.Solar.calc_solar.calc_power_fast
.. autofunction:: Energy.Sources.Solar.calc_solar.calc_cost
.. autofunction:: Energy.Sources.Solar.calc_solar.calc_num_panels

SolarModel Optimization
-----------------------
An OpenMDAO assembly, configured to use a pyOpt optimization driver, and configured with parameters corresponding to
the :class:`~Energy.Sources.Solar.Solar.SolarModel` inputs. This can be used for testing the model before integration
with other models.

.. autoclass:: Energy.Sources.Solar.Solar.SolarOptimization
    :members:
    :undoc-members:
    :private-members:
    :show-inheritance:

SolarModel Tests
----------------
.. autofunction:: Energy.Sources.Solar.test_solar.testSolarClean
.. autofunction:: Energy.Sources.Solar.test_solar.testSolarComp
.. autofunction:: Energy.Sources.Solar.test_solar.test_solar_non_neg
.. autofunction:: Energy.Sources.Solar.test_solar.test_solar_optimization
.. autofunction:: Energy.Sources.Solar.test_solar.run_print_test
