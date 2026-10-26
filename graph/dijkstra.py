from heapq import heappop, heappush


def dijkstra(nodes, S):
    ans = [10**18] * len(nodes)
    ans[S] = 0
    hq = [(0, S)]

    while hq:
        distance, cur = heappop(hq)
        if distance > ans[cur]:
            continue
        for nxt, cost in nodes[cur]:
            candidate = distance + cost
            if candidate < ans[nxt]:
                ans[nxt] = candidate
                heappush(hq, (candidate, nxt))

    return ans
