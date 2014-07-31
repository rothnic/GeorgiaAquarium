.. docs for ocean voyager exhibit

Ocean Voyager Model
===================

OceanVoyager Component
----------------------
The ocean voyager model component is developed in OpenMDAO, but the calculation functions have been developed as
stand-alone units. The primary OpenMDAO element that would be executed is the OceanVoyagerModel Component,
which is can be loaded by other OpenMDAO structures for automated execution.

*OceanVoyager Class Input Attributes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Energy\Sinks\Exhibits\OceanVoyager\OceanVoyager.py
    :language: python
    :start-after: # set up inputs
    :end-before: # set up outputs

*OceanVoyager Class Output Attributes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Energy\Sinks\Exhibits\OceanVoyager\OceanVoyager.py
    :language: python
    :start-after: # set up outputs
    :end-before: # set up constants

*OceanVoyager Class Constants*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Energy\Sinks\Exhibits\OceanVoyager\OceanVoyager.py
    :language: python
    :start-after: # set up constants
    :end-before: # primary model init

*OceanVoyager Class Definition*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: Energy.Sinks.Exhibits.OceanVoyager.OceanVoyager.OceanVoyagerModel
    :members: __init__,execute
    :show-inheritance:

OceanVoyager Tests
------------------
.. autofunction:: Energy.Sinks.Exhibits.OceanVoyager.test_ocean_voyager.test_ov_openmdao_model