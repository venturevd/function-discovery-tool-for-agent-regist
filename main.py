import argparse
import importlib
import json
import sys
from typing import List, Any

class FunctionRegistry:
    """A registry for discovering and executing callable functions."""

    def __init__(self, registry_path: str) -> None:
        """
        Initialize the function registry.

        Args:
            registry_path: Path to the registry JSON file.
        """
        self.registry_path = registry_path
        self.registry = self._load_registry()

    def _load_registry(self) -> dict:
        """Load and validate the registry from a JSON file."""
        try:
            with open(self.registry_path, 'r') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            print(f"Error: Registry file '{self.registry_path}' not found.", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in registry file '{self.registry_path}': {e}", file=sys.stderr)
            sys.exit(1)

    def discover_functions(self) -> None:
        """Discover and print available functions in the registry."""
        if "functions" not in self.registry:
            print("Error: Registry does not contain 'functions' key.", file=sys.stderr)
            sys.exit(1)

        print("Available functions:")
        for func_name, func_info in self.registry["functions"].items():
            print(f"  - {func_name}: {func_info['module']}.{func_info['function']}")

    def execute_function(self, function_name: str, args: List[Any]) -> None:
        """
        Execute a function from the registry with the given arguments.

        Args:
            function_name: Name of the function to execute.
            args: List of arguments to pass to the function.
        """
        if "functions" not in self.registry:
            print("Error: Registry does not contain 'functions' key.", file=sys.stderr)
            sys.exit(1)

        if function_name not in self.registry["functions"]:
            print(f"Error: Function '{function_name}' not found in registry.", file=sys.stderr)
            sys.exit(1)

        func_info = self.registry["functions"][function_name]
        module_name = func_info["module"]
        func_name = func_info["function"]

        try:
            module = importlib.import_module(module_name)
            func = getattr(module, func_name)
        except ImportError:
            print(f"Error: Could not import module '{module_name}'.", file=sys.stderr)
            sys.exit(1)
        except AttributeError:
            print(f"Error: Function '{func_name}' not found in module '{module_name}'.", file=sys.stderr)
            sys.exit(1)

        try:
            result = func(*args)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error executing function: {type(e).__name__}: {e}", file=sys.stderr)
            sys.exit(1)

def _parse_arguments(args_list: List[str]) -> List[Any]:
    """
    Parse string arguments into appropriate Python types.

    Args:
        args_list: List of string arguments.

    Returns:
        List of arguments converted to appropriate types (int, float, or str).

    Raises:
        ValueError: If an argument cannot be parsed or is malformed.
    """
    if not args_list:
        raise ValueError("No arguments provided for function execution.")

    parsed_args = []
    for arg in args_list:
        # Try to convert to int first, then float, then leave as string
        try:
            parsed_args.append(int(arg))
        except ValueError:
            try:
                parsed_args.append(float(arg))
            except ValueError:
                parsed_args.append(arg)
    return parsed_args

def main() -> None:
    """Main entry point for the function discovery and execution tool."""
    parser = argparse.ArgumentParser(
        description="Function discovery and execution tool for agent registries."
    )
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
        try:
            args_list = _parse_arguments(args.args or [])
        except ValueError as e:
            print(f"Error parsing arguments: {e}", file=sys.stderr)
            sys.exit(1)

        registry.execute_function(args.function, args_list)

if __name__ == "__main__":
    main()