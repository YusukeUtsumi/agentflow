import subprocess
from pathlib import Path
import datetime

def run(input):
    input_path = Path(input)
    if not input_path.exists():
        raise FileNotFoundError(f"[agent_b] 入力ファイルが存在しません: {input_path}")

    prompt = f"""以下の内容を読んで、AIエージェント市場の傾向を簡単に分析し、ポイントを3つにまとめてください。

===内容ここから===
{input_path.read_text()}
===内容ここまで===
"""

    desktop = Path.home() / "Desktop"
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = desktop / f"agentflow_trend_analysis_{timestamp}.txt"

    print("[agent_b] Gemini CLI による分析中...")

    process = subprocess.Popen(
        ["npx", "https://github.com/google-gemini/gemini-cli"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    stdout, _ = process.communicate(prompt)
    output_path.write_text(stdout)
    print(f"[agent_b] 分析結果を保存しました: {output_path}")
    return str(output_path)
