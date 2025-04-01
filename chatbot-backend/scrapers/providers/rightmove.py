"""
Rightmove Scraper Module

This module implements the property scraper for Rightmove.co.uk.
"""

import logging
from typing import List, Dict, Any, Optional, Set
from datetime import datetime
from decimal import Decimal
import aiohttp
from bs4 import BeautifulSoup
from scrapers.core.base import BaseScraper
from scrapers.core.schema import PropertyListing, PropertyLocation, PropertyFeatures, PropertyPrice

logger = logging.getLogger(__name__)

class RightmoveScraper(BaseScraper):
    """
    Scraper implementation for Rightmove.co.uk.
    """
    
    BASE_URL = "https://www.rightmove.co.uk"
    SEARCH_URL = f"{BASE_URL}/property-for-sale/find.html"
    LISTING_URL = f"{BASE_URL}/properties"
    LOCATION_SEARCH_URL = f"{BASE_URL}/property-for-sale/location.html"
    
    # Common location identifiers
    LOCATION_IDS = {
        "London": "REGION^87490",
        "Manchester": "REGION^87491",
        "Birmingham": "REGION^87492",
        "Leeds": "REGION^87493",
        "Glasgow": "REGION^87494",
        "Liverpool": "REGION^87495",
        "Bristol": "REGION^87496",
        "Sheffield": "REGION^87497",
        "Edinburgh": "REGION^87498",
        "Cardiff": "REGION^87499"
    }
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Rightmove scraper.
        
        Args:
            config: Optional configuration dictionary
        """
        super().__init__(config)
        self.session = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
    
    def get_location_id(self, location: str) -> str:
        """
        Get the Rightmove location identifier for a given location name.
        
        Args:
            location: Location name (e.g., "London", "Manchester")
            
        Returns:
            Location identifier string
        """
        # Check common locations first
        if location in self.LOCATION_IDS:
            return self.LOCATION_IDS[location]
        
        # If not found, return the location as is (might be a custom identifier)
        return location
    
    async def initialize(self):
        """Initialize the scraper session."""
        self.session = aiohttp.ClientSession(headers=self.headers)
    
    async def search(self, criteria: Dict[str, Any]) -> List[PropertyListing]:
        """
        Search for properties on Rightmove.
        
        Args:
            criteria: Search criteria dictionary
            
        Returns:
            List of PropertyListing objects
        """
        if not self._validate_criteria(criteria):
            logger.error("Invalid search criteria")
            return []
        
        try:
            # Get location identifier
            location = criteria.get("location", "")
            location_id = self.get_location_id(location)
            
            # Update criteria with location ID
            criteria["location"] = location_id
            
            # Construct search URL
            search_params = self._build_search_params(criteria)
            url = f"{self.SEARCH_URL}?{search_params}"
            
            logger.info(f"Searching URL: {url}")
            
            # Get search results
            data = await self._make_request(url, expect_json=False)
            if not data:
                logger.error("No data received from request")
                return []
            
            # Parse results
            soup = BeautifulSoup(data, "lxml")
            
            # Debug: Log the HTML content
            logger.debug(f"Page content: {soup.prettify()[:1000]}...")  # First 1000 chars
            
            # Try different property card selectors
            property_cards = (
                soup.find_all("div", class_="propertyCard") or
                soup.find_all("div", class_="property-card") or
                soup.find_all("div", {"data-test": "property-card"}) or
                soup.find_all("div", {"class": "l-searchResult"})
            )
            
            logger.info(f"Found {len(property_cards)} property cards")
            
            if not property_cards:
                # Try to find the results container
                results_container = soup.find("div", {"class": "l-searchResults"})
                if results_container:
                    logger.info("Found results container, but no property cards")
                    # Log the container content for debugging
                    logger.debug(f"Results container content: {results_container.prettify()[:1000]}...")
                else:
                    logger.warning("No results container found")
            
            # Extract listings with deduplication
            listings = []
            seen_ids: Set[str] = set()
            
            for card in property_cards:
                try:
                    listing = self._parse_property_card(card)
                    if listing and listing.listing_id not in seen_ids:
                        listings.append(listing)
                        seen_ids.add(listing.listing_id)
                        logger.info(f"Successfully parsed property: {listing.listing_id}")
                except Exception as e:
                    logger.error(f"Failed to parse property card: {str(e)}")
                    continue
            
            if not listings:
                logger.warning("No properties found matching the criteria")
            else:
                logger.info(f"Successfully found {len(listings)} properties")
            
            return listings
            
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return []
    
    async def get_listing_details(self, listing_id: str) -> Optional[PropertyListing]:
        """
        Get detailed information about a specific listing.
        
        Args:
            listing_id: Rightmove listing ID
            
        Returns:
            PropertyListing object if found, None otherwise
        """
        try:
            url = f"{self.LISTING_URL}/{listing_id}#/?channel=RES_BUY"
            data = await self._make_request(url, expect_json=False)
            if not data:
                return None
            
            soup = BeautifulSoup(data, "lxml")
            return self._parse_listing_page(soup)
            
        except Exception as e:
            logger.error(f"Failed to get listing details: {str(e)}")
            return None
    
    def _build_search_params(self, criteria: Dict[str, Any]) -> str:
        """
        Build search parameters for Rightmove URL.
        
        Args:
            criteria: Search criteria dictionary
            
        Returns:
            URL-encoded search parameters
        """
        # Convert property types to Rightmove format
        property_types = criteria.get("property_type", "")
        if property_types == "houses":
            property_types = "detached,semi-detached,terraced"
        
        params = {
            "searchLocation": criteria.get("location", ""),
            "useLocationIdentifier": "true",
            "locationIdentifier": criteria.get("location", ""),
            "radius": "0.0",
            "minPrice": criteria.get("price_min", ""),
            "maxPrice": criteria.get("price_max", ""),
            "minBedrooms": criteria.get("bedrooms_min", ""),
            "propertyTypes": property_types,
            "_includeSSTC": "on"
        }
        
        # Filter out empty values and join parameters
        return "&".join(f"{k}={v}" for k, v in params.items() if v)
    
    def _parse_property_card(self, card) -> Optional[PropertyListing]:
        """
        Parse a property card element into a PropertyListing object.
        
        Args:
            card: BeautifulSoup element containing property card
            
        Returns:
            PropertyListing object if successful, None otherwise
        """
        try:
            # Extract listing ID from the property card
            listing_id = None
            
            # Try to get from the property card ID
            card_id = card.get("id", "")
            if card_id.startswith("property-"):
                listing_id = card_id.replace("property-", "")
            
            # If not found, try to get from the link
            if not listing_id:
                link = card.find("a", class_="propertyCard-link")
                if link and "href" in link.attrs:
                    href = link["href"]
                    # Extract the ID from the URL
                    if "/properties/" in href:
                        listing_id = href.split("/properties/")[-1].split("#")[0]
                    elif "/property-for-sale/property/" in href:
                        listing_id = href.split("/property-for-sale/property/")[-1].replace(".html", "")
            
            if not listing_id:
                logger.error("Could not find listing ID")
                return None
            
            # Extract title
            title_elem = card.find("h2", class_="propertyCard-title")
            title = title_elem.text.strip() if title_elem else ""
            
            # Extract price
            price_elem = card.find("div", class_="propertyCard-priceValue")
            price = self._normalize_price(price_elem.text) if price_elem else 0
            
            # Extract location
            address_elem = card.find("address", class_="propertyCard-address")
            address = address_elem.text.strip() if address_elem else ""
            city = address.split(",")[-1].strip() if "," in address else ""
            postcode = ""  # Will be filled in detail view
            
            # Extract features
            features_elem = card.find("div", class_="propertyCard-features")
            bedrooms = None
            if features_elem:
                # Try different ways to find bedrooms
                beds_elem = (
                    features_elem.find("h2", text=lambda t: "bed" in t.lower()) or
                    features_elem.find("span", text=lambda t: "bed" in t.lower())
                )
                if beds_elem:
                    bedrooms = self._normalize_bedrooms(beds_elem.text)
            
            # Create PropertyListing object with proper URL
            return PropertyListing(
                listing_id=listing_id,
                source="rightmove",
                url=f"{self.LISTING_URL}/{listing_id}#/?channel=RES_BUY",
                title=title,
                description="",  # Will be filled in detail view
                location=PropertyLocation(
                    address=address,
                    city=city,
                    postcode=postcode
                ),
                features=PropertyFeatures(
                    bedrooms=bedrooms
                ),
                price=PropertyPrice(
                    amount=Decimal(str(price))
                )
            )
            
        except Exception as e:
            logger.error(f"Failed to parse property card: {str(e)}")
            return None
    
    def _parse_listing_page(self, soup) -> Optional[PropertyListing]:
        """
        Parse a listing page into a PropertyListing object.
        
        Args:
            soup: BeautifulSoup object of the listing page
            
        Returns:
            PropertyListing object if successful, None otherwise
        """
        try:
            # Extract listing ID from URL
            listing_id = soup.find("meta", {"property": "og:url"})["content"].split("/properties/")[-1].split("#")[0]
            
            # Extract title and description
            title = soup.find("h1", class_="property-header-title").text.strip()
            description = soup.find("div", class_="property-description").text.strip()
            
            # Extract price
            price_elem = soup.find("div", class_="property-header-price")
            price = self._normalize_price(price_elem.text) if price_elem else 0
            
            # Extract location
            address_elem = soup.find("address", class_="property-header-address")
            address = address_elem.text.strip() if address_elem else ""
            city = address.split(",")[-1].strip() if "," in address else ""
            postcode = ""  # Extract from address if available
            
            # Extract features
            features = {}
            features_grid = soup.find("div", class_="property-features-grid")
            if features_grid:
                for feature in features_grid.find_all("div", class_="property-feature"):
                    label = feature.find("span", class_="property-feature-label").text.strip()
                    value = feature.find("span", class_="property-feature-value").text.strip()
                    features[label.lower()] = value
            
            # Create PropertyListing object with proper URL
            return PropertyListing(
                listing_id=listing_id,
                source="rightmove",
                url=f"{self.LISTING_URL}/{listing_id}#/?channel=RES_BUY",
                title=title,
                description=description,
                location=PropertyLocation(
                    address=address,
                    city=city,
                    postcode=postcode
                ),
                features=PropertyFeatures(
                    bedrooms=self._normalize_bedrooms(features.get("bedrooms", "")),
                    bathrooms=self._normalize_bedrooms(features.get("bathrooms", "")),
                    property_type=features.get("property type", ""),
                    tenure=features.get("tenure", "")
                ),
                price=PropertyPrice(
                    amount=Decimal(str(price))
                )
            )
            
        except Exception as e:
            logger.error(f"Failed to parse listing page: {str(e)}")
            return None 