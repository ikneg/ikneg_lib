# ikneg_lib

AtCoder などの競技プログラミングで使う Python の実装集です。
必要なファイルの実装を提出コードにコピーして使います。外部ライブラリは不要です。

## 実装一覧

| 分類 | ファイル | 内容・計算量 |
| --- | --- | --- |
| テンプレート | [template.py](template.py) | 標準入力の補助関数・英字定数 |
| グラフ | [dijkstra.py](graph/dijkstra.py) | 非負の重みの最短路。O((V + E) log(V + E)) |
| グラフ | [zero_one_bfs.py](graph/zero_one_bfs.py) | 重みが 0・1 の最短路。O(V + E) |
| データ構造 | [bit.py](data_structures/bit.py) | 一点加算・累積和。O(log n) |
| データ構造 | [rmq.py](data_structures/rmq.py) | 一点更新・区間最大値。O(log n) |
| 全探索 | [bit_full_search.py](full_search/bit_full_search.py) | 部分集合の列挙例。O(n × 2ⁿ) |
| 方向 | [4.py](direction/4.py) / [8.py](direction/8.py) | グリッドの移動方向 |
| 整数演算 | [ceil.py](math/ceil.py) / [floor.py](math/floor.py) | 整数の割り算の切り上げ・切り下げ |

## 使い方

グラフの頂点番号は 0-indexed です。隣接リストには `(行き先, 重み)` を入れます。

```python
G = [[(1, 2), (2, 5)], [(2, 1)], []]
dist = dijkstra(G, 0)  # [0, 2, 3]
```

`zeroOneBFS(G, 0)` も同じ形式です。重みは 0 または 1 に限ります。
どちらも到達不能の距離は `10**18` です。有限の最短距離がこの値未満になる問題で使ってください。
[graph/input.txt](graph/input.txt) は手元確認用の入力データです。

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

`ceil(a, b)` と `floor(a, b)` は負数にも対応します。`b = 0` は使えません。
`bit_full_search.py` は `n` 個の要素の部分集合を列挙するサンプルです。
`direction` の `move` は `(行方向の差分, 列方向の差分)` として利用できます。

## 動作確認

```sh
python3 -m unittest discover -s tests
```
