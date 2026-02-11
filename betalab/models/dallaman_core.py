"""
dallaman_core.py

Core physiological implementation of the Dalla Man glucose–insulin model.

This file contains:
- The ODE system
- Default parameter set
- Default initial state vector

This is the pure science layer.
No simulation logic, plotting, or APIs here.
"""

import numpy as np


# ============================================================
# Default Parameters
# ============================================================

def get_default_parameters():
    return dict(
        V_G=1.88,
        k_1=0.065,
        k_2=0.079,
        G_b=95.0,
        V_I=0.05,
        m_1=0.19,
        m_2=0.484,
        m_4=0.194,
        m_5=0.0304,
        m_6=0.6471,
        HE_b=0.6,
        I_b=25.0,
        S_b=1.8,
        S_b_minus=-1.8,
        k_max=0.0558,
        k_min=0.008,
        k_abs=0.057,
        k_gri=0.0558,
        f=0.9,
        b=0.82,
        d=0.01,
        BW=78.0,
        k_p1=2.7,
        k_p2=0.0021,
        k_p3=0.009,
        k_p4=0.0618,
        k_i=0.0079,
        U_ii=1.0,
        V_m0=2.5,
        V_mX=0.047,
        K_m0=225.59,
        p_2U=0.0331,
        part=0.2,
        K=2.3,
        alpha=0.05,
        beta=0.11,
        gamma=0.5,
        k_e1=5.0e-4,
        k_e2=339.0,
        D=78000.0
    )


# ============================================================
# Default Initial State
# ============================================================

def get_default_initial_state(meal_size=78000.0):
    """
    Returns the default 12-state initial vector.
    """
    return np.array([
        178.0,   # Gp
        135.0,   # Gt
        4.5,     # Il
        1.25,    # Ip
        meal_size,  # Q_sto1
        0.0,     # Q_sto2
        0.0,     # Q_gut
        25.0,    # I1
        25.0,    # Id
        0.0,     # X
        3.6,     # I_po
        0.0      # Y
    ])


# ============================================================
# ODE System
# ============================================================

def dallaman_ode(t, x, p):
    """
    Core Dalla Man model dynamics.

    State vector:
    [Gp, Gt, Il, Ip, Qsto1, Qsto2, Qgut, I1, Id, X, I_po, Y]
    """

    Gp, Gt, Il, Ip, Q_sto1, Q_sto2, Q_gut, I1, Id, X, I_po, Y = x

    # Unpack parameters
    V_G = p['V_G']
    k_1 = p['k_1']
    k_2 = p['k_2']
    G_b = p['G_b']
    V_I = p['V_I']
    m_1 = p['m_1']
    m_2 = p['m_2']
    m_4 = p['m_4']
    m_5 = p['m_5']
    m_6 = p['m_6']
    HE_b = p['HE_b']
    I_b = p['I_b']
    S_b = p['S_b']
    k_max = p['k_max']
    k_min = p['k_min']
    k_abs = p['k_abs']
    k_gri = p['k_gri']
    f = p['f']
    b = p['b']
    d = p['d']
    BW = p['BW']
    k_p1 = p['k_p1']
    k_p2 = p['k_p2']
    k_p3 = p['k_p3']
    k_p4 = p['k_p4']
    k_i = p['k_i']
    U_ii = p['U_ii']
    V_m0 = p['V_m0']
    V_mX = p['V_mX']
    K_m0 = p['K_m0']
    p_2U = p['p_2U']
    part = p['part']
    K = p['K']
    alpha = p['alpha']
    beta = p['beta']
    gamma = p['gamma']
    D = p['D']

    aa = 5/2/(1 - b) / D
    cc = 5/2 / d / D

    # --- Derived quantities ---

    EGP = k_p1 - k_p2 * Gp - k_p3 * Id - k_p4 * I_po

    V_mmax = (1 - part) * (V_m0 + V_mX * X)
    U_idm = V_mmax * Gt / (K_m0 + Gt) if (K_m0 + Gt) != 0 else 0.0

    E = 0.0
    S = gamma * I_po
    I = Ip / V_I if V_I != 0 else 0.0
    G = Gp / V_G if V_G != 0 else 0.0

    HE = (-m_5) * S + m_6
    if abs(1 - HE) < 1e-8:
        m_3 = m_1 * 1e6
    else:
        m_3 = HE * m_1 / (1 - HE)

    Q_sto = Q_sto1 + Q_sto2
    Ra = f * k_abs * Q_gut / BW

    k_empt = k_min + (k_max - k_min) / 2.0 * (
        np.tanh(aa * (Q_sto - b * D)) - np.tanh(cc * (Q_sto - d * D)) + 2.0
    )

    U_id = U_idm
    U = U_ii + U_id

    S_po = Y + K * (EGP + Ra - E - U_ii - k_1 * Gp + k_2 * Gt) / V_G + S_b

    # --- ODEs ---

    dGp = EGP + Ra - E - U_ii - k_1 * Gp + k_2 * Gt
    dGt = -U_id + k_1 * Gp - k_2 * Gt
    dIl = (-m_1) * Il - m_3 * Il + m_2 * Ip + S
    dIp = (-m_2) * Ip - m_4 * Ip + m_1 * Il
    dQsto1 = -k_gri * Q_sto1
    dQsto2 = -k_empt * Q_sto2 + k_gri * Q_sto1
    dQgut = -k_abs * Q_gut + k_empt * Q_sto2
    dI1 = -k_i * (I1 - I)
    dId = -k_i * (Id - I1)
    dX = -p_2U * X + p_2U * (I - I_b)
    dIpo = -gamma * I_po + S_po
    dY = -alpha * (Y - beta * (G - G_b))

    return np.array([dGp, dGt, dIl, dIp, dQsto1, dQsto2, dQgut, dI1, dId, dX, dIpo, dY])
