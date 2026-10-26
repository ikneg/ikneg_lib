# ikneg_lib

AtCoder などの競技プログラミングで使う Python の実装集です。
必要なファイルの中身を、import や定数も含めて提出コードにコピーして使います。
Python 3.8 以降に対応し、外部ライブラリは不要です。使い方や注意点はこの README にまとめています。

## 実装一覧

| 分類 | ファイル | 内容・計算量 |
| --- | --- | --- |
| テンプレート | [template.py](template.py) | 標準入力の補助関数・英字定数 |
| グラフ | [dijkstra.py](graph/dijkstra.py) | 非負の重みの最短路。O((V + E) log(V + E)) |
| グラフ | [zero_one_bfs.py](graph/zero_one_bfs.py) | 重みが 0・1 の最短路。O(V + E) |
| グラフ | [lca.py](graph/lca.py) | ダブリングによる最小共通祖先。構築 O(n log n)、取得 O(log n) |
| グラフ | [scc.py](graph/scc.py) | Kosaraju 法による強連結成分分解。O(V + E) |
| グラフ | [max_flow.py](graph/max_flow.py) | Dinic 法による最大流。O(V²E) |
| データ構造 | [bit.py](data_structures/bit.py) | 一点加算・累積和。O(log n) |
| データ構造 | [rmq.py](data_structures/rmq.py) | 一点更新・区間最大値。O(log n) |
| データ構造 | [lazy_segtree.py](data_structures/lazy_segtree.py) | 汎用の区間更新・区間集約。O(log n) |
| データ構造 | [union_find.py](data_structures/union_find.py) | 集合の併合・連結判定。償却 O(α(n)) |
| データ構造 | [coordinate_compression.py](data_structures/coordinate_compression.py) | 座標圧縮と復元用の値一覧。O(n log n) |
| 文字列 | [rolling_hash.py](string/rolling_hash.py) | 部分文字列のハッシュ。構築 O(n)、取得 O(1) |
| 整数演算 | [combination.py](math/combination.py) | 二項係数。前計算 O(n + log mod)、nCr 取得 O(1) |
| 整数演算 | [mod_inverse.py](math/mod_inverse.py) | 法に対する逆元。O(log mod) |
| 全探索 | [bit_full_search.py](full_search/bit_full_search.py) | 部分集合の列挙例。O(n × 2ⁿ) |
| 方向 | [4.py](direction/4.py) / [8.py](direction/8.py) | グリッドの移動方向 |
| 整数演算 | [ceil.py](math/ceil.py) / [floor.py](math/floor.py) | 整数の割り算の切り上げ・切り下げ |

## 使い方

追加した実装の添字・頂点番号は 0-indexed、区間は半開区間 `[l, r)` です。
既存の BIT と rmq は 1-indexed なので、使い分けに気をつけてください。

### 最短路

グラフの頂点番号は 0-indexed です。隣接リストには `(行き先, 重み)` を入れます。

```python
G = [[(1, 2), (2, 5)], [(2, 1)], []]
dist = dijkstra(G, 0)  # [0, 2, 3]
```

`zeroOneBFS(G, 0)` も同じ形式です。重みは 0 または 1 に限ります。
どちらも到達不能の距離は `10**18` です。有限の最短距離がこの値未満になる問題で使ってください。
[graph/input.txt](graph/input.txt) は手元確認用の入力データです。

### BIT・区間最大値

BIT と rmq は 1-indexed です。添字や引数の検証は行わないため、有効な範囲で使ってください。
BIT の `add(i, x)` は `1 <= i <= n`、`sum(i)` は `0 <= i <= n` です。
`sum(0)` は 0 を返し、`length(n)` は値をすべて 0 に戻します。
rmq の `update(pos, x)` は `1 <= pos <= n`、`query(l, r)` は `1 <= l <= r <= n + 1` で使います。

```python
bit = BIT(5)  # BIT() のあと bit.length(5) でも初期化可能
bit.add(2, 3)
bit.add(4, 7)
bit.sum(4) - bit.sum(1)  # [2, 4] の和: 10

T = rmq(5)  # 区間最大値。初期値はすべて 0
T.update(2, 8)
T.query(1, 4)  # [1, 4) の最大値: 8
```

`rmq` は名前に反して区間最大値を求めます。従来の `query(l, r, 1, T.siz + 1, 1)` も使えます。
空区間の問い合わせは `-inf` を返します。

### 整数の割り算・その他

`ceil(a, b)` と `floor(a, b)` は負数にも対応します。`b = 0` は使えません。
`bit_full_search.py` は `n` 個の要素の部分集合を列挙するサンプルです。
`direction` の `move` は `(行方向の差分, 列方向の差分)` として利用できます。

