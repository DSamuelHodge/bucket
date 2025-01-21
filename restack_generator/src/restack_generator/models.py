# Pydantic models

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RestackConfig(BaseModel):
    """Configuration for the Restack generator."""
    
    lm_model: str = Field(
        default="llama3.1-8b",
        description="Cerebras LLM model to use for code generation"
    )
    max_tokens: int = Field(
        default=3000,
        description="Maximum tokens for LLM response"
    )
    temperature: float = Field(
        default=0.7,
        description="LLM temperature parameter"
    )
    api_key: Optional[str] = Field(
        default=None,
        description="API key for LLM service"
    )
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context for generation"
    )


class ComponentSpec(BaseModel):
    """Base class for component specifications."""
    
    name: str = Field(..., description="Component name")
    description: str = Field(..., description="Component description")
    input_schema: Dict[str, Any] = Field(
        ...,
        description="Input schema specification"
    )
    output_schema: Dict[str, Any] = Field(
        ...,
        description="Output schema specification"
    )
    retry_policy: Optional[Dict[str, Any]] = Field(
        None,
        description="Retry policy configuration"
    )
    timeout: Optional[str] = Field(
        None,
        description="Execution timeout (e.g., '30m')"
    )


class WorkflowSpec(ComponentSpec):
    """Specification for a workflow component."""
    
    steps: List[Dict[str, Any]] = Field(
        ...,
        description="Workflow steps specification"
    )


class FunctionSpec(ComponentSpec):
    """Specification for a function component."""
    
    dependencies: List[str] = Field(
        default_factory=list,
        description="Required function dependencies"
    )
