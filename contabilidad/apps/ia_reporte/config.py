"""
Configuración para el sistema de IA de reportes.
"""
from django.conf import settings
import os


class IAConfig:
    """
    Configuración centralizada para el sistema de IA.
    """
    
    # Configuración de OpenAI
    OPENAI_API_KEY = getattr(settings, 'OPENAI_API_KEY', '')
    OPENAI_MODEL = getattr(settings, 'OPENAI_MODEL', 'gpt-3.5-turbo')
    OPENAI_TEMPERATURE = getattr(settings, 'OPENAI_TEMPERATURE', 0.1)
    OPENAI_MAX_TOKENS = getattr(settings, 'OPENAI_MAX_TOKENS', 1000)
    
    # Configuración de reportes
    MAX_CUENTAS_REPORTE = getattr(settings, 'IA_MAX_CUENTAS_REPORTE', 50)
    MAX_ASIENTOS_REPORTE = getattr(settings, 'IA_MAX_ASIENTOS_REPORTE', 100)
    
    # Configuración de fechas por defecto
    DEFAULT_YEAR = getattr(settings, 'IA_DEFAULT_YEAR', None)  # None = año actual
    
    @classmethod
    def is_openai_configured(cls):
        """
        Verifica si OpenAI está configurado correctamente.
        """
        return bool(cls.OPENAI_API_KEY and cls.OPENAI_API_KEY != '')
    
    @classmethod
    def get_contexto_empresa_limitado(cls):
        """
        Obtiene el límite de cuentas para el contexto de empresa.
        """
        return getattr(settings, 'IA_CONTEXTO_EMPRESA_LIMIT', 20)