### Lazy Segment Tree

[lazy_segtree.py](data_structures/lazy_segtree.py) の `LazySegmentTree` クラスをコピーして使います。
こちらは **0-indexed** で、区間は **半開区間 `[l, r)`** です。
構築・メモリは O(n)、区間更新・区間取得・一点操作は O(log n)、全体の取得は O(1) です。
計算量は、渡す関数が O(1) で動く場合です。

区間加算・区間和の例です。各ノードに `(区間和, 要素数)` を持たせると、
区間への加算を `区間和 + 加算値 × 要素数` で処理できます。

```python
values = [1, 2, 3, 4, 5]
seg = LazySegmentTree(
    [(x, 1) for x in values],
    op=lambda a, b: (a[0] + b[0], a[1] + b[1]),
    e=(0, 0),
    mapping=lambda f, x: (x[0] + f * x[1], x[1]),
    composition=lambda f, g: f + g,
    id_=0,
)

seg.apply(1, 4, 10)         # [1, 12, 13, 14, 5]
print(seg.prod(1, 4)[0])    # 39
print(seg.all_prod()[0])    # 45
print(seg.get(2)[0])        # 13
seg.set(2, (7, 1))         # 位置2を7に置換。要素数も渡す
print(seg.prod(0, 3)[0])    # 20
```

| 引数 | 意味・満たす条件 |
| --- | --- |
| `values` | 初期値の iterable。整数の長さではなく、要素を渡す |
| `op(a, b)` | 左右の区間の集約。結合則を満たすこと。可換でなくてもよい |
| `e` | `op(e, x) == op(x, e) == x` となる単位元 |
| `mapping(f, x)` | 集約値 `x` に更新 `f` を適用する関数 |
| `composition(f, g)` | **先に `g`、次に `f`** を適用した更新 |
| `id_` | 何もしない更新。`mapping(id_, x) == x` を満たす |

`mapping(f, op(a, b)) == op(mapping(f, a), mapping(f, b))` と、
`mapping(composition(f, g), x) == mapping(f, mapping(g, x))` を満たすように定義してください。
更新の合成は結合則を満たし、`id_` を単位元とする必要があります。
`e` や `id_` は内部で共有するので、タプルや整数などを使い、渡した値や関数の引数を破壊的に変更しないでください。

区間代入・区間和なら、上の例の `mapping` を
`lambda f, x: x if f is None else (f * x[1], x[1])`、
`composition` を `lambda f, g: g if f is None else f`、`id_` を `None` に変更できます。
代入する値の `0` と「更新なし」を区別するのがポイントです。

`prod(l, l)` は `e` を返し、`apply(l, l, f)` は何もしません。
空配列も構築でき、`all_prod()` は `e` になります。
区間は `0 <= l <= r <= n`、一点操作は `0 <= p < n` に限り、範囲外は `IndexError` になります。

| メソッド | 内容 |
| --- | --- |
| `apply(l, r, f)` | `[l, r)` に更新 `f` を適用 |
| `prod(l, r)` | `[l, r)` の集約値を取得 |
| `all_prod()` | 全体の集約値を取得 |
| `get(p)` | 一点の値を取得 |
| `set(p, x)` | 一点の値を `x` に置換 |

### Union-Find

連結成分を管理します。`UnionFind(n)` で `0` から `n - 1` の各要素を別々の集合として作ります。
経路圧縮とサイズによる併合を使い、併合・判定・代表元・サイズの取得は償却 O(α(n))、構築とメモリは O(n) です。
辺の削除や併合の取り消しには対応していません。

```python
uf = UnionFind(5)
uf.merge(0, 2)
uf.merge(2, 4)
print(uf.same(0, 4))  # True
print(uf.same(0, 1))  # False
print(uf.size(2))     # 3
print(uf.group_count) # 3
print(uf.groups())   # [[0, 2, 4], [1], [3]]
```

`leader(a)` は代表元、`merge(a, b)` は併合後の代表元を返します。
すでに同じ集合なら何も変更しません。代表元やグループの順序には意味を持たせないでください。
`groups()` は全グループの要素一覧を返し、O(n α(n)) です。
`n = 0` も使え、`groups()` は `[]`、`group_count` は `0` です。
範囲外の要素は `IndexError`、負の `n` は `ValueError` になります。

### 座標圧縮

`coordinate_compress(values)` は `(圧縮後の配列, 昇順の重複なし元データ)` を返します。
同じ値は同じ番号になり、大小関係を保ったまま `0` から連番を振ります。
構築は O(n log n)、メモリは O(n) です。

```python
compressed, originals = coordinate_compress([40, -3, 40, 100])
print(compressed)                     # [1, 0, 1, 2]
print(originals)                      # [-3, 40, 100]
print([originals[i] for i in compressed])  # [40, -3, 40, 100]
```

