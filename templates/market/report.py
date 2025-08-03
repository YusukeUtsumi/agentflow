from pathlib import Path
import datetime

def run(input):
    # 入力は "agent_a.output + agent_b.output" の形式で渡ってくる想定
    # それぞれのファイルパスを分割
    parts = [p.strip() for p in input.split('+')]
    contents = []

    for file_path in parts:
        path = Path(file_path)
        if path.exists():
            contents.append(f"[{path.name}]\n{path.read_text()}")
        else:
            contents.append(f"[{file_path}] ファイルが見つかりません")

    # 出力先パス
    desktop = Path.home() / "Desktop"
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = desktop / f"agentflow_combined_report_{timestamp}.txt"

    print("[agent_c] agent_a と agent_b の結果を統合中...")

    # ファイルに統合結果を書き込み
    output_path.write_text("\n\n".join(contents))

    print(f"[agent_c] 統合結果を出力しました: {output_path}")
    return str(output_path)
