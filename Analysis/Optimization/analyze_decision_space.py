__author__ = 'Nick'

from GeorgiaAquariumOptimizer import GeorgiaAquariumOptimization
from openmdao.main.api import Assembly

breakEvenYears = range(1, 16)
initialInvestments = range(200000, 1000000, 110000)


if __name__ == '__main__':
    # for year in breakEvenYears:
    #     gao = GeorgiaAquariumOptimization(year, 400000, 'breakeven'+str(year))
    #     gao.run()

    for inv in initialInvestments:
        gao = GeorgiaAquariumOptimization(3, inv, 'investment'+str(inv))
        gao.run()
