# Property Scrapers Module

This module provides a modular and extensible framework for scraping property listings from various UK property websites. It's designed to be maintainable, efficient, and easy to extend with new property websites.

## Features

- Asynchronous scraping for better performance
- Rate limiting to prevent website blocking
- Error handling and logging
- Support for multiple property websites
- Unified data model for consistent results
- Easy to extend with new providers

## Architecture

```
scrapers/
├── core/
│   ├── schema.py      # Unified data models
│   ├── base.py        # Base scraper class
│   ├── controller.py  # Central scraper controller
│   └── __init__.py    # Core package exports
├── providers/
│   └── rightmove.py   # Rightmove.co.uk implementation
├── utils/             # Utility functions
├── test_scrapers.py   # Test script
└── __init__.py        # Package exports
```

### Core Components

1. **Schema (`schema.py`)**
   - Defines unified data models for property listings
   - Ensures consistent data structure across different sources
   - Key classes:
     - `PropertyListing`: Main listing model
     - `PropertyLocation`: Location details
     - `PropertyFeatures`: Property features and amenities
     - `PropertyPrice`: Price information

2. **Base Scraper (`base.py`)**
   - Abstract base class for all scrapers
   - Provides common functionality:
     - Rate limiting
     - Error handling
     - Request management
     - Data normalization
   - Defines required interface methods:
     - `search()`
     - `get_listing_details()`

3. **Controller (`controller.py`)**
   - Manages multiple scrapers
   - Coordinates concurrent searches
   - Handles scraper lifecycle
   - Provides unified search interface

### Provider Implementation

Currently implemented:
- **Rightmove Scraper (`rightmove.py`)**
  - Scrapes property listings from Rightmove.co.uk
  - Handles search and detail page parsing
  - Implements rate limiting and error handling
  - Supports location identifiers and property types

## Usage

### Basic Usage

```python
from scrapers import ScraperController, RightmoveScraper

# Initialize scrapers
scrapers = [RightmoveScraper()]
controller = ScraperController(scrapers)

# Initialize the controller
await controller.initialize()

# Search for properties
criteria = {
    "location": "London",
    "price_min": 300000,
    "price_max": 500000,
    "bedrooms_min": 2,
    "property_type": "houses"
}

listings = await controller.search(criteria, max_results=10)

# Clean up
await controller.cleanup()
```

### Search Criteria

The search criteria dictionary supports the following fields:

```python
{
    "location": str,          # Required: Location to search in
    "price_min": float,       # Optional: Minimum price
    "price_max": float,       # Optional: Maximum price
    "bedrooms_min": int,      # Optional: Minimum bedrooms
    "bedrooms_max": int,      # Optional: Maximum bedrooms
    "property_type": str,     # Optional: Type of property
    "max_results": int        # Optional: Maximum results to return
}
```

### Property Listing Structure

Each property listing follows this structure:

```python
{
    "listing_id": str,
    "source": str,
    "url": str,
    "title": str,
    "description": str,
    "location": {
        "address": str,
        "city": str,
        "postcode": str,
        "region": str,
        "country": str,
        "latitude": float,
        "longitude": float
    },
    "features": {
        "bedrooms": int,
        "bathrooms": int,
        "reception_rooms": int,
        "property_type": str,
        "tenure": str,
        "floor_area": float,
        "year_built": int,
        "features": List[str],
        "energy_rating": str,
        "council_tax_band": str
    },
    "price": {
        "amount": Decimal,
        "currency": str,
        "price_type": str,
        "is_under_offer": bool,
        "is_sold": bool,
        "sold_date": datetime,
        "sold_price": Decimal
    },
    "images": List[str],
    "floor_plans": List[str],
    "virtual_tour_url": str,
    "available_from": datetime,
    "last_updated": datetime
}
```

## Testing

To test the scrapers:

1. Navigate to the scrapers directory:
```bash
cd chatbot-backend/scrapers
```

2. Run the test script:
```bash
python test_scrapers.py
```

The test script will:
- Initialize the scrapers
- Perform a sample property search
- Display the first 5 results
- Show detailed information about each property

## Adding New Providers

To add a new property website scraper:

1. Create a new file in `providers/` directory:
```python
from scrapers.core.base import BaseScraper
from scrapers.core.schema import PropertyListing

class NewScraper(BaseScraper):
    def __init__(self, config=None):
        super().__init__(config)
        self.BASE_URL = "https://example.com"
        self.SEARCH_URL = f"{self.BASE_URL}/search"
        self.LISTING_URL = f"{self.BASE_URL}/property"
        
    async def search(self, criteria: Dict[str, Any]) -> List[PropertyListing]:
        # Implement search logic
        pass

    async def get_listing_details(self, listing_id: str) -> Optional[PropertyListing]:
        # Implement detail fetching logic
        pass
```

2. Implement required methods:
   - `search()`: Search for properties
   - `get_listing_details()`: Get detailed information
   - `initialize()`: Set up the scraper
   - `cleanup()`: Clean up resources

3. Add the scraper to `__init__.py` exports:
```python
from .providers.new_scraper import NewScraper

__all__ = [
    'ScraperController',
    'RightmoveScraper',
    'NewScraper',
    # ... other exports
]
```

4. Register with the controller:
```python
scrapers = [RightmoveScraper(), NewScraper()]
controller = ScraperController(scrapers)
```

## Error Handling

The module includes comprehensive error handling:
- Rate limiting to prevent website blocking
- Graceful handling of network errors
- Validation of search criteria
- Logging of errors and warnings
- Fallback values for missing data

## Rate Limiting

Each scraper implements rate limiting to prevent overwhelming the target websites:
- Minimum delay between requests
- Configurable delays per provider
- Automatic request queuing

## Future Improvements

1. **Additional Providers**
   - Zoopla.co.uk
   - OnTheMarket.com
   - findahood.com
   - primelocation.com
   - placebuzz.com
   - watersideproperties.com
   - propertysnake.org
   - mouseprice.com
   - home.co.uk
   - unmodlondon.co.uk
   - etc.

2. **Enhanced Features**
   - Proxy support
   - Caching layer
   - Advanced filtering
   - Image downloading
   - Price history tracking

3. **Performance Optimizations**
   - Parallel processing
   - Connection pooling
   - Result caching
   - Incremental updates