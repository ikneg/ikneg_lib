from collections import deque
def zeroOneBFS(nodes, S):
    ans=[10**18]*N
    ans[S]=0

    dq=deque([(0, S)])

    while dq:
        sumCost,cur=dq.popleft()
        for x, cost in nodes[cur]:
            if sumCost > ans[cur]:
                continue
            
            c=cost+sumCost

            if c < ans[x]:
                ans[x]=c
                if cost==1:
                    dq.append((c,x))
                else:
                    dq.appendleft((c,x))

    return ans

N,M,S,T=map(int,input().split())
G=[[] for _ in range(N)]

for i in range(M):
    a,b=map(int,input().split())
    a,b=a-1,b-1
    G[a].append((b,1))

for i in range(N):
    if G[i]:
        minNode=min(x[0] for x in G[i])
        for j in range(len(G[i])):
            if minNode==G[i][j][0]:
                G[i][j]=(G[i][j][0],0)

temp=zeroOneBFS(G, S-1)

if temp[T-1]==10**18:
    print(-1)
else:
    print(temp[T-1])

        



