# Finding a Hidden Point from Distance Queries on an Arbitrary Shape

## Problem

Let $S \subset \mathbb{R}^2$ be a **closed, bounded** set with positive area. A point $P_s$ is drawn uniformly from $S$. Each guess must be a point $P \in S$ and returns $|P - P_s|$. What is the minimum number of guesses needed to find $P_s$, **counting the final guess that hits it**?

## Result

> **Theorem.** For every such $S$, the answer is $3$.
>
> 1. **Upper bound.** There is a strategy that finds $P_s$ in at most $3$ guesses for *every* $P_s \in S$ in the worst case.
> 2. **Lower bound.** Any strategy finds $P_s$ within $2$ guesses with probability $0$.

---

## 1. Two guesses leave a mirror pair

**Lemma 1.** Let $P_1 \neq P_2$, let $\ell$ be the line through them, and let $\sigma$ be the reflection across $\ell$. Given $d_i = |P_i - P_s|$, the set of points $x \in \mathbb{R}^2$ with $|x - P_i| = d_i$ for $i = 1, 2$ is contained in $\{P_s,\ \sigma(P_s)\}$.

*Proof.* $\sigma$ is an isometry fixing $P_1$ and $P_2$, so $|\sigma(P_s) - P_i| = |P_s - P_i| = d_i$. Two circles with distinct centers meet in at most two points.

So after two guesses the candidates on the sheet are $\{P_s, \sigma(P_s)\} \cap S$. Guess 3 is forced to hit unless

$$\sigma(P_s) \in S \quad\text{and}\quad \sigma(P_s) \neq P_s .$$

If $\sigma(P_s) \in S$, then $\sigma(P_s) \in S \cap \sigma(S)$. With $H = \text{conv}(S)$ this gives

$$\sigma(P_s) \in S \;\Longrightarrow\; \sigma(P_s) \in H \cap \sigma(H). \tag{$*$}$$

**Goal:** choose $P_1, P_2 \in S$ so that $H \cap \sigma(H)$ cannot contain a point $\sigma(P_s) \neq P_s$.

---

## 2. Two facts about the convex hull

Since $S$ is compact with positive area, $H$ is a compact convex set with nonempty interior.

- **(F1)** Every extreme point of $H$ lies in $S$.
- **(F2)** A boundary point of $H$ that is not extreme lies in the relative interior of a segment contained in $\partial H$. So either $\partial H$ contains a segment, or **every** point of $\partial H$ is extreme, hence in $S$ by (F1).

Together, the guessable points include the extreme points of $H$, **even when $S$ is non-convex** (dents, holes, several components) and the segment between two such points leaves $S$.

---

## 3. Strategy

**Case A: $\partial H$ contains a segment.** Take a maximal segment $[A, B] \subset \partial H$. Its endpoints are extreme points, so $A, B \in S$.

- Guess $P_1 = A$, $P_2 = B$.
- Compute the two candidates and keep the one on the same side of $\ell = AB$ as $H$ (or the single point on $\ell$ if the circles are tangent).
- Guess it.

**Case B: $\partial H$ contains no segment.** Every boundary point is extreme, hence guessable.

- Guess any $P_1 \in \partial H$ and read $d_1$. If $d_1 = 0$, we are done.
- Choose $P_2 \in \partial H \setminus \{P_1\}$ so close to $P_1$ that the *cap* cut off by the chord $P_1 P_2$ has diameter $\delta < d_1$ (see §4, Case B).
- Guess $P_2$, read $d_2$, and take the candidate that lies in $S$.
- Guess it.

---

## 4. Correctness

### Case A

The line $\ell$ through $A, B$ supports $H$, so $H$ lies in one closed half-plane of $\ell$. Then $\sigma(H)$ lies in the opposite closed half-plane, and

$$H \cap \sigma(H) \subset \ell .$$

By $(*)$, if $\sigma(P_s) \in S$ then $\sigma(P_s) \in \ell$, so $\sigma(P_s) = P_s$. Hence the only candidate on the sheet is $P_s$, and guess 3 hits it.

**Explicit formula.** Let $D = |AB|$, $u = (B - A)/D$, and let $n$ be the unit normal to $\ell$ pointing toward $H$. Then

$$P_s = A + a\,u + h\,n, \qquad a = \frac{d_1^2 - d_2^2 + D^2}{2D}, \qquad h = \sqrt{d_1^2 - a^2} \ \ (\ge 0).$$
### Case B

Let $\ell$ be the line through $P_1, P_2$. Let $\ell^-$ be the closed half-plane of $\ell$ containing the short boundary arc from $P_1$ to $P_2$, and let

$$K = H \cap \ell^- \qquad\text{(the cap).}$$

**Claim 1: $H \cap \sigma(H) \subset K \cup \sigma(K)$.** Take $x \in H \cap \sigma(H)$.

- If $x \in \ell^-$, then $x \in H \cap \ell^- = K$.
- Otherwise $x$ is in the open half-plane opposite $\ell^-$, and $x \in \sigma(H)$ there, so $x \in \sigma(H \cap \ell^-) = \sigma(K)$.

**Claim 2: $\text{diam}(K) \to 0$ as $P_2 \to P_1$ along $\partial H$.** $K$ is the convex region bounded by the chord $P_1P_2$ and the boundary arc from $P_1$ to $P_2$. Its diameter equals the diameter of that arc, which shrinks to $0$ as $P_2 \to P_1$. So for fixed $d_1 > 0$ we can pick $P_2$ with $\delta := \text{diam}(K) < d_1$.

**Conclusion.** $P_1 \in K$ and $\sigma(P_1) = P_1$, so $K \cup \sigma(K) \subset \bar{B}(P_1, \delta)$. If $\sigma(P_s) \in S$, then by $(*)$ and Claim 1,

$$|\sigma(P_s) - P_1| \le \delta < d_1 .$$

But $|\sigma(P_s) - P_1| = |P_s - P_1| = d_1$, a contradiction. So $\sigma(P_s) \notin S$, the only candidate on the sheet is $P_s$, and guess 3 hits it.

(In Case B, $P_2$ is chosen **adaptively** from $d_1$.)

---

## 5. Lower bound

- **You only get one shot per distance ring:** When you make your first guess, finding out the distance tells you the secret point is hiding somewhere on a circle around your first guess. But your second-guess strategy can only pick **one single point** for that distance.
- **A single point can't cover a whole circle:** Since the secret point could be anywhere along that circle, trying to hit it with just one guess is like trying to hit a moving target with a single grain of sand. The odds of guessing the exact right spot on that circle are zero.

Combined with §3-4, **the minimum is exactly $3$.**

---
