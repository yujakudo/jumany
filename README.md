# jumany Pythonモジュール、および JUMAN 7.01＋拡張API 
日本語形態素解析システムJUMANのPythonモジュールと、そのための拡張APIを追加したJUMAN 7.01のビルド環境です。

JUMANについてはこちらをご参照ください。：
[日本語形態素解析システム JUMAN](http://nlp.ist.i.kyoto-u.ac.jp/index.php?JUMAN)

## jumany Pythonモジュール
JUMAN＋拡張APIのPythonモジュールです。

PyKNPや標準入出力を介さず、またモジュール内ではライブラリのバッファを直接参照していますので、幾分高速です。

解析結果は、後方最長一致の解一つだけを出力します。（-bオプション相当）

意味情報は取得できません。

### 要件
jumanyの利用には以下が必要です。
- POSIX または Windows
- Python 3.3以上

### インストール
```shell
pip install jumany
```
または
```shell
pip3 install jumany --user
```
など。

### 使用例
Pythonインタプリタからの使用例を以下に示します。

```shell
>>> import jumany
>>> jumany.open_lib()
True
>>> jumany.analyze("吾輩は猫である。")
[('吾輩', 'わがはい', '吾輩', 6, 1, 0, 0), ('は', 'は', 'は', 9, 2, 0, 0),('猫', 'ねこ', '猫', 6, 1, 0, 0), ('である', 'である', 'だ', 4, 0, 25, 15), ('。', ' 。', '。', 1, 1, 0, 0)]
>>> jumany.get_hinsi(6)
'名詞'
>>> jumany.get_bunrui(6,1)
'普通名詞'
>>> jumany.analyze("吾輩は猫である。\nまだ名前は無い。", True, True)
['吾輩', 'は', '猫', 'である', '。', 'まだ', '名前', 'は', '無い', '。']
```

### ライセンス
Pythonスクリプトのライセンスは2条項BSDライセンスです。

共有ライブラリのライセンスはJUMANのライセンス（3条項BSDライセンス）に準じます。

Windowsにインストールされるビルド済み共有ライブラリは、GNUのライブラリをリンクしているためLGPLが適用されます。

### 制限事項
`open_lib()`, `close_lib()`を複数回行う処理には対応していません。
スクリプトの最初で`open_lib()`するのみにして下さい。

これは、JUMAN内部のリソース管理が複雑なため開放・初期化が十分にできず、予測不可能なことが起こりうるためです。将来対応の予定もありません。

### リファレンス
品詞、品詞分類、活用型、活用形の一覧や全数が知りたいときは、それぞれ変数
 L_HINSI, L_BUNRUI, L_KATUYOU1, L_KATUYOU2 を参照してください。

以下、関数仕様を示します。

#### get_error_msg
直近に発生したエラー(失敗)のメッセージ文字列を取得します。
- 宣言：`def get_error_msg()->str:`
- 引数：なし
- 戻り：メッセージ文字列。エラーなしのときは空文字列。

#### open_lib
ライブラリの利用を開始します。
既にライブラリをオープンしている場合は、何もせずに成功を返します。
- 宣言：`def open_lib(rc_path: str = None)->bool:`
- 引数：
	- `rc_path` リソースファイルへのパス。
	`None`（未指定）のときはモジュール内のjumanrcを参照する。
- 戻り：
	- `True`: 成功
	- `False`: 失敗

#### close_lib
ライブラリの利用を終了します。
- 宣言：`def close_lib():`
- 引数：なし
- 戻り：なし

#### analyze
文字列を解析します。 
- 宣言：`def analyze(text: str, remove_space: bool = False, just_word: bool = False)->[]:`
- 引数：
	- `text`: 解析する文字列
	- `remove_space`: `True`のとき、空白（CR, LF, tab含む）のみの形態素は出力しない。
	- `just_word`: `True`のとき、形態素の文書内表記のみ出力する。（分かち書き）
- 戻り：
	- 解析結果のリスト  
		- `just_word == False`のとき：  
		[(形態素文書内表記:str, 読み:str, 基本形:str, 
		品詞コード:int, 品詞分類コード:int, 活用型コード:int, 活用形コード:int), ... ]  
		各コードが0の場合は値なしを示す。
		- `just_word == True`のとき：  
		[ 形態素文書内表記:str, ... ]
	- `None`: 失敗

#### get_hinsi
品詞の文字列を取得します。
- 宣言：`def get_hinsi(hinsi: int)->str:`
- 引数：
	- `hinsi`: 品詞コード
- 戻り：品詞の文字列

#### get_bunrui
品詞分類の文字列を取得します。
- 宣言：`def get_bunrui(hinsi: int, bunrui: int)->str:`
- 引数：
	- `hinsi`: 品詞コード
	- `bunrui`: 品詞分類コード
- 戻り：品詞分類の文字列

#### get_katuyou1
活用型の文字列を取得します。
- 宣言：`def get_katuyou1(katuyou1: int)->str:`
- 引数：
	- `katuyou1`: 活用型コード
- 戻り：活用型の文字列

#### get_katuyou2
活用形の文字列を取得します。
- 宣言：`def get_katuyou2(katuyou1: int, katuyou2: int)->str:`
- 引数：
	- `katuyou1`: 活用型コード
	- `katuyou2` 活用形コード
- 戻り：活用形の文字列

### 対話モード
モジュールを実行すると対話モードで起動します。
```shell
python3 -m jumany
```

#### オプション
- `-r <path to jumanrc>`: リソースファイルを指定します。
- `-d <delimiter>`: 指定のデリミタ区切りで表示します。指定がない場合はスペース区切りになります。
- `-h`, `--help`: ヘルプを表示します。

### テスト
以下の入力でテストを行います。
```shell
python3 -m jumany.test
```


以上、jumanyについて。

## JUMAN＋拡張API
Pythonモジュールが利用する拡張APIを実装したライブラリと、
Windows用に仕様変更した実行ファイルをビルドするための環境です。

パッチと、簡易にビルドするためのスクリプトが含まれます。

### 公式リリースとの違い
[公式リリース](http://nlp.ist.i.kyoto-u.ac.jp/index.php?JUMAN)との主要な違いは、ライブラリへのAPIの追加です。

実行ファイルの仕様上の違いは以下です。
1. jumanrc内の文法ファイル・辞書ファイルへのパスの記述は、絶対パスか、jumanrcからの相対パスで記述する。(各ファイルを探索する仕様はオミット。)
1. オプションの追加：
	- `--if <Path to file>` 入力するファイルへのパス
	- `--of <Path to file>` 出力するファイルへのパス
	- `--enc <Encoding>` エンコーディング指定（standaloneモードのみ正常動作）

またWindows用実行ファイルについては、以下の違いもあります。
1. 入出力はデフォルトでUTF-8。
1. juman.iniは参照しない。
1. -rオプションで指定されていない場合、juman.exeと同じディレクトリにあるjumanrcを読み込む。
1. ディレクトリの構成。

追加オプションは、ハイフン2つで始まります。

--encオプションは、コンマ区切りで「入力エンコーディング,出力エンコーディング」のように指定します。  
コンマなしで一つだけ指定した場合は、入出力ともそのエンコーディングになります。

### 使用例
Shift_JISのファイルを入力し、結果をUTF-8でファイルに出力：  
```shell
path\to\juman --enc sjis,utf-8 --if sjis.txt --of result.txt
```

CP932のコマンドプロンプトでインタラクティブに分析：  
```shell
path\to\juman -b --enc CP932
```

### 制限事項
このパッチと頒布バイナリは、スタンドアローンモードのみ検証しています。  
サーバ、クライアント、トレーニングの各モードでは検証していません。  
これらのモード内では入力のエンコーディング変換をしていませんので、--encオプションは利用できません。

### ビルド

#### MinGWの場合
MSYS2のMinGW上でビルドの実績があります。

##### ビルド要件
ビルドには以下のパッケージが必要です。（カッコ内は実績のあるバージョン）
- mingw-w64-x86_64-libsystre (1.0.1-2)
- mingw-w64-x86_64-libtre-git (r122.c2f5d13-4)
- libintl (0.19.7-3)
- libiconv (1.14-2)

また、mingw-w64-x86_64-toolchain に含まれるツール、wget, patch, tar, bzip2なども必要です。

##### ビルド方法
MinGWのコンソールにて展開ディレクトリに移動後、以下を順に入力します。  
```shell
./btool load
./btool build-w64
```

展開ディレクトリのdistの下に、ディレクトリ`juman-7.01_ext_win64`が作成されます。
名前を変え、適切な場所に配置してください。

#### POSIXシステムの場合
Bash on Ubuntu on Windows上でビルドの実績があります。

展開ディレクトリに移動後、以下を順に入力します。  
```shell
./btool load
cd juman-7.10
./configure
make
make install
```
（./configureのオプションは適切に指定して下さい。）

### ライセンス
JUMANのライセンスは3条項BSDライセンスです。（juman-7.01内のCOPYINGをご参照ください。）

パッチによって追加されるファイルはパブリック・ドメインです。

リリースしているWindows用バイナリには、GNUのライブラリをリンクしているため、LGPLが適用されます。


以上、JUMAN＋拡張APIについて。