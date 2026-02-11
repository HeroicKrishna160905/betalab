import matplotlib.pyplot as plt


class SimResult:
    """
    Minimal simulation result wrapper.

    Gives direct access to key states + plotting.
    """

    def __init__(self, sol):
        self._sol = sol

        self.t = sol.t
        self.Gp = sol.y[0, :]
        self.Gt = sol.y[1, :]
        self.Ip = sol.y[3, :]
        self.Ipo = sol.y[10, :]

    def plot(self, var=None, title=None):
        """
        Plot simulation results.

        Parameters
        ----------
        var : str or None
            If None -> plot default glucose + insulin panels
            If provided -> plot specific variable (e.g., "Gp", "Ip")

        title : str or None
            Optional title for the figure (useful for experiments)
        """

        # Default plot (glucose + insulin)
        if var is None:
            plt.figure(figsize=(10, 6))

            if title:
                plt.suptitle(title)

            plt.subplot(2, 1, 1)
            plt.plot(self.t, self.Gp, label="Gp")
            plt.plot(self.t, self.Gt, label="Gt")
            plt.ylabel("Glucose")
            plt.legend()
            plt.grid(True)

            plt.subplot(2, 1, 2)
            plt.plot(self.t, self.Ip, label="Ip")
            plt.plot(self.t, self.Ipo, label="Ipo")
            plt.xlabel("Time (min)")
            plt.ylabel("Insulin")
            plt.legend()
            plt.grid(True)

            plt.tight_layout()
            plt.show()
            return

        # Plot specific variable
        if hasattr(self, var):
            plt.figure()

            if title:
                plt.title(title)
            else:
                plt.title(var)

            plt.plot(self.t, getattr(self, var))
            plt.grid(True)
            plt.show()
