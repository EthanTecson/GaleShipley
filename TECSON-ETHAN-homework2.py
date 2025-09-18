# TECSON-ETHAN-homework2.py
import sys
from collections import deque

def main():
    lines = [line.strip() for line in sys.stdin if line.strip()]
    n = int(lines[0])

    # Parse men (first n lines after the count)
    men_order = []
    men_prefs = {}  # man -> [w1, w2, ...]
    for i in range(1, 1 + n):
        tokens = lines[i].split()
        man, prefs = tokens[0], tokens[1:]
        men_order.append(man)
        men_prefs[man] = prefs

    # Parse women (next n lines)
    women_rank = {}  # {w1: {m1,...}, w2: {m1,...}...}
    for i in range(n + 1, (n*2) + 1):
        tokens = lines[i].split()
        woman, ranking_list = tokens[0], tokens[1:]
        # Build rank map: lower rank value means higher preference
        # Rank map for men
        # {m1: 0, m2: 1, m3: 2}
        rank_map = {}
        for r, man in enumerate(ranking_list):
            rank_map[man] = r
        women_rank[woman] = rank_map

    # Gale–Shapley (men-proposing)
    free_men = deque(men_order) # preserves input order
    next_idx = {} # next woman index for each man
    for m in men_order:
        next_idx[m] = 0
    engaged_to = {} # woman: man

    while free_men:
        m = free_men.popleft()
        w = men_prefs[m][next_idx[m]]
        next_idx[m] += 1

        if w not in engaged_to:
            # woman is free
            engaged_to[w] = m
        else:
            m_current = engaged_to[w]
            # woman prefers the man with higher preference
            if women_rank[w][m] < women_rank[w][m_current]:
                engaged_to[w] = m
                free_men.append(m_current) # dumped man is free 
            else:
                free_men.append(m) # rejected

    # Format partners for output
    partners = {}
    for w,m in engaged_to.items():
        partners[m] = w

    for m in men_order:
        print(f"{m} {partners[m]}")

if __name__ == "__main__":
    main()
