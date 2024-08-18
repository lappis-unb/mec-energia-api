
from sko.PSO import PSO
from sko.GA import GA
from global_search_recommendation.domain import Domain
from global_search_recommendation.recommendation import Recommendation
from tariffs.models import Tariff
from mec_energia.settings import NEW_RESOLUTION_MINIMUM_DEMAND
from abc import ABC

class Runner(ABC):
    def __init__(self, domain: Domain) -> None:
        self.domain = domain
        self.history = domain.consumption_history
        self.p_lbound = max(self.history['peak_measured_demand_in_kw'].min(), NEW_RESOLUTION_MINIMUM_DEMAND)
        self.o_lbound = max(self.history['off_peak_measured_demand_in_kw'].min(), NEW_RESOLUTION_MINIMUM_DEMAND)
        self.p_ubound = max(self.history['peak_measured_demand_in_kw'].max(), self.p_lbound+1)
        self.o_ubound = max(self.history['off_peak_measured_demand_in_kw'].max(), self.o_lbound+1)
        self.g_lb = min(self.p_lbound, self.o_lbound) 
        self.g_ub = max(self.p_ubound, self.o_ubound)
        self.skip_green = self.domain.current_contract.subgroup in ['A2', 'A3']

    def _check_bounds(self, lb: .0, up: .0):
        return up >= lb
    
    @classmethod
    def calculate(self):
        ...
        
class PSORunner(Runner):
    def calculate(self):
        if (self._check_bounds(lb=self.p_lbound, up=self.p_ubound) \
           and self._check_bounds(lb=self.o_lbound, up=self.o_ubound)):
            
            blue = PSO(func=self.domain.blue_objective_func, n_dim=2, pop=40, max_iter=100,
                       w=0.8, c1=0.6, c2=0.6, lb=[self.p_lbound, self.o_lbound], 
                       ub=[self.p_ubound, self.o_ubound])
            blue.run()
        else:
            raise Exception("limites inválidos para computação da recomendação na modalidade azul via PSO")

        if self._check_bounds(lb=self.g_lb, up=self.g_ub):

            if not self.skip_green:
                green = PSO(func=self.domain.green_objective_func, n_dim=1, pop=40, max_iter=100,
                            w=0.8, c1=0.6, c2=0.6, lb=self.g_lb, ub=self.g_ub)
                green.run()
        else:
            raise Exception("limites inválidos para computação da recomendação na modalidade verde via PSO")

        green_best_value = green.gbest_y + round(green.gbest_x[0]) if not self.skip_green else 0
        blue_best_value = blue.gbest_y + round(blue.gbest_x[0]) + round(blue.gbest_x[1])

        if not self.skip_green and green_best_value < blue_best_value:
            return Recommendation(Tariff.GREEN, (0, round(green.gbest_x[0])), self.domain)
        else:
            return Recommendation(Tariff.BLUE, (round(blue.gbest_x[0]), round(blue.gbest_x[1])), self.domain)
        
class GARunner(Runner):
    def calculate(self):
        if self._check_bounds(lb=self.p_lbound, up=self.p_ubound) \
           and self._check_bounds(lb=self.o_lbound, up=self.o_ubound):
            
            blue_ga = GA(func=self.domain.blue_objective_func, n_dim=2, size_pop=40, max_iter=100,
                         prob_mut=0.005, lb=[self.p_lbound, self.o_lbound], ub=[self.p_ubound, self.o_ubound], 
                         early_stop=20, precision=[1,1])
            blue = blue_ga.run()
        else:
            raise Exception("limites inválidos para computação da recomendação na modalidade azul via GA")

        if self._check_bounds(lb=self.g_lb, up=self.g_ub):

            if not self.skip_green:
                green_ga = GA(func=self.domain.green_objective_func, n_dim=1, size_pop=40, max_iter=100, \
                              prob_mut=0.005, lb=[self.g_lb], ub=[self.g_ub], early_stop=20, precision=1)
                green = green_ga.run()
        else:
            raise Exception("limites inválidos para computação da recomendação na modalidade verde via GA")
        
        green_best_value = green[1][0] + round(green[0][0]) if not self.skip_green else 0
        blue_best_value = blue[1][0]+ round(blue[0][0]) + round(blue[0][1])

        if not self.skip_green and green_best_value < blue_best_value:
            return Recommendation(Tariff.GREEN, (0, round(green[0][0])), self.domain)
        else:
            return Recommendation(Tariff.BLUE, (round(blue[0][0]), round(blue[0][1])), self.domain)