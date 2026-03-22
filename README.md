# Function Discovery Tool for Agent Registries

This tool enables agents to discover callable functions in a registry and execute them with execution guarantees.

## Features
- Discover available functions in a registry
- Execute functions with guaranteed execution
- Handle function execution errors gracefully

## Usage

### Discover Functions
```bash
python3 main.py discover --registry <registry_path>
```

### Execute a Function
```bash
python3 main.py execute --registry <registry_path> --function <function_name> [--args <arg1> <arg2> ...]
```

## Example

### Discover Functions
```bash
python3 main.py discover --registry ./registry.json
```

### Execute a Function
```bash
python3 main.py execute --registry ./registry.json --function add --args 2 3
```

## Registry Format

The registry is a JSON file with the following structure:

```json
{
  "functions": {
    "add": {
      "module": "math_operations",
      "function": "add",
      "args": ["int", "int"],
      "returns": "int"
    },
    "subtract": {
      "module": "math_operations",
      "function": "subtract",
      "args": ["int", "int"],
      "returns": "int"
    }
  }
}
```

## Development

### Requirements
- Python 3.6+

### Testing

Run tests with:
```bash
python3 -m unittest discover
```

### Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request