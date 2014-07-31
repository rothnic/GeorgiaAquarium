.. lighting model docs

Lighting Model
==============

Reusable LightingModel Component
--------------------------------
The LightingModel component is an OpenMDAO component, which could be used by multiple exhibits to help determine
their individual lighting configuration. The LightingModel uses a :class:`~Common.Lighting.calc_lighting.Lights` class
to configure both a nominal and new design lighting configuration, then perform calculations based on the
configurations.

*LightingModel Class Input Attributes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Common\Lighting\Lighting.py
    :language: python
    :start-after: # set up inputs
    :end-before: # set up outputs

*LightingModel Class Output Attributes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Common\Lighting\Lighting.py
    :language: python
    :start-after: # set up outputs
    :end-before: # set up constants

*LightingModel Class Constants*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Common\Lighting\Lighting.py
    :language: python
    :start-after: # set up constants
    :end-before: # initialization

*LightingModel Class Definition*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: Common.Lighting.Lighting.LightingModel
    :members: __init__,execute

*Lights Class*
~~~~~~~~~~~~~~
.. autoclass:: Common.Lighting.calc_lighting.Lights
    :members: __init__,initial_cost,recurring_cost,recurrance_period,yearly_cost,power_per_year,print_config

Lighting Tests
--------------

.. autofunction:: Common.Lighting.test_lighting.setup_tests
.. autofunction:: Common.Lighting.test_lighting.test_lights_initial
.. autofunction:: Common.Lighting.test_lighting.test_lights_power_year
.. autofunction:: Common.Lighting.test_lighting.test_lights_recurrance
.. autofunction:: Common.Lighting.test_lighting.test_lights_cost
.. autofunction:: Common.Lighting.test_lighting.test_lighting_model
.. autofunction:: Common.Lighting.test_lighting.test_lights_yearly_cost
