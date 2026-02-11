class PhysiologicalSystem:
    """
    Base class for physiological dynamical system models.

    All models like DallaMan, Hovorka, Bergman will inherit from this.
    """

    def __init__(self, params=None):
        self.params = params or {}
        self.states = {}

    # -----------------------------
    # Parameter handling
    # -----------------------------
    def set_params(self, **kwargs):
        """Update model parameters."""
        self.params.update(kwargs)

    def get_params(self):
        """Return current parameters."""
        return self.params

    # -----------------------------
    # State handling
    # -----------------------------
    def set_states(self, **kwargs):
        """Set internal state variables."""
        self.states.update(kwargs)

    def get_states(self):
        """Return current state variables."""
        return self.states

    # -----------------------------
    # Core simulation method
    # -----------------------------
    def simulate(self, *args, **kwargs):
        raise NotImplementedError(
            "simulate() must be implemented by subclasses."
        )
