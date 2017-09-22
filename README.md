# JUMAN パッチ & MinGW用ビルドスクリプト
JUMANをWindows上で使いやすくするためのパッチと、MinGW上でビルドするためのスクリプトです。

[日本語形態素解析システム JUMAN](http://nlp.ist.i.kyoto-u.ac.jp/index.php?JUMAN)

## 公式リリースとの違い
上記ページよりダウンロード可能な、Windows 64bit版からの仕様上の違いは以下です。
1. 入出力はデフォルトでUTF-8。
1. juman.iniを読み込まない。
1. -rオプションで指定されていない場合、juman.exeと同じディレクトリにあるjumanrcを読み込む。
1. jumanrc内の文法ファイル・辞書ファイルへのパスの記述は、jumanrcからの相対パスでも記述できる。
1. オプションの追加：
	* `--if <Path to file>` 入力するファイルへのパス
	* `--of <Path to file>` 出力するファイルへのパス
	* `--enc <Encoding>` エンコーディング指定（standaloneモードのみ正常動作）
1. ディレクトリの構成。

2-4は、公式リリース版と共存可能にし、ディレクトリの配置を自由にするための仕様変更です。

追加オプションは、ハイフン2つで始まります。

--encオプションは、コンマ区切りで「入力エンコーディング,出力エンコーディング」のように指定します。  
コンマなしで一つだけ指定した場合は、入出力ともそのエンコーディングになります。

## 使用例
Shift_JISのファイルを入力し、結果をUTF-8でファイルに出力：  
```shell
path\to\juman.exe --enc sjis,utf-8 --if sjis.txt --of result.txt
```

コマンドプロンプトでインタラクティブに分析：  
```shell
path\to\juman.exe -b --enc CP932
```

## ビルド
ビルドは、MSYS2 MinGW 64bit上でのみ実績があります。
（パッケージ：msys2-x86_64-20161025.exe）

### ビルド要件
ビルドには以下のパッケージが必要です。（カッコ内は実績のあるバージョン）
* mingw-w64-x86_64-libsystre (1.0.1-2)
* mingw-w64-x86_64-libtre-git (r122.c2f5d13-4)
* libintl (0.19.7-3)
* libiconv (1.14-2)

また、mingw-w64-x86_64-toolchain に含まれるツール、wget, patch, tar, bzip2なども必要です。

### ビルド方法
展開ディレクトリにある、btoolを編集します。

特にビルド後にjumanがインストールされるディレクトリを示す、変数distは適切に編集してください。  
デフォルトでは、`/tmp/juman-7.01_patched-win64`にインストールするようになっています。


MinGWのコンソールにて展開ディレクトリに移動後、以下を順に入力します。  
```shell
./btool load
./btool patch
./btool build
./btool align
```

distのディレクトリに作成されますので、その中味を適切な場所に移動してください。

### その他
Linux等、Windows以外のシステムでも、btoolを適切に編集すれば、ビルド・インストール可能かと思います。（現在のところ、そのメリットはありません。）

## ライセンス
JUMANのライセンスは3条項BSDライセンスです。（juman-7.01内のCOPYINGをご参照ください。）  
このリポジトリのパッチはパブリック・ドメインにしています。  
但しバイナリにはGNUのライブラリをリンクしているため、LGPLが適用されます。

以上。