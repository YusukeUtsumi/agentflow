import yaml
import importlib
import sys
from pathlib import Path
sys.path.append(str(Path("templates").resolve().parent))

# Store outputs of each step
step_outputs = {}

def resolve_input(raw_input):
    # Replace {{step_id.output}} with actual output
    if isinstance(raw_input, str):
        for key, value in step_outputs.items():
            placeholder = f"{{{{{key}.output}}}}"
            raw_input = raw_input.replace(placeholder, str(value))
    return raw_input

def run_step(step):
    step_id = step.get("id")
    handler = step.get("handler")
    input_data = resolve_input(step.get("input"))

    if handler == "python":
        module_name = step.get("module")
        if not module_name:
            raise ValueError(f"Step {step_id}: 'module' is required for python handler.")
        
        # Import module dynamically
        module = importlib.import_module(module_name)

        # Call run(input)
        if not hasattr(module, "run"):
            raise AttributeError(f"Module {module_name} must define a 'run(input)' function.")
        
        output = module.run(input_data)
        step_outputs[step_id] = output
        print(f"[{step_id}] Output: {output}")

    else:
        raise NotImplementedError(f"Handler '{handler}' is not supported yet.")

def main(yaml_path):
    with open(yaml_path, "r") as f:
        flow = yaml.safe_load(f)

    steps = flow.get("steps", [])
    for step in steps:
        run_step(step)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agentflow_runner.py path/to/flow.yaml")
        sys.exit(1)
    
    yaml_path = Path(sys.argv[1])
    if not yaml_path.exists():
        print(f"YAML file not found: {yaml_path}")
        sys.exit(1)

    main(str(yaml_path))
