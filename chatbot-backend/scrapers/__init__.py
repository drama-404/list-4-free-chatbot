"""
Property Scrapers Package

This package provides a modular framework for scraping property listings
from various UK property websites. It includes a unified data schema,
base scraper class, and provider-specific implementations.

Components:
-----------
1. Core
   - schema.py: Unified property data schema
   - base.py: Base scraper class
   - controller.py: Central scraper controller

2. Providers
   - rightmove.py: Rightmove.co.uk scraper
   - (future) zoopla.py: Zoopla.co.uk scraper
   - (future) onthemarket.py: OnTheMarket.com scraper

3. Utils
   - (future) proxy.py: Proxy management
   - (future) rate_limiter.py: Rate limiting utilities
"""

from .core.schema import (
    PropertyListing,
    PropertyLocation,
    PropertyFeatures,
    PropertyPrice
)

from .core.base import BaseScraper
from .core.controller import ScraperController
from .providers.rightmove import RightmoveScraper

__all__ = [
    # Schema
    'PropertyListing',
    'PropertyLocation',
    'PropertyFeatures',
    'PropertyPrice',
    
    # Core
    'BaseScraper',
    'ScraperController',
    
    # Providers
    'RightmoveScraper'
] 