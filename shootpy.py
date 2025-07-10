import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import yaml
from tkinter import ttk

# apps.yamlの読み込み
def load_apps():
    with open('apps.yaml', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_ext(filepath):
    return os.path.splitext(filepath)[1].lower()

def launch_app(app, filepath):
    args = app['args'].replace('{file}', f'"{filepath}"')
    cmd = f'"{app["path"]}" {args}'
    try:
        subprocess.Popen(cmd, shell=True)
    except Exception as e:
        messagebox.showerror('エラー', f'アプリ起動失敗: {e}')

def select_app(apps, filepath):
    root = tk.Tk()
    root.title('アプリケーション選択')
    root.geometry('320x180')
    label = tk.Label(root, text=f'ファイル: {filepath}', wraplength=300)
    label.pack(pady=4)
    tree = ttk.Treeview(root)
    # カラム定義を先に行う
    tree['columns'] = ('name', 'path', 'args')
    tree.column('#0', width=120, minwidth=80)
    tree.heading('#0', text='アプリ名')
    tree.pack(expand=True, fill='both', padx=4, pady=4)
    # Treeviewにアプリを追加
    def add_items(parent, app_list):
        for idx, app in enumerate(app_list):
            text = app['name']
            node_id = tree.insert(parent, 'end', text=text, open=False)
            tree.set(node_id, 'name', app['name'])
            tree.set(node_id, 'path', app.get('path', ''))
            tree.set(node_id, 'args', app.get('args', ''))
            # 子項目があれば再帰的に追加
            if 'children' in app:
                add_items(node_id, app['children'])
    add_items('', apps)
    # 最初のノードを選択し、Treeviewにフォーカス
    first = tree.get_children()
    if first:
        tree.selection_set(first[0])
        tree.focus(first[0])
    tree.focus_set()
    # ダブルクリックまたはEnterで起動
    def on_open(event=None):
        sel = tree.selection()
        if not sel:
            return
        item = sel[0]
        name = tree.set(item, 'name')
        path = tree.set(item, 'path')
        args = tree.set(item, 'args')
        if path:
            app = {'name': name, 'path': path, 'args': args}
            launch_app(app, filepath)
            root.destroy()
    tree.bind('<Double-1>', on_open)
    root.bind('<Return>', on_open)
    # Escapeキーでウィンドウを閉じる
    root.bind('<Escape>', lambda event: root.destroy())
    root.mainloop()

def main():
    if len(sys.argv) < 2:
        print('ファイルパスを引数で指定してください')
        sys.exit(1)
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print('ファイルが存在しません')
        sys.exit(1)
    apps_dict = load_apps()
    ext = get_ext(filepath)
    apps = apps_dict.get(ext)
    if not apps:
        print(f'拡張子 {ext} に対応するアプリがありません')
        sys.exit(1)
    select_app(apps, filepath)

if __name__ == '__main__':
    main() 