import argparse
import importlib
import json
import sys

class FunctionRegistry:
    def __init__(self, registry_path):
        self.registry_path = registry_path
        self.registry = self._load_registry()

    def _load_registry(self):
        """Load the registry from a JSON file."""
        try:
            with open(self.registry_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Registry file '{self.registry_path}' not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in registry file '{self.registry_path}'.")
            sys.exit(1)

    def discover_functions(self):
        """Discover and print available functions in the registry."""
        if "functions" not in self.registry:
            print("Error: Registry does not contain 'functions' key.")
            sys.exit(1)

        print("Available functions:")
        for func_name, func_info in self.registry["functions"].items():
            print(f"  - {func_name}: {func_info['module']}.{func_info['function']}")

    def execute_function(self, function_name, args):
        """Execute a function from the registry with the given arguments."""
        if "functions" not in self.registry:
            print("Error: Registry does not contain 'functions' key.")
            sys.exit(1)

        if function_name not in self.registry["functions"]:
            print(f"Error: Function '{function_name}' not found in registry.")
            sys.exit(1)

        func_info = self.registry["functions"][function_name]
        module_name = func_info["module"]
        func_name = func_info["function"]

        try:
            module = importlib.import_module(module_name)
            func = getattr(module, func_name)
        except ImportError:
            print(f"Error: Could not import module '{module_name}'.")
            sys.exit(1)
        except AttributeError:
            print(f"Error: Function '{func_name}' not found in module '{module_name}'.")
            sys.exit(1)

        try:
            result = func(*args)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error executing function: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Function discovery and execution tool for agent registries.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Discover command
    discover_parser = subparsers.add_parser("discover", help="Discover available functions in the registry")
    discover_parser.add_argument("--registry", required=True, help="Path to the registry JSON file")

    # Execute command
    execute_parser = subparsers.add_parser("execute", help="Execute a function from the registry")
    execute_parser.add_argument("--registry", required=True, help="Path to the registry JSON file")
    execute_parser.add_argument("--function", required=True, help="Name of the function to execute")
    execute_parser.add_argument("--args", nargs=argparse.REMAINDER, help="Arguments to pass to the function")

    args = parser.parse_args()

    registry = FunctionRegistry(args.registry)

    if args.command == "discover":
        registry.discover_functions()
    elif args.command == "execute":
        if not args.args:
            print("Error: No arguments provided for function execution.")
            sys.exit(1)

        # Convert argument strings to appropriate types
        try:
            args_list = []
            for arg in args.args:
                # Try to convert to int first, then float, then leave as string
                try:
                    args_list.append(int(arg))
                except ValueError:
                    try:
                        args_list.append(float(arg))
                    except ValueError:
                        args_list.append(arg)
        except Exception as e:
            print(f"Error parsing arguments: {e}")
            sys.exit(1)

        registry.execute_function(args.function, args_list)

if __name__ == "__main__":
    main()