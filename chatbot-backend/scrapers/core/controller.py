"""
Scraper Controller Module

This module provides the central controller that manages all property scrapers
and coordinates the search process across multiple providers.
"""

from typing import List, Dict, Any, Optional
import asyncio
import logging
from .base import BaseScraper
from .schema import PropertyListing

logger = logging.getLogger(__name__)

class ScraperController:
    """
    Central controller for managing property scrapers.
    Coordinates search requests across multiple providers.
    """
    
    def __init__(self, scrapers: List[BaseScraper]):
        """
        Initialize the controller with a list of scrapers.
        
        Args:
            scrapers: List of initialized scraper instances
        """
        self.scrapers = scrapers
        self.active_scrapers = {}
        
    async def initialize(self):
        """Initialize all scrapers."""
        for scraper in self.scrapers:
            try:
                await scraper.initialize()
                self.active_scrapers[scraper.__class__.__name__] = scraper
            except Exception as e:
                logger.error(f"Failed to initialize scraper {scraper.__class__.__name__}: {str(e)}")
    
    async def cleanup(self):
        """Clean up all scrapers."""
        for scraper in self.active_scrapers.values():
            try:
                await scraper.cleanup()
            except Exception as e:
                logger.error(f"Failed to cleanup scraper {scraper.__class__.__name__}: {str(e)}")
    
    async def search(self, criteria: Dict[str, Any], max_results: Optional[int] = None) -> List[PropertyListing]:
        """
        Search for properties across all active scrapers.
        
        Args:
            criteria: Dictionary containing search criteria
            max_results: Maximum number of results to return per scraper
            
        Returns:
            List of PropertyListing objects
        """
        if not self.active_scrapers:
            logger.warning("No active scrapers available")
            return []
        
        # Create search tasks for each scraper
        tasks = []
        for scraper_name, scraper in self.active_scrapers.items():
            try:
                # Add max_results to criteria if specified
                search_criteria = criteria.copy()
                if max_results:
                    search_criteria["max_results"] = max_results
                
                task = asyncio.create_task(scraper.search(search_criteria))
                tasks.append((scraper_name, task))
            except Exception as e:
                logger.error(f"Failed to create search task for {scraper_name}: {str(e)}")
        
        # Wait for all tasks to complete
        results = []
        for scraper_name, task in tasks:
            try:
                scraper_results = await task
                results.extend(scraper_results)
            except Exception as e:
                logger.error(f"Search failed for {scraper_name}: {str(e)}")
        
        # Sort results by price if available
        results.sort(key=lambda x: x.price.amount)
        
        return results
    
    async def get_listing_details(self, listing_id: str, source: str) -> Optional[PropertyListing]:
        """
        Get detailed information about a specific listing.
        
        Args:
            listing_id: Unique identifier for the listing
            source: Name of the scraper that has this listing
            
        Returns:
            PropertyListing object if found, None otherwise
        """
        if source not in self.active_scrapers:
            logger.error(f"Scraper {source} not found")
            return None
            
        try:
            return await self.active_scrapers[source].get_listing_details(listing_id)
        except Exception as e:
            logger.error(f"Failed to get listing details from {source}: {str(e)}")
            return None
    
    def get_active_scrapers(self) -> List[str]:
        """
        Get list of active scraper names.
        
        Returns:
            List of scraper names
        """
        return list(self.active_scrapers.keys())
    
    def get_scraper_status(self) -> Dict[str, bool]:
        """
        Get status of all scrapers.
        
        Returns:
            Dictionary mapping scraper names to their active status
        """
        return {
            scraper_name: True
            for scraper_name in self.active_scrapers
        } 