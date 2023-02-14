# IOmonitUR / UR用 I/Oモニター

## Install
必要なパッケージ
1. RTDE_Python_Client_Library
2. PySimpleGUI

### RTDE_Python_Client_Library
ユニバーサルロボットのGitページからcloneします。
~~~
git clone https://github.com/UniversalRobots/RTDE_Python_Client_Library.git
~~~
pipでインストールがうまくいかない場合は、rtde以下をPYTHONPATHにコピーするだけでいいそうです。例えば
~~~
cp -a rtde ~/.local/lib/python3.8/site-packages/
~~~

### PySimpleGUI
Python屋さんで流行りのGUIフレームワーク(?)というか・・・ラッパーのようなもの(?)  
「2次元リストでレイアウトマネージャを代用」するという発想が、直感的でシンプル(大掛かりな開発環境が要らない)。
~~~
pip install PySimpleGUI
~~~
本家サイトには、色々Exampleあり
[PySimpleGUI](https://www.pysimplegui.org/en/latest/)

## Run
~~~
./iomonitur
~~~

## Arrangement
1. レイアウト変更  
layout_*.pyの以下のインタフェースを実装すれば、レイアウトの変更が可能です。
    - buildメソッド  
argumentで渡された、ラベル文字のリストを元にレイアウト(Widgetのリスト)を作ります。作ったリストはlayoutプロパティで参照できるようにします。
    - layoutプロパティ(オブジェクト)
buildメソッドの結果作られるオブジェクト


## Screen shot
<img src="screenshot.png" />
