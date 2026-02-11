import numpy as np
from scipy.integrate import solve_ivp

from .physiological_system import PhysiologicalSystem
from .dallaman_core import (
    dallaman_ode,
    get_default_parameters,
    get_default_initial_state
)
from .result import SimResult


class dallaman(PhysiologicalSystem):

    def __init__(self, params=None):
        default_params = get_default_parameters()

        if params:
            default_params.update(params)

        super().__init__(params=default_params)

    def set(self, **kwargs):
        self.params.update(kwargs)

    def get(self):
        return self.params

    def sim(self, t_span=(0, 600), dt=0.1, meal=78000.0, method="RK45"):

        x0 = get_default_initial_state(meal_size=meal)

        self.states = {"x0": x0}

        t_eval = np.arange(t_span[0], t_span[1] + dt, dt)

        sol = solve_ivp(
            lambda t, x: dallaman_ode(t, x, self.params),
            t_span,
            x0,
            t_eval=t_eval,
            method=method,
            atol=1e-6,
            rtol=1e-6
        )

        return SimResult(sol)
