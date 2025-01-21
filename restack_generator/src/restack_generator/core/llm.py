import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

from ..models import RestackConfig
from ..exceptions import LLMError

# Load environment variables from .env file
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)

class LLMClient:
    """Cerebras LLM client for code generation."""
    
    AVAILABLE_MODELS = ["llama3.1-8b", "llama-3.3-70b"]
    
    def __init__(self, config: RestackConfig):
        """Initialize LLM client with configuration."""
        self.config = config
        api_key = config.api_key or os.getenv("CEREBRAS_API_KEY")
        if not api_key:
            raise LLMError("No API key provided for Cerebras service (CEREBRAS_API_KEY)")
        
        try:
            self.client = Cerebras(api_key=api_key)
            # Validate the model exists
            if self.config.lm_model not in self.AVAILABLE_MODELS:
                available_models = self.list_available_models()
                raise LLMError(
                    f"Invalid model: {self.config.lm_model}. "
                    f"Available models: {', '.join(available_models)}"
                )
        except Exception as e:
            raise LLMError(f"Failed to initialize Cerebras client: {str(e)}")

    def list_available_models(self) -> list[str]:
        """List available Cerebras models."""
        try:
            response = self.client.models.list()
            return [model["id"] for model in response]
        except Exception as e:
            raise LLMError(f"Failed to list models: {str(e)}")

    async def generate(self, prompt: str) -> str:
        """Generate code using the Cerebras LLM.
        
        Args:
            prompt: Detailed prompt for code generation
            
        Returns:
            Generated code as string
            
        Raises:
            LLMError: If generation fails
        """
        try:
            system_prompt = (
                "Write code in python that follows the Temporal framework, "
                "without any additional explanation or comments, only return code, avoid using ```python``` tag, identifier."
            )
            
            full_prompt = f"{system_prompt}\n\n{prompt}"
            
            # Make the API call to Cerebras using the correct parameters
            response = self.client.completions.create(
                model=self.config.lm_model,
                prompt=full_prompt,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                stop=None  # Optional: Add stop sequences if needed
            )
            
            if not response or not hasattr(response, 'choices') or not response.choices:
                raise LLMError("No response received from Cerebras API")
                
            print(response.choices[0].text.strip())
            return response.choices[0].text.strip()
            
        except Exception as e:
            raise LLMError(f"Failed to generate code: {str(e)}")

    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """Get information about a specific model.
        
        Args:
            model_id: The ID of the model to retrieve info for
            
        Returns:
            Dict containing model information
            
        Raises:
            LLMError: If retrieval fails
        """
        try:
            return self.client.models.retrieve(model_id)
        except Exception as e:
            raise LLMError(f"Failed to get model info for {model_id}: {str(e)}")