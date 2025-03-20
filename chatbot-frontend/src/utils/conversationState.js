export const CONVERSATION_STATES = {
    INITIAL: 'INITIAL',
    CONFIRM_SEARCH: 'CONFIRM_SEARCH',
    LOCATION_INPUT: 'LOCATION_INPUT',
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
      price: null
    },
    preferences: {
      publicTransport: null,
      schools: null,
      timeline: null,
      hasPreApprovedLoan: null
    },
    userEmail: null
  };