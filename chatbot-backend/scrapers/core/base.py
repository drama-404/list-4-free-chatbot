"""
Base Scraper Module

This module defines the base scraper class that all provider-specific scrapers
will inherit from. It provides common functionality and defines the interface
that all scrapers must implement.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import logging
from .schema import PropertyListing
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """
    Base class for all property scrapers.
    Defines the interface and common functionality that all scrapers must implement.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the scraper with optional configuration.
        
        Args:
            config: Dictionary containing scraper-specific configuration
        """
        self.config = config or {}
        self.session = None
        self.last_request_time = None
        self.min_request_delay = 1.0  # Minimum delay between requests in seconds
        
    @abstractmethod
    async def search(self, criteria: Dict[str, Any]) -> List[PropertyListing]:
        """
        Search for properties matching the given criteria.
        
        Args:
            criteria: Dictionary containing search criteria
                {
                    "location": str,
                    "price_min": float,
                    "price_max": float,
                    "bedrooms_min": int,
                    "bedrooms_max": int,
                    "property_type": str,
                    "max_results": int
                }
        
        Returns:
            List of PropertyListing objects
        """
        pass
    
    @abstractmethod
    async def get_listing_details(self, listing_id: str) -> Optional[PropertyListing]:
        """
        Get detailed information about a specific listing.
        
        Args:
            listing_id: Unique identifier for the listing
            
        Returns:
            PropertyListing object if found, None otherwise
        """
        pass
    
    async def cleanup(self):
        """Clean up resources used by the scraper."""
        if self.session:
            await self.session.close()
    
    def _validate_criteria(self, criteria: Dict[str, Any]) -> bool:
        """
        Validate search criteria.
        
        Args:
            criteria: Dictionary containing search criteria
            
        Returns:
            bool: True if criteria are valid, False otherwise
        """
        required_fields = ["location"]
        return all(field in criteria for field in required_fields)
    
    def _normalize_price(self, price_str: str) -> float:
        """
        Normalize price string to float.
        
        Args:
            price_str: Price string (e.g., "£500,000")
            
        Returns:
            float: Normalized price
        """
        try:
            # Remove currency symbols, commas, and whitespace
            price_str = price_str.replace("£", "").replace(",", "").strip()
            return float(price_str)
        except (ValueError, AttributeError):
            logger.error(f"Failed to normalize price: {price_str}")
            return 0.0
    
    def _normalize_bedrooms(self, bedrooms_str: str) -> Optional[int]:
        """
        Normalize bedrooms string to integer.
        
        Args:
            bedrooms_str: Bedrooms string (e.g., "3")
            
        Returns:
            Optional[int]: Normalized number of bedrooms
        """
        try:
            return int(bedrooms_str)
        except (ValueError, TypeError):
            logger.error(f"Failed to normalize bedrooms: {bedrooms_str}")
            return None
    
    def _get_timestamp(self) -> datetime:
        """Get current timestamp."""
        return datetime.utcnow()
    
    async def _make_request(self, url: str, method: str = "GET", expect_json: bool = False, **kwargs) -> Optional[Union[Dict[str, Any], str]]:
        """
        Make HTTP request with rate limiting and error handling.
        
        Args:
            url: URL to request
            method: HTTP method
            expect_json: Whether to expect JSON response
            **kwargs: Additional arguments for the request
            
        Returns:
            Optional[Union[Dict[str, Any], str]]: Response data if successful, None otherwise
        """
        if not self.session:
            raise RuntimeError("Session not initialized")
            
        try:
            # Implement rate limiting
            if self.last_request_time:
                delay = self.min_request_delay - (datetime.utcnow() - self.last_request_time).total_seconds()
                if delay > 0:
                    await asyncio.sleep(delay)
            
            async with self.session.request(method, url, **kwargs) as response:
                self.last_request_time = datetime.utcnow()
                response.raise_for_status()
                
                if expect_json:
                    return await response.json()
                else:
                    return await response.text()
                
        except aiohttp.ClientError as e:
            logger.error(f"Request failed: {url} - {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during request: {url} - {str(e)}")
            return None 