#!/usr/bin/env python3
"""
Test script for the property scrapers module.
This script demonstrates how to use the scrapers to search for properties.
"""

import asyncio
import logging
import sys
import os
from typing import Dict, Any
from datetime import datetime

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import from the package
from scrapers.providers.rightmove import RightmoveScraper
from scrapers.core.controller import ScraperController

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO to DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_scrapers():
    """Test the property scrapers."""
    try:
        # Initialize scrapers
        logger.info("Initializing scrapers...")
        rightmove = RightmoveScraper()
        controller = ScraperController([rightmove])
        await controller.initialize()
        
        # Test search
        logger.info("Testing property search...")
        search_criteria = {
            "location": "London",
            "price_min": 300000,
            "price_max": 500000,
            "bedrooms_min": 2,
            "property_type": "houses"
        }
        
        logger.info(f"Searching for properties with criteria: {search_criteria}")
        results = await controller.search(search_criteria)
        
        if results:
            logger.info(f"Found {len(results)} properties")
            for listing in results[:5]:  # Show first 5 results
                logger.info(f"Property: {listing.title}")
                logger.info(f"Price: £{listing.price.amount:,.2f}")
                logger.info(f"Location: {listing.location.address}")
                logger.info(f"URL: {listing.url}")
                logger.info("---")
        else:
            logger.warning("No properties found matching the criteria")
            
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
    finally:
        # Cleanup
        await controller.cleanup()

async def test_listing_details(listing_id: str) -> None:
    """
    Test fetching detailed information for a specific property listing.
    
    Args:
        listing_id: The ID of the listing to fetch details for
    """
    try:
        # Initialize scrapers
        logger.info("Initializing scrapers...")
        scrapers = [RightmoveScraper()]
        controller = ScraperController(scrapers)
        
        # Initialize the controller
        await controller.initialize()
        
        # Get listing details
        logger.info(f"Fetching details for listing: {listing_id}")
        listing = await controller.get_listing_details(listing_id)
        
        if listing:
            print("\n" + "="*50)
            print(f"Title: {listing.title}")
            print(f"Price: £{listing.price.amount:,.2f}")
            print(f"Location: {listing.location.address}")
            print(f"Description: {listing.description[:200]}...")
            print(f"Features: {listing.features}")
            print(f"Images: {len(listing.images)} available")
            print("="*50)
        else:
            logger.warning(f"No listing found with ID: {listing_id}")
            
    except Exception as e:
        logger.error(f"Error fetching listing details: {str(e)}")
        raise
    finally:
        # Clean up
        await controller.cleanup()

async def main() -> None:
    """
    Main function to run the tests.
    """
    try:
        # Test property search
        print("\nTesting property search...")
        await test_scrapers()
        
        # Test listing details (uncomment and provide a valid listing ID)
        # print("\nTesting listing details...")
        # await test_listing_details("your_listing_id_here")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main()) 