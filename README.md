# The Hegyesy-Ramanujan Semiprime Law

By Jonathan Hegyesy.

This repository records an exact branch law for semiprimes under a
Ramanujan-Mobius complex deviation.

## Setup

Let:

```text
n = p q
p <= q
Q = floor(sqrt(p q))
```

where `p` and `q` are prime.

On the main branch:

```text
q / p < 4
```

define the visible complex deviation:

```text
Delta_Q^C(n)
  = sum_{m=2}^Q [
        log(1 + c_m(n) / m^2)
        - log(1 + mu(m) / m^2)
    ] exp(2 pi i / m)
```

Here:

```text
c_m(n) = Ramanujan sum
mu(m)  = Mobius function
```

## Theorem

If:

```text
n = p q
p <= q
q / p < 4
```

then:

```text
Delta_Q^C(pq)
  = log((p^2 + p - 1) / (p^2 - 1)) exp(2 pi i / p)
```

In particular, on the main branch, the visible complex deviation depends only
on the smaller factor `p`, not on `q`.

## Proof

A summand at index `m` can be nonzero only when:

```text
gcd(m, pq) > 1
```

Since `p` and `q` are prime, this requires:

```text
p divides m
```

or:

```text
q divides m
```

Because:

```text
m <= Q <= sqrt(pq)
```

the condition `q divides m` would imply:

```text
q <= sqrt(pq)
```

Squaring gives:

```text
q^2 <= pq
```

so:

```text
q <= p
```

Since `p <= q`, this can only occur in the equal-prime overlap. Apart from that
overlap, no `q`-multiple is visible below `sqrt(pq)`.

Thus only multiples of `p` can contribute. Write:

```text
m = k p
```

The visibility condition gives:

```text
k p <= sqrt(pq)
```

so:

```text
k <= sqrt(q / p)
```

Under the main branch condition `q / p < 4`, we get:

```text
k < 2
```

hence `k = 1`. Therefore the only active visible index is:

```text
m = p
```

At `m = p`, since `p divides pq`:

```text
c_p(pq) = phi(p) = p - 1
mu(p)   = -1
```

Therefore:

```text
1 + c_p(pq) / p^2
  = 1 + (p - 1) / p^2
  = (p^2 + p - 1) / p^2
```

and:

```text
1 + mu(p) / p^2
  = 1 - 1 / p^2
  = (p^2 - 1) / p^2
```

The single nonzero visible summand is:

```text
log((p^2 + p - 1) / (p^2 - 1)) exp(2 pi i / p)
```

This proves the theorem.

## Immediate consequences

The angle is exact:

```text
arg(Delta_Q^C(pq)) = 2 pi / p
```

The magnitude is exact:

```text
|Delta_Q^C(pq)|
  = log((p^2 + p - 1) / (p^2 - 1))
```

As `p` grows:

```text
|Delta_Q^C(pq)|
  = 1/p - 1/(2p^2) + O(p^-3)
```

For fixed `p`, all semiprimes `pq` with `p <= q` and `q / p < 4` produce the
same complex deviation.

## Numerical audit

The theorem was audited for semiprimes up to `10^7`.

| Quantity | Value |
|---|---:|
| Main-branch semiprimes tested | 120,106 |
| Ratio condition | `q / p < 4` |
| Maximum complex error | `2.4510768355742725e-16` |
| Mean complex error | `8.12140706597992e-17` |
| Maximum magnitude error | `2.445960101127298e-16` |
| Maximum angle error | `0` |
| Fixed-`p` variation | `0` to floating precision |

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
branch:

```text
q / p < 4
```

It does not claim:

- a complete theory of all higher branches `q / p >= 4`,
- a general semiprime factorization algorithm,
- a cryptographic result,
- or a result about the Riemann hypothesis.

The point is the exact branch identity: on the first visible semiprime branch,
the Ramanujan-Mobius complex deviation collapses to one vector and encodes the
smaller prime factor through its angle and radius.
