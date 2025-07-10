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
    import tkinter as tk
    import os
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを非表示
    import sys
    script_name = os.path.basename(sys.argv[0])
    file_name = os.path.basename(filepath)
    # メニュー生成
    menu = tk.Menu(root, tearoff=0)
    # 最上部にスクリプト名・ファイル名を選択不可で追加
    # menu.add_command(label=f'[{script_name}]', state='disabled')
    # menu.add_command(label=f'[{file_name}]', state='disabled')
    # menu.add_separator()
    accelerator_map = {}
    def add_menu_items(menu_obj, app_list):
        for app in app_list:
            if isinstance(app, dict) and app.get('type') == 'separator':
                menu_obj.add_separator()
                continue
            label = app['name']
            import re
            m = re.search(r'\(&([A-Za-z0-9])\)', label)
            acc = m.group(1).lower() if m else None
            # サブメニュー
            if 'children' in app:
                submenu = tk.Menu(menu_obj, tearoff=0)
                add_menu_items(submenu, app['children'])
                menu_obj.add_cascade(label=label, menu=submenu)
                if acc:
                    accelerator_map[acc] = (submenu, None)
            else:
                def make_cmd(a):
                    return lambda: (launch_app(a, filepath), root.destroy())
                menu_obj.add_command(label=label, command=make_cmd(app))
                if acc:
                    accelerator_map[acc] = (menu_obj, menu_obj.index('end'))
    add_menu_items(menu, apps)
    # アクセラレータキーで決定
    def on_accel(event):
        key = event.keysym.lower()
        if key in accelerator_map:
            menu_obj, idx = accelerator_map[key]
            if idx is not None:
                menu_obj.invoke(idx)
    root.bind_all('<KeyPress>', on_accel)
    # Escapeで閉じる
    root.bind('<Escape>', lambda event: root.destroy())
    # 起動時にメニューをスクリーン中央に表示
    def show_menu():
        x = root.winfo_screenwidth() // 2
        y = root.winfo_screenheight() // 2
        menu.tk_popup(x, y)
        root.after(100, lambda: root.destroy())  # メニューが閉じられたら終了
    root.after(100, show_menu)
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