export const CONVERSATION_STATES = {
    INITIAL: 'INITIAL',
    CONFIRM_FILTERS: 'CONFIRM_FILTERS',
    EDIT_LOCATION: 'EDIT_LOCATION',
    PROPERTY_TYPE: 'PROPERTY_TYPE',
    BEDROOMS: 'BEDROOMS',
    PUBLIC_TRANSPORT: 'PUBLIC_TRANSPORT',
    SCHOOLS: 'SCHOOLS',
    TIMELINE: 'TIMELINE',
    FINANCIAL_READINESS: 'FINANCIAL_READINESS',
    EMAIL_REQUEST: 'EMAIL_REQUEST',
    COMPLETED: 'COMPLETED'
  };

  export const PROPERTY_TYPES = {
    LAND: 'Land',
    RESIDENTIAL: {
      label: 'Residential',
      subtypes: ['Studio', 'Flat', 'Detached House', 'Villa', 'Luxury']
    },
    COMMERCIAL: {
      label: 'Commercial',
      subtypes: ['Offices', 'Retail', 'Professional Services', 'Industrial']
    },
    LEISURE: {
      label: 'Leisure',
      subtypes: ['Hotels', 'Golf Clubs', 'Sport Facilities']
    }
  };

  export const TIMELINE_OPTIONS = [
    'ASAP',
    '1-3 months',
    '3-6 months',
    'Not sure yet'
  ];
  
  export const initialState = {
    currentState: CONVERSATION_STATES.INITIAL,
    filters: {
      location: null,
      propertyType: null,
      propertySubtype: null,
      bedrooms: {
        min: null,
        max: null
      },
      price: null,
      existingFilters: false
    },
    preferences: {
      publicTransport: null,
      schools: null,
      timeline: null,
      hasPreApprovedLoan: null
    },
    userEmail: null
  };

  export const extractBedroomNumbers = (input) => {
    const text = input.toLowerCase();
    let min = null;
    let max = null;

    // Handle specific patterns
    if (text.includes('studio')) return { min: 0, max: 0 };
    
    // Extract numbers from text
    const numbers = text.match(/\d+/g);
    if (numbers) {
      if (text.includes('min') && text.includes('max')) {
        min = parseInt(numbers[0]);
        max = parseInt(numbers[1]);
      } else if (text.includes('-') || text.includes('to')) {
        min = parseInt(numbers[0]);
        max = parseInt(numbers[1]);
      } else {
        min = parseInt(numbers[0]);
        max = min;
      }
    }

    return { min, max };
  };