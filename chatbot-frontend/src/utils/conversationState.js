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
      existingFilters: true
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

    // Handle special cases
    if (text.includes('studio')) return { min: 0, max: 0 };
    if (text.includes('no min') || text.includes('any min')) min = null;
    if (text.includes('no max') || text.includes('any max')) max = null;
    
    // Extract numbers and keywords
    const minMatch = text.match(/min(?:imum)?\s*(\d+)/i);
    const maxMatch = text.match(/max(?:imum)?\s*(\d+)/i);
    const rangeMatch = text.match(/(\d+)\s*(?:-|to)\s*(\d+)/);
    const singleNumber = text.match(/^(\d+)$/);

    if (minMatch && !text.includes('no min')) {
      min = parseInt(minMatch[1]);
    }
    if (maxMatch && !text.includes('no max')) {
      max = parseInt(maxMatch[1]);
    }
    if (rangeMatch) {
      min = parseInt(rangeMatch[1]);
      max = parseInt(rangeMatch[2]);
    }
    if (singleNumber) {
      min = parseInt(singleNumber[1]);
      max = min;
    }

    return { min, max };
  };