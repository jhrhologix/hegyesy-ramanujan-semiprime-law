# The Hegyesy-Ramanujan Semiprime Law

By Jonathan Hegyesy.

This repository records an exact branch law for semiprimes under a
Ramanujan-Mobius complex deviation.

Let

$$
n=pq,\qquad p\le q,\qquad Q=\lfloor\sqrt{pq}\rfloor,
$$

where $p$ and $q$ are prime. On the main branch $q/p<4$, define

$$
\Delta_Q^{\mathbb C}(n)
=
\sum_{m=2}^{Q}
\left[
\log\!\left(1+\frac{c_m(n)}{m^2}\right)
-
\log\!\left(1+\frac{\mu(m)}{m^2}\right)
\right]e^{2\pi i/m},
$$

where $c_m(n)$ is the Ramanujan sum and $\mu(m)$ is the Mobius function.

## Theorem

If $n=pq$, $p\le q$, and $q/p<4$, then

$$
\Delta_Q^{\mathbb C}(pq)
=
\log\!\left(\frac{p^2+p-1}{p^2-1}\right)e^{2\pi i/p}.
$$

In particular, on the main branch the visible complex deviation depends only on
the smaller factor $p$, not on $q$.

## Proof

A summand at index $m$ can be nonzero only when $\gcd(m,pq)>1$, hence only
when $p\mid m$ or $q\mid m$.

Because $m\le Q\le\sqrt{pq}$, the condition $q\mid m$ would imply

$$
q\le\sqrt{pq}.
$$

Squaring gives $q^2\le pq$, so $q\le p$. Since $p\le q$, this can only
occur in the equal-prime overlap. Apart from that overlap, no $q$-multiple is
visible below $\sqrt{pq}$.

Thus only multiples of $p$ can contribute. Write $m=kp$. The visibility
condition gives

$$
kp\le\sqrt{pq},
$$

so

$$
k\le\sqrt{q/p}.
$$

Under the main branch condition $q/p<4$, we get $k<2$, hence $k=1$.
Therefore the only active visible index is $m=p$.

At $m=p$, since $p\mid pq$,

$$
c_p(pq)=\varphi(p)=p-1,\qquad \mu(p)=-1.
$$

Therefore

$$
1+\frac{c_p(pq)}{p^2}
=
\frac{p^2+p-1}{p^2},
$$

and

$$
1+\frac{\mu(p)}{p^2}
=
\frac{p^2-1}{p^2}.
$$

The single nonzero visible summand is

$$
\log\!\left(\frac{p^2+p-1}{p^2-1}\right)e^{2\pi i/p}.
$$

This proves the theorem.

## Immediate consequences

The angle is exact:

$$
\arg \Delta_Q^{\mathbb C}(pq)=\frac{2\pi}{p}.
$$

The magnitude is exact:

$$
\left|\Delta_Q^{\mathbb C}(pq)\right|
=
\log\!\left(\frac{p^2+p-1}{p^2-1}\right).
$$

As $p\to\infty$,

$$
\left|\Delta_Q^{\mathbb C}(pq)\right|
=
\frac1p-\frac1{2p^2}+O(p^{-3}).
$$

For fixed $p$, all semiprimes $pq$ with $p\le q$ and $q/p<4$ produce
the same complex deviation.

## Numerical audit

The theorem was audited for semiprimes up to $10^7$.

| Quantity | Value |
|---|---:|
| Main-branch semiprimes tested | 120,106 |
| Ratio condition | $q/p<4$ |
| Maximum complex error | $2.4510768355742725\times10^{-16}$ |
| Mean complex error | $8.12140706597992\times10^{-17}$ |
| Maximum magnitude error | $2.445960101127298\times10^{-16}$ |
| Maximum angle error | 0 |
| Fixed-$p$ variation | 0 to floating precision |

The audit script is in [scripts/audit_main_branch.py](scripts/audit_main_branch.py).
The summary table is in [data/main_branch_audit_summary.csv](data/main_branch_audit_summary.csv).

Example:

```powershell
python scripts/audit_main_branch.py --nmax 1000000
```

For the larger audit:

```powershell
python scripts/audit_main_branch.py --nmax 10000000
```

## Scope

This repository makes a narrow mathematical claim about the main semiprime
branch $q/p<4$.

It does not claim:

- a complete theory of all higher branches $q/p\ge 4$,
- a general semiprime factorization algorithm,
- a cryptographic result,
- or a result about the Riemann hypothesis.

The point is the exact branch identity: on the first visible semiprime branch,
the Ramanujan-Mobius complex deviation collapses to one vector and encodes the
smaller prime factor through its angle and radius.
