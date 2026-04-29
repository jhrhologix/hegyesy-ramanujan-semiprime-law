"""
Audit the Hegyesy-Ramanujan main semiprime branch law.

The theorem tested:
    If n = p*q, p <= q prime, Q = floor(sqrt(n)), and q/p < 4, then

        Delta_Q^C(pq)
        = log((p^2 + p - 1) / (p^2 - 1)) * exp(2*pi*i/p).

This script is intentionally standalone: it uses only the Python standard
library and computes the visible deviation directly on the main branch.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


def build_spf(nmax: int) -> list[int]:
    spf = list(range(nmax + 1))
    if nmax >= 1:
        spf[1] = 1
    for i in range(2, math.isqrt(nmax) + 1):
        if spf[i] == i:
            start = i * i
            for j in range(start, nmax + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf


def build_omega(spf: list[int]) -> list[int]:
    omega = [0] * len(spf)
    for n in range(2, len(spf)):
        omega[n] = 1 + omega[n // spf[n]]
    return omega


def build_mobius(nmax: int) -> list[int]:
    mu = [1] * (nmax + 1)
    prime_count = [0] * (nmax + 1)
    square_factor = [False] * (nmax + 1)
    for p in range(2, nmax + 1):
        if prime_count[p] == 0:
            for j in range(p, nmax + 1, p):
                prime_count[j] += 1
            p2 = p * p
            for j in range(p2, nmax + 1, p2):
                square_factor[j] = True
    for n in range(2, nmax + 1):
        if square_factor[n]:
            mu[n] = 0
        elif prime_count[n] % 2:
            mu[n] = -1
        else:
            mu[n] = 1
    return mu


def ramanujan_c(m: int, n: int, mu: list[int]) -> int:
    g = math.gcd(m, n)
    total = 0
    d = 1
    while d * d <= g:
        if g % d == 0:
            total += d * mu[m // d]
            other = g // d
            if other != d:
                total += other * mu[m // other]
        d += 1
    return total


def actual_delta_main_branch(n: int, p: int, mu: list[int]) -> complex:
    qmax = math.isqrt(n)
    total = 0.0 + 0.0j
    for m in range(p, qmax + 1, p):
        c = ramanujan_c(m, n, mu)
        baseline = mu[m]
        if c == baseline:
            continue
        term = math.log(1.0 + c / (m * m)) - math.log(1.0 + baseline / (m * m))
        total += term * complex(math.cos(2.0 * math.pi / m), math.sin(2.0 * math.pi / m))
    return total


def expected_delta(p: int) -> complex:
    amp = math.log((p * p + p - 1.0) / (p * p - 1.0))
    phase = 2.0 * math.pi / p
    return amp * complex(math.cos(phase), math.sin(phase))


def angle_error(a: complex, b: complex) -> float:
    aa = math.atan2(a.imag, a.real)
    bb = math.atan2(b.imag, b.real)
    return abs((aa - bb + math.pi) % (2.0 * math.pi) - math.pi)


def audit(nmax: int) -> dict[str, float | int]:
    spf = build_spf(nmax)
    omega = build_omega(spf)
    mu = build_mobius(math.isqrt(nmax) + 1)

    tested = 0
    min_ratio = float("inf")
    max_ratio = 0.0
    max_complex_error = 0.0
    sum_complex_error = 0.0
    max_magnitude_error = 0.0
    sum_magnitude_error = 0.0
    max_angle_error = 0.0
    sum_angle_error = 0.0

    for n in range(4, nmax + 1):
        if omega[n] != 2:
            continue
        p = spf[n]
        q = n // p
        if p > q:
            p, q = q, p
        ratio = q / p
        if ratio >= 4.0:
            continue

        actual = actual_delta_main_branch(n, p, mu)
        expected = expected_delta(p)
        complex_error = abs(actual - expected)
        magnitude_error = abs(abs(actual) - abs(expected))
        theta_error = angle_error(actual, expected)

        tested += 1
        min_ratio = min(min_ratio, ratio)
        max_ratio = max(max_ratio, ratio)
        max_complex_error = max(max_complex_error, complex_error)
        sum_complex_error += complex_error
        max_magnitude_error = max(max_magnitude_error, magnitude_error)
        sum_magnitude_error += magnitude_error
        max_angle_error = max(max_angle_error, theta_error)
        sum_angle_error += theta_error

    if tested == 0:
        raise RuntimeError("No main-branch semiprimes found.")

    return {
        "tested_count": tested,
        "min_ratio": min_ratio,
        "max_ratio": max_ratio,
        "max_complex_abs_error": max_complex_error,
        "mean_complex_abs_error": sum_complex_error / tested,
        "max_magnitude_error": max_magnitude_error,
        "mean_magnitude_error": sum_magnitude_error / tested,
        "max_angle_error": max_angle_error,
        "mean_angle_error": sum_angle_error / tested,
    }


def save_summary(path: Path, row: dict[str, float | int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nmax", type=int, default=1_000_000)
    parser.add_argument("--out", type=Path, default=Path("data/latest_audit_summary.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    row = audit(args.nmax)
    save_summary(args.out, row)
    print("Hegyesy-Ramanujan main semiprime branch audit")
    for key, value in row.items():
        print(f"{key}: {value}")
    print(f"saved: {args.out}")


if __name__ == "__main__":
    main()
