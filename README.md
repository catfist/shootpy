# shootpy
Windows前提

## 機能
- 拡張子ごとの引き渡し先アプリケーションリスト(`apps.json`)を読み込む
- ターミナル等でファイルパスを引数として受け取る
- 拡張子を判断してアプリケーションリストのGUIを生成
- 選択されたアプリケーションでファイルを開く

## `apps.json`仕様
- "name": アプリケーション名
	- アクセラレーターキーを指定可能
- "path": 実行ファイルのパス
- "args": アプリケーションに渡す引数
	- プレースホルダにより引き渡すファイルパスを記述する

## 実行ファイル化（PyInstaller使用）

1. 必要なパッケージをインストール
   ```sh
   pip install pyinstaller pyyaml
   ```
2. 実行ファイルを作成
   ```sh
   pyinstaller --onefile --noconsole shootpy.py
   ```
   - dist/shootpy.exe が生成されます。
   - apps.yaml も同じフォルダに配置してください。

3. 実行例
   ```sh
   dist\shootpy.exe <ファイルパス>
   ```
