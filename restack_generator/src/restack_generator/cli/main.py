import asyncio
from pathlib import Path
import yaml
import tracemalloc
import sys
import logging

import click
from rich.console import Console

from ..models import RestackConfig, WorkflowSpec
from ..generators.workflow import WorkflowGenerator
from ..core.logging_config import setup_logging

console = Console()
logger = logging.getLogger(__name__)

def init_tracemalloc():
    """Initialize tracemalloc for memory tracking."""
    tracemalloc.start()

@click.group()
def cli():
    """Restack Generator CLI"""
    init_tracemalloc()

@cli.command()
@click.argument('spec_file', type=click.Path(exists=True))
@click.option('--output', '-o', default='generated',
              help='Output directory for generated code')
@click.option('--api-key', envvar='CEREBRAS_API_KEY',
              help='Cerebras API key (or set CEREBRAS_API_KEY env var)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def generate(spec_file: str, output: str, api_key: str, verbose: bool):
    """Generate Restack components from a specification file."""
    # Setup logging with appropriate level
    setup_logging("DEBUG" if verbose else "INFO")
    logger.info("Starting code generation process")
    
    try:
        asyncio.run(async_generate(spec_file, output, api_key))
    except Exception as e:
        logger.error(f"Error generating workflow: {str(e)}", exc_info=True)
        sys.exit(1)

async def async_generate(spec_file: str, output: str, api_key: str):
    """Asynchronous implementation of generate command."""
    try:
        logger.info(f"Loading specification from {spec_file}")
        with open(spec_file) as f:
            spec_data = yaml.safe_load(f)
        
        logger.debug(f"Loaded specification: {spec_data}")
        
        # Create config
        config = RestackConfig(api_key=api_key)
        logger.debug("Created RestackConfig")
        
        # Create generator
        generator = WorkflowGenerator(config)
        logger.debug("Created WorkflowGenerator")
        
        # Create output directory
        output_path = Path(output)
        output_path.mkdir(exist_ok=True)
        logger.debug(f"Created output directory: {output_path}")
        
        # Generate workflow
        spec = WorkflowSpec(**spec_data)
        logger.info("Generating workflow code...")
        code = await generator.generate_component(spec)
        
        # Write output
        output_file = output_path / f"{spec.name.lower()}_workflow.py"
        with open(output_file, 'w') as f:
            f.write(code)
            
        logger.info(f"Successfully generated workflow: {output_file}")
        console.print(f"[green]Successfully generated workflow: {output_file}[/green]")

        # Print memory statistics
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        stats_msg = "\nMemory usage (Top 3):"
        logger.debug(stats_msg)
        console.print(f"[yellow]{stats_msg}[/yellow]")
        for stat in top_stats[:3]:
            logger.debug(str(stat))
            console.print(f"[dim]{stat}[/dim]")
            
    except Exception as e:
        error_msg = f"Error in async_generate: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise

def main():
    """Entry point for the CLI."""
    cli()

if __name__ == '__main__':
    main()