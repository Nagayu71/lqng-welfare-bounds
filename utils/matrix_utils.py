import numpy as np
import networkx as nx

__all__ = [
    "is_full_rank",
    "are_all_real",
    "satisfies_spectral_condition",
    "zero_tolerance",
    "network_stats",
]


def is_full_rank(A: np.ndarray, hermitian: bool = True) -> bool:
    return np.linalg.matrix_rank(A, hermitian=hermitian) == A.shape[0]


def are_all_real(arr: np.ndarray) -> np.bool:
    """
    Check if all elements in the array are real numbers.
    """
    return np.all(np.isreal(arr))


def satisfies_spectral_condition(
    attenuation: float, eigenvalues: np.ndarray
) -> np.bool:
    """
    Check if the spectral condition r(phi A) < 1/2 is satisfied for the eigenvalues of the adjacency matrix A.
    """
    return np.all(np.abs(attenuation * eigenvalues) < 0.5)


def zero_tolerance(A: np.ndarray) -> float:
    """
    Return a tolerance for deciding if eigenvalues of matrix A are zero
    """
    n = A.shape[0]
    eps = np.finfo(A.dtype).eps  # machine epsilon for the given dtype
    normA = np.linalg.norm(A, ord=2)  # spectral norm (largest singular value)
    return n * normA * eps


def network_stats(G: nx.Graph) -> dict:
    n = G.number_of_nodes()
    m = G.number_of_edges()
    degrees = [d for n, d in G.degree()]
    avg_deg = np.mean(degrees)
    max_deg = np.max(degrees)
    min_deg = np.min(degrees)
    density = nx.density(G)
    clustering = nx.average_clustering(G)
    if nx.is_connected(G):
        diameter = nx.diameter(G)
    else:
        diameter = float("inf")
    return {
        "Nodes": n,
        "Edges": m,
        "density": density,
        "<k>": avg_deg,
        "k_max": max_deg,
        "k_min": min_deg,
        "diameter": diameter,
        "clustering": clustering,
    }
