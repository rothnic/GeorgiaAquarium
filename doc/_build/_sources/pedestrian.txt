.. pedestrian documentation

Pedestrian Model
================

PedestrianModel Component
-------------------------
The pedestrian model component is developed in OpenMDAO, but the calculation functions have been developed as
stand-alone units. In this case much of the actual model exists in an agent-based simulation developed within
AnyLogic, but limitations in capability and time exist for integrating that model directly into the system of
systems model. The primary OpenMDAO element that would be executed is the
:class:`~Pedestrian.Pedestrian.PedestrianModel` Component, which can be loaded by other OpenMDAO structures for
automated execution.

*PedestrianModel Class Input Attributes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Pedestrian\Pedestrian.py
    :language: python
    :start-after: # set up inputs
    :end-before: # set up outputs

*PedestrianModel Class Output Attributes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Pedestrian\Pedestrian.py
    :language: python
    :start-after: # set up outputs
    :end-before: # set up constants

*PedestrianModel Class Constants*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Pedestrian\Pedestrian.py
    :language: python
    :start-after: # set up constants
    :end-before: # primary model method

*PedestrianModel Class Definition*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: Pedestrian.Pedestrian.PedestrianModel
    :members: __init__,execute
    :show-inheritance:

PedSurrogate Class
------------------
.. autoclass:: Pedestrian.calc_ped.PedSurrogate
    :members: __init__,sim
    :show-inheritance:

PedestrianModel Tests
---------------------
.. autofunction:: Pedestrian.test_pedestrian.test_samples
.. autofunction:: Pedestrian.test_pedestrian.run_tests_with_print
