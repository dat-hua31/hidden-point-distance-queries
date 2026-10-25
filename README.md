# Finding a Hidden Point from Distance Queries

An algorithmic implementation and formal mathematical repository exploring the problem of locating a uniformly random hidden point $P_s$ inside an arbitrary compact planar region $S \subset \mathbb{R}^2$ using only Euclidean distance queries ($\vert{}\vert{}P - P_s\vert{}\vert{}$).

---

## 📜 Overview

Given a compact set $S \subset \mathbb{R}^2$ with positive area and a uniformly distributed hidden point $P_s \in S$, an adaptive query strategy selects points $P_1, P_2, \dots \in S$ and receives their Euclidean distances to $P_s$. The strategy succeeds at step $k$ if $P_k = P_s$.

This repository contains both the formal mathematical proof and a modular Python framework demonstrating that **three queries always suffice**, while **two queries succeed with probability zero**.

---

## 📐 Theoretical Results

**Theorem 1.** For every compact set $S \subset \mathbb{R}^2$ with positive area:

1. **Upper Bound:** There exists an adaptive strategy that finds $P_s$ in at most **3 queries** for every $P_s \in S$.
2. **Lower Bound:** Every strategy finds $P_s$ within **2 queries with probability 0**.

Hence, the exact minimum number of queries required in the worst case is **3**.

---

## 🗂️ Repository Architecture

```text
├── formal.pdf          # Complete formal mathematical paper & proofs
├── note.md             # Concise markdown breakdown of lemmas & cases
├── query.py            # Core distance query engine, mirror pair math, & reduction logic
├── shape.py            # Planar shape definitions, convex hull ($H$), & boundary analysis
├── strategies.py       # Implementation of Case A (segments) & Case B (smooth boundaries)
└── experiments.py      # Numerical validation & simulation scripts

```

---

## 🔍 Core Algorithmic Strategies

### 1. The Mirror Pair Reduction

After two queries $P_1$ and $P_2$, the possible candidate locations for $P_s$ are restricted to a mirror pair $\{P_s, \sigma(P_s)\}$ across the line $\ell$ passing through $P_1$ and $P_2$. The third query resolves this ambiguity unless $\sigma(P_s) \in S$ and $\sigma(P_s) \neq P_s$.

### 2. Case A: Boundary Contains a Segment

If the boundary of the convex hull $\partial H$ contains a non-degenerate segment $[A, B]$, we choose $P_1 = A$ and $P_2 = B$. Because $\ell = AB$ supports $H$, reflection cannot map points of $H$ back into $H$ unless they lie directly on $\ell$, forcing $\sigma(P_s) = P_s$.

* **Explicit coordinate solution:**

$$D = \vert{}\vert{}B - A\vert{}\vert{}, \quad u = \frac{B - A}{D}, \quad a = \frac{d_1^2 - d_2^2 + D^2}{2D}, \quad h = \sqrt{d_1^2 - a^2}$$


$$P_s = A + a u + h n$$



### 3. Case B: Boundary Contains No Segment

If $\partial H$ is strictly curved (contains no segments), every boundary point is an extreme point and therefore belongs to $S$.

* Query $P_1 \in \partial H$ to obtain $d_1 > 0$.
* Choose an adaptive second query $P_2 \in \partial H \setminus \{P_1\}$ such that the cap $K$ cut off by chord $P_1 P_2$ has diameter $\delta < d_1$.
* This guarantees $\sigma(P_s) \notin H \cap \sigma(H)$, reducing candidates to a single unique point for the third query.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8 or higher
* NumPy / SciPy (for numerical simulations in `experiments.py`)

### Running Simulations

To test the strategies across various shapes and verify query bounds:

```bash
python experiments.py

```

---

## 📖 Documentation & References

* **Formal Paper:** See [`formal.pdf`](https://www.google.com/search?q=formal.pdf) for rigorous measure-theoretic proofs, Carathéodory's theorem applications, and integral lower bound calculations.
* **Notes:** See [`note.md`](note.md) for a quick conceptual summary.

---

## 📄 License

This project is open-source under the [MIT License](https://www.google.com/search?q=LICENSE).