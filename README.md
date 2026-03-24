# Function Discovery Tool for Agent Registries

This tool enables agents to discover callable functions in a registry and execute them with execution guarantees. It provides a standardized way to discover, validate, and invoke functions registered in a JSON configuration file.

## Features

- **Discover available functions** - List all registered functions with their module and function names
- **Execute functions with guarantees** - Reliable function invocation with proper error handling
- **Automatic argument type conversion** - String arguments are converted to int/float as appropriate
- **Structured registry format** - Clear JSON schema for function definitions
- **Execution guarantees** - Fail-fast error handling with descriptive exit codes

## Dependencies

This tool requires **Python 3.6 or higher** with only standard library dependencies:
- `argparse` - Command-line argument parsing
- `importlib` - Dynamic module loading
- `json` - Registry file parsing
- `sys` - Error output and exit handling
- `typing` - Type hints (optional, for development)

No external pip packages are required.

## File Structure

```
project/
├── main.py              # Main CLI tool (this repository)
├── registry.json        # Function registry configuration
├── math_operations.py   # Example module with callable functions
├── other_module.py      # Additional function modules (optional)
└── README.md           # This file
```

### Registry JSON Structure

The registry file must be a JSON object with a `"functions"` key containing function definitions:

```json
{
  "functions": {
    "function_name": {
      "module": "module_name_without_py",
      "function": "function_name_in_module",
      "args": ["type1", "type2"],
      "returns": "return_type"
    }
  }
}
```

**Requirements:**
- `module`: The Python module name (without `.py`), must be in the same directory or importable
- `function`: The exact function name within that module
- `args`: An array describing expected argument types (informational, not enforced)
- `returns`: The expected return type (informational, not enforced)

**Example `registry.json`:**
```json
{
  "functions": {
    "add": {
      "module": "math_operations",
      "function": "add",
      "args": ["int", "int"],
      "returns": "int"
    },
    "greet": {
      "module": "greeting",
      "function": "say_hello",
      "args": ["str"],
      "returns": "str"
    }
  }
}
```

### Function Module Structure

Function modules should expose callable functions at module level. The tool does not enforce any specific interface beyond being callable.

**Example `math_operations.py`:**
```python
def add(a: int, b: int) -> int:
    """Add two numbers and return the sum."""
    return a + b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b
```

## Usage

### Discover Available Functions

Lists all registered functions with their full import paths:

```bash
python3 main.py discover --registry ./registry.json
```

**Example output:**
```
Available functions:
  - add: math_operations.add
  - multiply: math_operations.multiply
```

### Execute a Function

Invoke a registered function with positional arguments:

```bash
python3 main.py execute --registry ./registry.json --function add --args 5 3
```

**Example output:**
```
Result: 8
```

### Supported Argument Types

Arguments are automatically converted:
- Whole numbers: `"42"` → `int(42)`
- Decimal numbers: `"3.14"` → `float(3.14)`
- All other strings: remain as `str`

Booleans (`true`/`false`), lists, or dicts are passed as strings and must be parsed by the function.

## Error Handling

The tool exits with non-zero status codes on errors:

| Code | Scenario |
|------|-----------|
| 1 | Registry file not found or invalid JSON |
| 1 | Missing `functions` key in registry |
| 1 | Specified function not found in registry |
| 1 | Module import failed |
| 1 | Function not found in module |
| 1 | Function execution error (exception raised) |
| 1 | Argument parsing error |

Errors are printed to `stderr`.

## Testing

### Basic Verification

Run the help command to verify installation:

```bash
python3 main.py --help
```

### Run Sample Operations

```bash
# Discover functions
python3 main.py discover --registry ./registry.json

# Execute math operations
python3 main.py execute --registry ./registry.json --function add --args 2 3
python3 main.py execute --registry ./registry.json --function subtract --args 10 4
python3 main.py execute --registry ./registry.json --function multiply --args 6 7
python3 main.py execute --registry ./registry.json --function divide --args 20 4
```

## Execution Guarantees

This tool guarantees:
1. **Registry integrity** - Valid JSON structure required at startup
2. **Function existence** - Validates function exists in registry before attempting import
3. **Module importability** - Reports import failures explicitly
4. **Type-safe invocation** - Arguments converted before function call
5. **Error isolation** - Function exceptions caught and reported without stack traces in success case
6. **Proper exit codes** - Zero on success, non-zero on any failure

## License

MIT