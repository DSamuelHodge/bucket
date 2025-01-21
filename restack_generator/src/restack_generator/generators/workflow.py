from typing import Dict, Any
import logging

from ..core.base import BaseGenerator
from ..models import WorkflowSpec, RestackConfig
from ..exceptions import GeneratorError

logger = logging.getLogger(__name__)

class WorkflowGenerator(BaseGenerator):
    """Generator for Restack workflow components."""
    
    def __init__(self, config: RestackConfig):
        super().__init__(config)
        self.name = "WorkflowGenerator"

    async def generate_component(self, spec: WorkflowSpec) -> str:
        """Generate a workflow component from specification."""
        # Validate the specification
        self._validate_spec(spec)
        
        # Create prompt for code generation
        prompt = self._create_prompt(spec)
        logger.debug(f"Generated prompt:\n{prompt}")
        
        try:
            # Generate implementation code using LLM
            logger.debug("Calling LLM for code generation...")
            implementation = await self.llm_client.generate(prompt)
            logger.debug(f"Received implementation:\n{implementation}")
            
            if not implementation or len(implementation.strip()) == 0:
                raise GeneratorError("Received empty implementation from LLM")
            
            # Prepare template context
            context = {
                "name": spec.name,
                "description": spec.description,
                "input_schema": spec.input_schema,
                "output_schema": spec.output_schema,
                "code": implementation,
            }
            
            logger.debug("Rendering template with context...")
            result = self.render_template("workflow.py.j2", context)
            logger.debug(f"Generated result:\n{result}")
            
            if not result or len(result.strip()) == 0:
                raise GeneratorError("Template rendering produced empty result")
                
            return result
            
        except Exception as error:
            logger.error(f"Error during generation: {str(error)}")
            raise GeneratorError(f"Failed to generate workflow: {str(error)}")

    def _create_prompt(self, spec: WorkflowSpec) -> str:
        """Create a detailed prompt for the LLM."""
        return f"""
Please generate a Python implementation for a Restack workflow with these specifications:

Workflow Name: {spec.name}
Description: {spec.description}

Input Schema:
{spec.input_schema}

Output Schema:
{spec.output_schema}

Steps to implement:
{spec.steps}

Requirements:
1. Use @workflow.run decorator for the main execution method
2. Implement proper error handling and retries
3. Add logging at key execution points
4. Handle async operations correctly
5. Return data matching the output schema exactly
6. Implement each workflow step in sequence

Example format:
```python
@workflow.run
async def run(self, input: DataProcessorInput) -> DataProcessorOutput:
    self.logger.info("Starting workflow execution")
    try:
        # Workflow implementation here
        pass
    except Exception as error:
        self.logger.error(f"Workflow failed: {{str(error)}}")
        raise
```

Generate only the implementation code, not the class definition or imports.
"""