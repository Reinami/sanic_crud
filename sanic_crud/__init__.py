from .collection_resource import BaseCollectionResource
from .single_resource import BaseResource
from .crud_generation import generate_crud

__version__ = '0.1.0'

__all__ = ['BaseCollectionResource', 'BaseResource', 'generate_crud']