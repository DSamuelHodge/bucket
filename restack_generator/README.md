# Restack Workflow Generator

A context-aware code generator for creating Restack workflow components using Large Language Models.

## Overview

Restack Workflow Generator is a tool that automates the creation of Restack workflow components by leveraging the power of Large Language Models. It takes workflow specifications in YAML format and generates production-ready Python code with proper error handling, logging, and best practices.

## Features

- 🚀 Context-aware code generation
- 📝 YAML-based workflow specifications
- 🔧 Customizable templates using Jinja2
- 🤖 Integration with Cerebras LLM models
- 📊 Built-in logging and monitoring
- ⚡ Async/await support
- 🛠️ Proper error handling and validation

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/restack_generator.git
cd restack_generator

# Install with Poetry
poetry install
```

## Quick Start

1. Set up your environment:
```bash
# Set your Cerebras API key
export CEREBRAS_API_KEY='your-api-key-here'
```

2. Create a workflow specification (example.yaml):
```yaml
name: DataProcessor
description: "A simple workflow that processes input data"

input_schema:
  data:
    type: Dict[str, Any]
    description: "Input data to process"
    
output_schema:
  processed_data:
    type: Dict[str, Any]
    description: "Processed output data"

steps:
  - name: validate
    type: function
    function: data_validation
```

3. Generate your workflow:
```bash
poetry run restack-generator generate example.yaml
```

## Project Structure

```
restack_generator/
├── src/
│   └── restack_generator/
│       ├── cli/          # Command-line interface
│       ├── core/         # Core functionality
│       ├── generators/   # Component generators
│       └── templates/    # Jinja2 templates
├── tests/               # Test suite
└── examples/           # Example specifications
```

## Configuration

The generator can be configured through:
- Environment variables
- Command-line options
- Configuration files

See the [documentation](docs/configuration.md) for more details.

## Development

```bash
# Install development dependencies
poetry install --with dev

# Run tests
poetry run pytest

# Run with verbose logging
poetry run restack-generator generate example.yaml --verbose
```

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.