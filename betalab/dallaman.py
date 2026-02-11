"""
dallaman.py

Ultra-minimal research interface for the Dalla Man glucose–insulin model.

Usage:
    from betalab.models.dallaman import dallaman

    m = dallaman()
    m.set(BW=70)

    sol = m.sim()
    sol.plot()
"""

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
    """
    Minimal Dalla Man model wrapper.

    Clean research API:
        m = dallaman()
        m.set(...)
        sol = m.sim()
        sol.plot()
    """

    def __init__(self, params=None):
        default_params = get_default_parameters()

        if params:
            default_params.update(params)

        super().__init__(params=default_params)

    # -------------------------
    # Minimal parameter API
    # -------------------------
    def set(self, **kwargs):
        """Update model parameters."""
        self.params.update(kwargs)

    def get(self):
        """Return current parameters."""
        return self.params

    # -------------------------
    # Simulation
    # -------------------------
    def sim(self, t_span=(0, 600), dt=0.1, meal=78000.0, method="RK45"):
        """
        Run simulation.

        Parameters
        ----------
        t_span : tuple
            (start, end) time in minutes

        dt : float
            time step

        meal : float
            glucose amount (controls Q_sto1 initial state)

        method : str
            ODE solver
        """

        # initial state
        x0 = get_default_initial_state(meal_size=meal)

        # store initial state for transparency
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
