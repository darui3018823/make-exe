import subprocess
import argparse
import os

def create_exe(script_path, output_dir=None, hidden_imports=None, icon_path=None):
    """指定されたPythonスクリプトをexe化する"""
    if not os.path.exists(script_path):
        print(f"エラー: スクリプトが見つかりません: {script_path}")
        return

    # 出力先ディレクトリを設定
    if output_dir:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_option = f"--distpath {output_dir}"
    else:
        output_option = ""

    # 追加オプションの設定
    hidden_imports_option = ""
    if hidden_imports:
        hidden_imports_option = " ".join([f"--hidden-import {imp}" for imp in hidden_imports])

    icon_option = f"--icon {icon_path}" if icon_path else ""

    # PyInstallerコマンドの構築
    command = f"pyinstaller --onefile {output_option} {hidden_imports_option} {icon_option} {script_path}"
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"成功: {script_path} を exe 化しました！")
    except subprocess.CalledProcessError as e:
        print(f"エラーが発生しました: {e}")

def show_help():
    """ヘルプメッセージを表示する"""
    help_message = """
Pythonスクリプトをexe化するツール

使用方法:
  make-exe <script> [--output <directory>] [--hidden-import <module> ...] [--icon <icon_path>]

オプション:
  <script>               exe化したいPythonスクリプトのパス
  --output <directory>   exeの出力先ディレクトリ (省略時はデフォルト)
  --hidden-import        隠れたモジュールのインポートを指定 (複数指定可能)
  --icon                 exeに埋め込むアイコンのパス

例:
  make-exe my_script.py --output ./dist --hidden-import requests --icon my_icon.ico

注意:
  - pyinstallerがインストールされている必要があります。
  - このスクリプトを使用して、簡単にPythonスクリプトをexe化できます。
"""
    print(help_message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pythonスクリプトをexe化するツール", add_help=False)
    parser.add_argument("script", nargs="?", help="exe化したいPythonスクリプトのパス")
    parser.add_argument("--output", help="exeの出力先ディレクトリ", default=None)
    parser.add_argument("--hidden-import", nargs="*", help="隠れたモジュールのインポートを指定", default=None)
    parser.add_argument("--icon", help="exeに埋め込むアイコンのパス", default=None)
    args = parser.parse_args()

    if not args.script:
        print("エラー: スクリプトのパスが指定されていません。\n")
        show_help()
    else:
        create_exe(args.script, args.output, args.hidden_import, args.icon)