入力は iterable で、要素はハッシュ可能かつ互いに大小比較できる値にしてください。
空入力なら `([], [])` です。番号の差は元の座標間の距離を表さないため、距離が必要な場面では `originals` を使います。

### LCA（最小共通祖先）

重みなし・連結・無向の木を、隣接リストで渡します。各辺を両方向に一度ずつ入れてください。
`LCA(graph, root=0)` は指定した根に対する最小共通祖先を前計算します。
構築とメモリは O(n log n)、各問い合わせは O(log n) です。

```python
graph = [[1, 2], [0, 3, 4], [0], [1], [1]]
tree = LCA(graph)
print(tree.lca(3, 4))           # 1
print(tree.lca(2, 4))           # 0
print(tree.distance(2, 4))      # 3
print(tree.kth_ancestor(4, 2))  # 0
print(tree.kth_ancestor(4, 3))  # -1
print(tree.depth[4])           # 2
```

`distance(a, b)` は辺数による距離です。`kth_ancestor(v, 0)` は `v` 自身、根より上なら `-1` を返します。
空の木、不正な根、非連結、探索で検出した閉路、負の `k` は `ValueError`、範囲外の頂点は `IndexError` になります。
入力が無向・重複辺なしであることは呼び出し側で保証してください。
探索は反復処理なので、長い一本道でも再帰の深さ制限を変更せず使えます。

### Rolling Hash

`RollingHash(text)` は文字列の部分区間のハッシュを計算します。
法は `2**61 - 1`、基数はファイルの読み込み時にランダムに選び、同じ実装から作ったインスタンスで共有します。
構築・メモリは O(n)、`get(l, r)` は O(1) です。

```python
text = "abracadabra"
hashed = RollingHash(text)
print(hashed.get(0, 4) == hashed.get(7, 11))  # True
other = RollingHash("abra", base=hashed.base)
print(hashed.get(0, 4) == other.get(0, 4))    # True
print(hashed.get(2, 2))                     # 0
```

異なる文字列や区間を比較するときは、基数と区間の長さをそろえてください。
同じハッシュでも衝突により文字列が異なる可能性があります。厳密な一致が必要なら元の文字列も比較してください。
実行ごとに基数が変わるため、ハッシュ値を保存して別の実行結果と比べる用途には、同じ `base` を明示します。
空文字列も扱えます。範囲外の区間は `IndexError`、`1 < base < 2**61 - 1` を満たさない基数は `ValueError` です。

### SCC（強連結成分分解）

`SCC(n)` に有向辺を追加し、`scc()` で互いに到達できる頂点をグループに分けます。
構築と分解、メモリは O(V + E)、一辺の追加は償却 O(1) です。

```python
graph = SCC(4)
for a, b in [(0, 1), (1, 0), (1, 2), (2, 3), (3, 2)]:
    graph.add_edge(a, b)
groups = graph.scc()
print([sorted(group) for group in groups])  # [[0, 1], [2, 3]]

component_id = [0] * 4
for i, group in enumerate(groups):
    for v in group:
        component_id[v] = i
```

グループは縮約後の DAG のトポロジカル順に返します。異なる成分への辺 `a -> b` について、
`component_id[a] < component_id[b]` が成り立ちます。グループ内の頂点順序は保証しません。
自己ループ・多重辺・孤立頂点に対応し、頂点数が `0` なら `[]` を返します。
辺を追加して再び `scc()` を呼ぶと、その時点のグラフを分解し直します。
負の頂点数は `ValueError`、範囲外の頂点は `IndexError` です。探索に再帰は使いません。

### 二項定理・二項係数

二項定理 `(a + b)**n = Σ C(n, r) * a**(n-r) * b**r` に使う二項係数を計算します。
`Combination(n, mod=998244353)` は階乗と逆階乗を前計算し、`comb(n, r)` で法 `mod` における nCr を返します。
前計算は O(n + log mod)、メモリは O(n)、問い合わせは O(1) です。

```python
combinations = Combination(100, mod=998244353)
print(combinations.comb(5, 2))  # 10
print(combinations.comb(5, 8))  # 0
print(combinations.comb(0, 0))  # 1

coefficients = binomial_coefficients(4)
print(coefficients)  # [1, 4, 6, 4, 1]
a, b = 2, 3
print(sum(c * a**(4 - r) * b**r for r, c in enumerate(coefficients)))  # 625
```

`Combination` は `n!` と `mod` が互いに素である必要があります。
通常は素数の `mod` と `0 <= n < mod` で使ってください。
この条件を満たす複合数の法も使えますが、逆階乗が存在しなければ構築時に `ValueError` になります。
`comb(n, r)` の `n` が前計算範囲外の場合も `ValueError`、`r < 0` または `r > n` は `0` です。

