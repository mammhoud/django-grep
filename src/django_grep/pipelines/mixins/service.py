"""
Service mixins for models.
"""

from typing import Any, Dict, Type

from django.db import models

from ..services.base import BaseService, ServiceRegistry


class ServiceMixin:
    """
    Mixin to add service layer to models.
    """
    
    @classmethod
    def get_service_class(cls) -> Type[BaseService]:
        """
        Get service class for this model.
        """
        # Check registry first
        service_name = f"{cls.__name__.lower()}_service"
        service_class = ServiceRegistry.get(service_name)
        
        if service_class:
            return service_class
        
        # Create dynamic service
        from ..services.base import ModelService
        
        class DynamicService(ModelService):
            model_class = cls
        
        return DynamicService
    
    @classmethod
    def get_service(cls) -> BaseService:
        """Get service instance."""
        service_class = cls.get_service_class()
        return service_class(model_class=cls)
    
    def get_service_instance(self) -> BaseService:
        """Get service instance for this object."""
        return self.get_service()
    
    def save_with_service(self, data: Dict[str, Any], **kwargs) -> models.Model:
        """
        Save using service layer.
        """
        service = self.get_service()
        
        if self.pk is None:
            # Create new
            success, obj, message = service.create(data, **kwargs)
        else:
            # Update existing
            success, obj, message = service.update(self.pk, data, **kwargs)
        
        if not success:
            raise ValueError(f"Service operation failed: {message}")
        
        return obj
    
    def delete_with_service(self, **kwargs) -> bool:
        """
        Delete using service layer.
        """
        service = self.get_service()
        return service.delete(self.pk, **kwargs)
    
    def refresh_from_service(self, **kwargs) -> models.Model:
        """
        Refresh object from service.
        """
        service = self.get_service()
        obj = service.get(self.pk, **kwargs)
        
        if not obj:
            raise self.DoesNotExist(f"Object {self.pk} not found")
        
        # Update self with object data
        for field in self._meta.fields:
            if field.name != 'id':
                setattr(self, field.name, getattr(obj, field.name))
        
        return self