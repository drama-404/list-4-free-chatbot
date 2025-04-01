"""
Core package for the property scrapers.
Contains base classes and common functionality.
"""

from .base import BaseScraper
from .controller import ScraperController
from .schema import PropertyListing, PropertyLocation, PropertyFeatures, PropertyPrice

__all__ = [
    'BaseScraper',
    'ScraperController',
    'PropertyListing',
    'PropertyLocation',
    'PropertyFeatures',
    'PropertyPrice'
] 