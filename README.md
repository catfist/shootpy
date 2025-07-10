# shootpy
Windows前提

## 機能
- 拡張子ごとの引き渡し先アプリケーションリスト(`apps.yaml`)を読み込む
- ターミナル等でファイルパスを引数として受け取る
- 拡張子を判断してアプリケーションリストのGUIを生成
- 選択されたアプリケーションでファイルを開く

## `apps.yaml`仕様（YAML形式）
- 拡張子ごとにリストでアプリケーションを記述
- 各アプリは以下のキーを持つ
  - `name`: アプリケーション名（アクセラレーターキー指定可）
  - `path`: 実行ファイルのパス
  - `args`: アプリケーションに渡す引数（`{file}`でファイルパスを指定）
  - `children`: （任意）子項目リスト（サブメニューとして展開）
  - `type`: （任意）区切り線としてGUIに表示（name, path, args不要、選択不可）

### サンプル
```yaml
.txt:
  - name: メモ帳(&N)
    path: C:/Windows/System32/notepad.exe
    args: "{file}"
  - type: separator
  - name: サクラエディタ(&S)
    children:
      - name: 通常モード
        path: C:/Program Files/Sakura/sakura.exe
        args: "{file}"
      - name: 読み取り専用
        path: C:/Program Files/Sakura/sakura.exe
        args: "-R {file}"
.png:
  - name: ペイント(&P)
    path: C:/Windows/System32/mspaint.exe
    args: "{file}"
```

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
