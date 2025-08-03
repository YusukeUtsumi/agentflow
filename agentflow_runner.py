import yaml
import importlib
import subprocess
import sys
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# モジュールパスの設定
sys.path.append(str(Path("templates").resolve().parent))

# ステップの出力を記憶する
step_outputs = {}

def resolve_input(raw_input):
    if isinstance(raw_input, str):
        for key, value in step_outputs.items():
            placeholder = f"{{{{{key}.output}}}}"
            raw_input = raw_input.replace(placeholder, str(value))
    return raw_input

# Pythonモジュール実行
def run_python(step, step_id, input_data):
    module_name = step.get("module")
    if not module_name:
        raise ValueError(f"Step {step_id}: 'module' is required for python handler.")
    
    module = importlib.import_module(module_name)
    if not hasattr(module, "run"):
        raise AttributeError(f"Module {module_name} must define a 'run(input)' function.")
    
    return module.run(input_data)

# シェルスクリプト（.sh）実行
def run_shell(step, step_id, input_data):
    script = step.get("script")
    if not script:
        raise ValueError(f"Step {step_id}: 'script' is required for shell handler.")
    
    result = subprocess.run(["sh", script, input_data], capture_output=True, text=True)
    return result.stdout.strip()

# JavaScriptファイル（Node.js）実行
def run_javascript(step, step_id, input_data):
    script = step.get("script")
    if not script:
        raise ValueError(f"Step {step_id}: 'script' is required for javascript handler.")
    
    result = subprocess.run(["node", script, input_data], capture_output=True, text=True)
    return result.stdout.strip()

# handler種別をマッピング
handler_map = {
    "python": run_python,
    "shell": run_shell,
    "javascript": run_javascript,
}

# ステップ実行ロジック（エラーハンドリング追加）
def run_step(step):
    step_id = step.get("id")
    handler = step.get("handler")
    input_data = resolve_input(step.get("input"))

    print(f"[{step_id}] ▶ Starting (handler: {handler})")

    if handler not in handler_map:
        print(f"[{step_id}] ❌ Error: Handler '{handler}' is not supported.")
        sys.exit(1)

    try:
        output = handler_map[handler](step, step_id, input_data)
        step_outputs[step_id] = output
        print(f"[{step_id}] ✅ Output: {output}")
    except Exception as e:
        print(f"[{step_id}] ❌ Error: {type(e).__name__}: {str(e)}")
        sys.exit(1)

# 並列ステップ実行
def run_parallel_steps(steps):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_step, step) for step in steps]
        for future in futures:
            future.result()  # 全て完了するまで待つ

# メイン関数（parallel対応）
def main(yaml_path):
    with open(yaml_path, "r") as f:
        flow = yaml.safe_load(f)
    
    steps = flow.get("steps", [])
    parallel_batch = []

    for step in steps:
        if step.get("parallel", False):
            parallel_batch.append(step)
        else:
            if parallel_batch:
                run_parallel_steps(parallel_batch)
                parallel_batch = []
            run_step(step)

    if parallel_batch:
        run_parallel_steps(parallel_batch)

# CLI起動
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agentflow_runner.py path/to/flow.yaml")
        sys.exit(1)
    
    yaml_path = Path(sys.argv[1])
    if not yaml_path.exists():
        print(f"YAML file not found: {yaml_path}")
        sys.exit(1)
    
    main(str(yaml_path))
