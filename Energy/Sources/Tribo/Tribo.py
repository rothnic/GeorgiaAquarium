"""
   /Energy/Sources/Tribo/Tribo.py
"""

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float

from Common.AttributeTools.io import print_outputs
from calc_tribo import calc_cost, calc_power


class TriboModel(Component):
    # set up inputs
    tileCount = Float(5.0, iotype='in', desc='number of tiles')
    pedStepsPerTile = Float(50.0, iotype='in', desc='expected steps per tile')
    tileEff = Float(0.9, iotype='in', desc='tribo efficiency (percent)')
    tileUnitCost = Float(800.0, iotype='in', desc='unit cost of a single tile')
    mgtTileUnitCost = Float(800.0, iotype='in', desc='unit cost of a management tile')
    tilekWh = Float(0.002, iotype='in', desc='power produced per step (kWh)')

    # set up outputs
    totalkWh = Float(1.0, iotype='out', desc='yearly power output (kWh)')
    triboCapitalCost = Float(1.0, iotype='out', desc='investment cost ($)')


    def execute(self):
        # Calculate power
        self.totalkWh = calc_power(
            self.tileCount,
            self.pedStepsPerTile,
            self.tileEff,
            self.tilekWh)

        # Calculate cost
        self.triboCapitalCost = calc_cost(
            self.tileUnitCost,
            self.tileCount,
            self.mgtTileUnitCost)


def run_tests():
    comp = TriboModel()
    comp.execute()
    print_outputs(comp)


if __name__ == "__main__":
    # Module test routine, executes when this python file is ran independently
    # For example, using Pycharm, right click while editing and select Run
    run_tests()