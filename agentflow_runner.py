import yaml
import importlib
import subprocess
import sys
import os
from pathlib import Path

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
    # 追加する場合はここに追記
}

# ステップ実行ロジック
def run_step(step):
    step_id = step.get("id")
    handler = step.get("handler")
    input_data = resolve_input(step.get("input"))

    if handler not in handler_map:
        raise NotImplementedError(f"Handler '{handler}' is not supported yet.")
    
    output = handler_map[handler](step, step_id, input_data)
    step_outputs[step_id] = output
    print(f"[{step_id}] Output: {output}")

# メイン関数
def main(yaml_path):
    with open(yaml_path, "r") as f:
        flow = yaml.safe_load(f)
    
    steps = flow.get("steps", [])
    for step in steps:
        run_step(step)

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
