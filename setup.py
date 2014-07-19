from distutils.core import setup

setup(
    name='GeorgiaAquarium',
    version='0.0.1',
    author='Nick Roth',
    author_email='nroth6@gatech.edu',
    packages=['GeorgiaAquarium',
              'GeorgiaAquarium.Common',
              'GeorgiaAquarium.Common.AttributeTools',
              'GeorgiaAquarium.Common.DecisionTreeSurrogate',
              'GeorgiaAquarium.Common.FfnetSurrogate',
              'GeorgiaAquarium.Common.LhsUncertaintyDriver',
              'GeorgiaAquarium.Common.NeurolabSurrogate',
              'GeorgiaAquarium.Common.RunAggregator',
              'GeorgiaAquarium.Cost',
              'GeorgiaAquarium.Energy',
              'GeorgiaAquarium.Energy.Sinks',
              'GeorgiaAquarium.Energy.Sinks.Exhibits',
              'GeorgiaAquarium.Energy.Sinks.Exhibits.OceanVoyager',
              'GeorgiaAquarium.Energy.Sources',
              'GeorgiaAquarium.Energy.Sources.Grid',
              'GeorgiaAquarium.Energy.Sources.Solar',
              'GeorgiaAquarium.Energy.Sources.Tribo',
              'GeorgiaAquarium.Energy.Sources.Wind',
              'GeorgiaAquarium.Pedestrian',
              'GeorgiaAquarium.Uncertainties'
              ],
    package_data={'': ['*.csv', '*.net', '*.p']
    },
    url='',
    license='LICENSE.txt',
    description='Georgia Aquarium Model',
    long_description=open('GeorgiaAquarium\README.md').read(),
    install_requires=[
        'Ffnet >= 0.7.1',
    ]
)