import subprocess
from pathlib import Path
import datetime

def run(input):
    prompt = "2026年のAIエージェント市場規模の予測をして"

    desktop = Path.home() / "Desktop"
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = desktop / f"agentflow_market_forecast_{timestamp}.txt"

    print("[agent_a] Gemini CLI を起動してプロンプトを送信中...")

    process = subprocess.Popen(
        ["npx", "https://github.com/google-gemini/gemini-cli"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    stdout, _ = process.communicate(prompt)
    output_path.write_text(stdout)

    print(f"[agent_a] 出力完了: {output_path}")
    return str(output_path)
