"""
This script generates Chung–Lu random graphs (nx.expected_degree_graph)
from the observed degree sequence of a given network G.
It computes the full adjacency spectrum (all eigenvalues) for each sampled graph
and saves them together with metadata and the degree sequence.
"""

import json
from datetime import datetime
from typing import Tuple
import numpy as np
import networkx as nx

__all__ = [
    "sample_chunglu_spectra",
]


def degrees_from_graph(G: nx.Graph) -> np.ndarray:
    """Extract degree sequence (as float array) from the observed graph G."""
    return np.array([d for _, d in G.degree()], dtype=float)


def adjacency_spectrum_full(G: nx.Graph) -> np.ndarray:
    """
    Compute the full adjacency spectrum of graph G.
    This returns all eigenvalues (real, sorted).
    Complexity: O(n^3), but acceptable for small / medium graphs.
    """
    # Convert adjacency matrix to dense array
    A = nx.to_scipy_sparse_array(G, dtype=float, format="csr")
    A_dense = A.toarray()
    evals = np.linalg.eigvalsh(A_dense)  # symmetric eigenvalue solver
    return np.sort(evals)


def sample_expected_degree_graph(
    w: np.ndarray, selfloops: bool, rng: np.random.Generator
) -> nx.Graph:
    """
    Generate one Chung–Lu random graph from expected degree sequence w.
    - selfloops: whether to allow self-loops
    - rng: numpy Generator for reproducibility
    """
    seed = int(rng.integers(0, 2**32 - 1))
    Gs = nx.expected_degree_graph(w, selfloops=selfloops, seed=seed)
    # Relabel nodes to integers (0..n-1) for consistency
    return nx.convert_node_labels_to_integers(Gs, ordering="sorted")


def sample_chunglu_spectra(
    G: nx.Graph,
    sample_size: int = 10000,
    selfloops: bool = False,
    seed: int = 42,
    outfile: str = None,
) -> Tuple[np.ndarray, dict]:
    """
    Main routine:
    - Generate num_samples Chung–Lu random graphs
    - Compute the full adjacency spectrum (ascending order) for each graph
    - Save results to NPZ file
    """
    rng = np.random.default_rng(seed)
    w = degrees_from_graph(G)
    n = G.number_of_nodes()

    spectra_list = []

    for _ in range(sample_size):
        G_sampled = sample_expected_degree_graph(w, selfloops=selfloops, rng=rng)
        evals = adjacency_spectrum_full(G_sampled)
        spectra_list.append(evals.astype(np.float64))

    spectra = np.vstack(spectra_list)  # shape: (sample_size, #nodes)

    meta = {
        "model": "Chung-Lu (nx.expected_degree_graph)",
        "selfloops": selfloops,
        "sample_size": sample_size,
        "n": int(n),
        "m_observed": int(G.number_of_edges()),
        "mode": "full",
        "seed": seed,
        "datetime": datetime.now().isoformat(timespec="seconds"),
        "networkx_version": nx.__version__,
        "numpy_version": np.__version__,
    }

    # Save spectra, degree sequence, and metadata
    np.savez_compressed(
        outfile,
        spectra=spectra,
        degrees=w.astype(np.float64),
        meta=json.dumps(meta, ensure_ascii=False),
    )

    return spectra, meta
