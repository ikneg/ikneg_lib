from collections import deque


def zeroOneBFS(nodes, S):
    ans = [10**18] * len(nodes)
    ans[S] = 0
    dq = deque([(0, S)])

    while dq:
        distance, cur = dq.popleft()
        if distance > ans[cur]:
            continue
        for nxt, cost in nodes[cur]:
            candidate = distance + cost
            if candidate < ans[nxt]:
                ans[nxt] = candidate
                dq.append((candidate, nxt)) if cost == 1 else dq.appendleft((candidate, nxt))

    return ans
