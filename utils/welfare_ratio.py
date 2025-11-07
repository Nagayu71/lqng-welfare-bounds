import numpy as np
from .matrix_utils import *

__all__ = [
    "mu",
    "eigenvalues_PinvN",
    "candidate_welfare_values",
]


def mu(attenuation: float, alpha: np.ndarray) -> np.ndarray:
    """
    The function mu(attenuation, alpha) = (1 - 2 * attenuation * alpha) / (1 - attenuation * alpha)^2.

    Args:
        attenuation (float): Strength of the network effects
        alpha (np.ndarray): Eigenvalues of the adjacency matrix A

    Returns:
        np.ndarray: Computed values of mu(attenuation, alpha)
    """
    return (1 - 2 * attenuation * alpha) / (1 - attenuation * alpha) ** 2


def eigenvalues_PinvN(attenuation: float, alpha: np.ndarray) -> np.ndarray:
    """
    Compute the eigenvalues of the matrix P_inv * N for a simple graph with adjacency matrix A.

    Args:
        attenuation (float): Strength of the network effects
        alpha (np.ndarray): Eigenvalues of the adjacency matrix A

    Raises:
        ValueError: if the inputs are not real numbers or do not satisfy the spectral condition.

    Returns:
        np.ndarray: Eigenvalues of the matrix P_inv * N
    """
    if not are_all_real(alpha):
        raise ValueError("The inputs must be real numbers.")
    if not satisfies_spectral_condition(attenuation, alpha):
        raise ValueError("The inputs do not satisfy the spectral condition.")
    return (1 - 2 * attenuation * alpha) / (1 - attenuation * alpha) ** 2


def candidate_welfare_values(attenuation: float, eigenvalues: dict) -> dict:
    mu = {}
    for name, eigs in eigenvalues.items():
        try:
            mu[name] = eigenvalues_PinvN(attenuation, eigs)
        except Exception as e:
            print(f"Error with {name}: {e}")
            mu[name] = None
    return mu
