.. tribo documentaiton

Triboelectric Model
===================

Triboelectric Component
-----------------------

*TriboModel Class Input Attributes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Energy\Sources\Tribo\Tribo.py
    :language: python
    :start-after: # set up inputs
    :end-before: # set up outputs

*TriboModel Class Output Attributes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Energy\Sources\Tribo\Tribo.py
    :language: python
    :start-after: # set up outputs
    :end-before: # set up constants

*TriboModel Class Constants*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ..\Energy\Sources\Tribo\Tribo.py
    :language: python
    :start-after: # set up constants
    :end-before: # primary model method

*TriboModel Class Definition*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: Energy.Sources.Tribo.Tribo.TriboModel
    :members: execute
    :show-inheritance:

TriboModel Calculations
-----------------------
.. autofunction:: Energy.Sources.Tribo.calc_tribo.calc_power
.. autofunction:: Energy.Sources.Tribo.calc_tribo.calc_cost

TriboModel Optimization
-----------------------
.. autoclass:: Energy.Sources.Tribo.Tribo.TriboOptimization
    :members:
    :undoc-members:
    :private-members:
    :show-inheritance:

TriboModel Tests
----------------
.. autofunction:: Energy.Sources.Tribo.test_tribo.test_tribo_openmdao_model
.. autofunction:: Energy.Sources.Tribo.test_tribo.test_tribo_optimization