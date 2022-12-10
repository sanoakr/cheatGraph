import sys
import os
import re
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from functools import reduce

matplotlib.use('TkAgg')
graph_dir = './graph'

def common_substring(list) -> str:
  def common(s1, s2):
    idx = 0
    for i, j, _ in zip(s1, s2, range(len(s1))):
      if i != j:
        break
      idx = _ + 1
    return s1[:idx]
  return ''.join(reduce(common, list))

def plot_weighted_network(uset, wdict, out=True, fout='tmp.png', show=False, spring_k=0.8):
  G = nx.Graph()
  # add edges
  for (u1, u2), w in wdict.items():
    G.add_edge(u1, u2, weight=w)
  # add 0 weight edges
  for u1 in uset:
    for u2 in uset:
      if u1 == u2:
        continue
      uTuple = tuple(sorted((u1,u2)))
      #if not uTuple in wdict:
      #  G.add_edge(u1, u2, weight=0)

  # draw network
  plt.figure(figsize=(10,10))
  pos = nx.spring_layout(G, k=spring_k)
  weights = nx.get_edge_attributes(G, 'weight').values()
  nx.draw_networkx(G, pos = pos,
    node_size = 150, node_color = 'w', edgecolors = 'k', linewidths = 1,
    with_labels = True, font_size = 8, font_color = 'k',
    edge_color = weights, edge_cmap = plt.cm.Reds, #edge_vmin = 0, edge_vmax = 20,
  )
  # out
  if out:
    os.makedirs(graph_dir, exist_ok=True)
    plt.savefig(f'{graph_dir}/{fout}', dpi=300, bbox_inches='tight')
  if show:
    plt.get_current_fig_manager().window.wm_geometry("+100+100")
    plt.show()

if __name__ == '__main__':
  # ファイル名をコマンドライン引数から取得
  files = sys.argv[1:]
  # 統合グラフ用のデータ
  uListAll = []
  wDictAll = {}

  # ファイルを逐次処理
  for fn in files:
    # ファイル名から拡張子を除いた部分を取得
    fn_head = fn.split('.')[0]

    with open(fn) as f:
      lines = f.read().splitlines()
      # 日付パターン
      dtpat = r'^(Sun|Mon|Tue|Wed|Thu|Fri|Sat)\s+'
      # データ部を処理
      uList = []
      wDict = {}
      for l in lines:
        # 日付行を処理
        if re.match(dtpat, l):
          dtString = l.replace(' ', '-').replace(':', '-')
        # p で始まる行のみ処理
        if l.startswith('p'):
          pat = r'p\d+\/(\w+)\/.+\s+\((\d+)\%\)'
          lpat = pat + r'\s+' + pat + r'\s+(\d+)'
          u1, p1, u2, p2, m = re.match(lpat, l).groups()
          # ユーザーリストに追加
          uList.append(u1)
          uList.append(u2)
          # weight は百分率の平均 * matchした行数
          w = (float(p1)+float(p2))/200 * int(m)
          # ユーザータプルをソート
          uTuple = tuple(sorted((u1,u2)))
          # weight が無いかより小さい値なら設定（複数あれば最大値を設定する）
          if (not uTuple in wDict) or wDict[uTuple] > w:
            wDict[uTuple] = w
          #print(f'{u1}\t{u2}\t{w}')

      # 統合グラフ用のデータに追加
      uListAll.extend(uList)
      for uTuple, w in wDict.items():
        if not uTuple in wDictAll:
          wDictAll[uTuple] = w
        else:
          wDictAll[uTuple] += w

      # ユーザーリスト
      uSet = set(uList)
      # 個別グラフを描画
      plot_weighted_network(uset=uSet, wdict=wDict, fout=fn_head+'_'+dtString+'.png')

  # 統合グラフを描画
  uSetAll = set(uListAll)
  plot_weighted_network(uset=uSetAll, wdict=wDictAll, fout=common_substring(files)+'_'+dtString+'.png')