# src/restack_generator/core/base.py

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict

import jinja2
from pydantic import BaseModel

from ..models import RestackConfig
from ..exceptions import GeneratorError
from .llm import LLMClient


class BaseGenerator(ABC):
    """Base class for all Restack generators."""

    def __init__(self, config: RestackConfig):
        """Initialize generator with configuration."""
        self.config = config
        self.template_dir = Path(__file__).parent.parent / "templates"
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.llm_client = LLMClient(config)

    @abstractmethod
    async def generate_component(self, spec: BaseModel) -> str:
        """Generate a Restack component from specification.
        
        Args:
            spec: Component specification as a Pydantic model
            
        Returns:
            Generated component code as a string
            
        Raises:
            GeneratorError: If generation fails
        """
        pass

    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a Jinja2 template with the given context.
        
        Args:
            template_name: Name of template file
            context: Template context dictionary
            
        Returns:
            Rendered template as string
            
        Raises:
            GeneratorError: If template rendering fails
        """
        try:
            template = self.env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            raise GeneratorError(f"Failed to render template {template_name}: {str(e)}")

    def _validate_spec(self, spec: BaseModel) -> None:
        """Validate component specification.
        
        Args:
            spec: Component specification to validate
            
        Raises:
            GeneratorError: If validation fails
        """
        try:
            spec_dict = spec.model_dump()
            # Add custom validation logic here
            required_fields = ["name", "description"]
            missing = [f for f in required_fields if f not in spec_dict]
            if missing:
                raise ValueError(f"Missing required fields: {', '.join(missing)}")
        except Exception as e:
            raise GeneratorError(f"Invalid component specification: {str(e)}")