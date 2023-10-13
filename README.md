# cheatGraph
a graph generater from MOSS output
[Moss](https://theory.stanford.edu/~aiken/moss/) の出力から Spring Graph を作成
## Requirements
- Python3
- networkx
- matplotlib
## How to Use
```
python3 cheatGraph.py ex1-p1.txt
python3 cheatGraph.py ex1-*
```
```
w3m -dump -cols 120 http://moss.stanford.edu/results/1/1234567890/ > ex01-p1.txt
python3 cheatGraph.py ex1-p1.txt
```

- [Moss](https://theory.stanford.edu/~aiken/moss/) 出力のPlain Textファイルを引数指定すると、graph ディレクトリ配下にグラフを png 出力します。
- 入力ファイルは Moss results ページのコピペ、あるいは w3m でダンプしたものを想定しています。ｗ3m でダンプする場合は、-cols で大きめの画面幅を指定してください。ユーザ名や提出ファイル名が長いと dump テキストが途中で改行されてしまいうまく処理されません。
- 複数のMOSSファイルを指定すると、個別データのグラフ、およびそれらの統合データのグラフをMOSSデータ内の日付付き png ファイルとして出力します。統合グラフはMOSSファイル名の先頭共通部分から出力名を決定しています。
- ファイル出力（default:True）、画面表示（default: False）、バネ係数（default: 0.8）などは、グラフ描画関数 plot_weighted_network() の引数として指定しています。
