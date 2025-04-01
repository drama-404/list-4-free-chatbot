"""
Property Data Schema

This module defines the unified data schema for property listings.
All scraped data will be normalized to this schema for consistency.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any
from decimal import Decimal

@dataclass
class PropertyLocation:
    """Represents a property's location details."""
    address: str
    city: str
    postcode: str
    region: Optional[str] = None
    country: str = "United Kingdom"
    latitude: Optional[float] = None
    longitude: Optional[float] = None

@dataclass
class PropertyFeatures:
    """Represents a property's features and amenities."""
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    reception_rooms: Optional[int] = None
    property_type: Optional[str] = None
    tenure: Optional[str] = None
    floor_area: Optional[float] = None
    year_built: Optional[int] = None
    features: List[str] = None
    energy_rating: Optional[str] = None
    council_tax_band: Optional[str] = None

@dataclass
class PropertyPrice:
    """Represents a property's price information."""
    amount: Decimal
    currency: str = "GBP"
    price_type: str = "asking_price"  # asking_price, guide_price, sold_price
    is_under_offer: bool = False
    is_sold: bool = False
    sold_date: Optional[datetime] = None
    sold_price: Optional[Decimal] = None

@dataclass
class PropertyListing:
    """Unified schema for property listings from any source."""
    # Basic Information
    listing_id: str
    source: str  # e.g., "rightmove", "zoopla"
    url: str
    title: str
    description: str
    
    # Location
    location: PropertyLocation
    
    # Features
    features: PropertyFeatures
    
    # Price
    price: PropertyPrice
    
    # Additional Information
    images: List[str] = None
    floor_plans: List[str] = None
    virtual_tour_url: Optional[str] = None
    available_from: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    
    # Raw Data (for debugging and future reference)
    raw_data: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert the listing to a dictionary format."""
        return {
            "listing_id": self.listing_id,
            "source": self.source,
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "location": {
                "address": self.location.address,
                "city": self.location.city,
                "postcode": self.location.postcode,
                "region": self.location.region,
                "country": self.location.country,
                "latitude": self.location.latitude,
                "longitude": self.location.longitude
            },
            "features": {
                "bedrooms": self.features.bedrooms,
                "bathrooms": self.features.bathrooms,
                "reception_rooms": self.features.reception_rooms,
                "property_type": self.features.property_type,
                "tenure": self.features.tenure,
                "floor_area": self.features.floor_area,
                "year_built": self.features.year_built,
                "features": self.features.features,
                "energy_rating": self.features.energy_rating,
                "council_tax_band": self.features.council_tax_band
            },
            "price": {
                "amount": str(self.price.amount),
                "currency": self.price.currency,
                "price_type": self.price.price_type,
                "is_under_offer": self.price.is_under_offer,
                "is_sold": self.price.is_sold,
                "sold_date": self.price.sold_date.isoformat() if self.price.sold_date else None,
                "sold_price": str(self.price.sold_price) if self.price.sold_price else None
            },
            "images": self.images,
            "floor_plans": self.floor_plans,
            "virtual_tour_url": self.virtual_tour_url,
            "available_from": self.available_from.isoformat() if self.available_from else None,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "raw_data": self.raw_data
        } 