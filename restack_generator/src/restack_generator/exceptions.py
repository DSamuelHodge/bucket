# src/restack_generator/exceptions.py

class GeneratorError(Exception):
    """Base exception for generator errors."""
    pass


class ValidationError(GeneratorError):
    """Raised when component validation fails."""
    pass


class LLMError(GeneratorError):
    """Raised when LLM interaction fails."""
    pass


class TemplateError(GeneratorError):
    """Raised when template rendering fails."""
    pass