`binomial_coefficients(n)` は法を取らない正確な整数で `[C(n, 0), ..., C(n, n)]` を返します。
`n = 0` なら `[1]`、負の `n` は `ValueError` です。
O(n) 回の整数演算を使いますが、値が大きくなると多倍長整数の計算時間・メモリも増えます。
上記の計算量は整数演算を O(1) とした目安です。

### 逆元

`mod_inverse(a, mod)` は `a * x % mod == 1` となる `0 <= x < mod` を返します。
Python の `pow(a, -1, mod)` を使い、計算量は O(log mod) です。

```python
print(mod_inverse(3, 7))   # 5
print(mod_inverse(-3, 7))  # 2
print(mod_inverse(5, 12))  # 5
print(10 * mod_inverse(3, 7) % 7)  # 法7での10/3: 1
```

法は素数でなくても構いませんが、`gcd(a, mod) == 1` が必要です。
逆元が存在しない場合や `mod <= 1` の場合は `ValueError` になります。
通常の整数除算とは異なり、法に対する割り算に使う関数です。

### 最大流

`MaxFlow(n)` に有向辺と非負整数の容量を追加し、`flow(source, sink)` で最大流を求めます。
Dinic 法を用い、最大流は O(V²E)、メモリは O(V + E)、一辺の追加は償却 O(1) です。
経路の探索に再帰は使いません。

```python
graph = MaxFlow(4)
edge_id = graph.add_edge(0, 1, 3)
graph.add_edge(0, 2, 2)
graph.add_edge(1, 2, 1)
graph.add_edge(1, 3, 2)
graph.add_edge(2, 3, 3)
print(graph.flow(0, 3))           # 5
print(graph.get_edge(edge_id))    # (0, 1, 3, 3)
print(graph.min_cut(0))           # [True, False, False, False]
print(graph.flow(0, 3))           # 0
```

| メソッド | 内容・計算量 |
| --- | --- |
| `add_edge(a, b, capacity)` | 有向辺を追加し、その辺の番号を返す。償却 O(1) |
| `flow(s, t, limit=None)` | 追加で流せた量を返す。`limit` で今回流す量を制限できる |
| `get_edge(i)` | `(始点, 終点, 元の容量, 現在の流量)` を返す。O(1) |
| `edges()` | 追加順ですべての辺の情報を返す。O(E) |
| `min_cut(s)` | 残余グラフで `s` から到達できる頂点を bool 配列で返す。O(V + E) |

`flow` は内部の残余容量を更新します。同じ始点・終点で繰り返すと追加分だけが返ります。
最初から計算し直す場合や始点・終点を変える場合は、インスタンスを作り直してください。
途中で辺を追加して、同じ始点・終点から計算を続けることもできます。
`min_cut(s)` が最小カットを表すのは、最大流まで流し切った後です。`limit` で途中終了した場合は保証されません。
無向辺は両方向の有向辺として追加してください。自己ループ・多重辺・逆向きの辺・容量 `0` にも対応しています。
始点と終点が同じ場合、負の頂点数、負数や整数以外の容量・上限は `ValueError`、範囲外の頂点・辺番号は `IndexError` です。

## 動作確認

```sh
python3 -m unittest discover -s tests
```

Lazy Segment Tree は、単純な配列とのランダム比較で区間加算・代入・アフィン変換を確認しています。
空配列・空区間・一点操作・2の累乗でない長さ・更新の合成順序・可換でない集約もテスト対象です。
追加した実装も、配列による集合管理・親をたどる LCA・全点間の到達可能性・全カット列挙などと比較しています。
最大流は容量制約・流量保存・流量制限後の再開を確認し、LCA・SCC・最大流は長さ 3000 の一本道でも確認しています。
二項係数は `math.comb`、逆元は互いに素かどうかによる成功・失敗、Rolling Hash は直接計算したハッシュと比較しています。

## 変更ログ

### 2026-10-27

- Union-Find・座標圧縮・LCA・Rolling Hash・SCC・二項係数・逆元・最大流を追加。
- 各実装の使用例、計算量、戻り値、入力条件、例外、注意点を README に追加。
- Lazy Segment Tree のコード内コメント・docstring を削除し、説明を README に集約。
- 追加実装の比較テストと、再帰を使わないグラフ探索の確認を追加。
- 汎用の `LazySegmentTree` を追加。区間更新・区間集約・一点取得・一点置換に対応。
- 初期化と区間加算・区間和の使用例、区間代入への変更方法、演算の条件と計算量を追加。
- 遅延更新と境界条件を確認するテストを追加。
