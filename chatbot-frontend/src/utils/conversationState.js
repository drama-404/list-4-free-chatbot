/**
 * Conversation State Management Module
 * 
 * Manages the state and flow of the chat conversation.
 * Provides utilities for handling property types, preferences, and state transitions.
 */

/**
 * Enumeration of possible conversation states
 * @readonly
 * @enum {string}
 */
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

/**
 * Available property types and their subtypes
 * @readonly
 * @enum {Object}
 */
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

/**
 * Available timeline options for property purchase
 * @readonly
 * @type {string[]}
 */
export const TIMELINE_OPTIONS = [
  'ASAP',
  '1-3 months',
  '3-6 months',
  'Not sure yet'
];

/**
 * Initial state object for the conversation
 * @readonly
 * @type {Object}
 */
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
    price: {
      min: null,
      max: null
    },
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

/**
 * Creates initial state with search criteria from the main app
 * 
 * @param {Object} searchCriteria - Search criteria from the main app
 * @returns {Object} Initial state with search criteria
 */
export const createInitialStateWithFilters = (searchCriteria) => ({
  ...initialState,
  filters: {
    ...initialState.filters,
    ...searchCriteria,
    existingFilters: true
  }
});

/**
 * Formats price range into a human-readable string
 * 
 * @param {number} min - Minimum price
 * @param {number} max - Maximum price
 * @returns {string|null} Formatted price range or null if no valid range
 */
const formatPrice = (min, max) => {
  if (min && max) return `between £${min.toLocaleString()} and £${max.toLocaleString()}`;
  if (min) return `from £${min.toLocaleString()}`;
  if (max) return `up to £${max.toLocaleString()}`;
  return null;
};

/**
 * Formats bedroom range into a human-readable string
 * 
 * @param {number} min - Minimum number of bedrooms
 * @param {number} max - Maximum number of bedrooms
 * @returns {string|null} Formatted bedroom range or null if no valid range
 */
const formatBedrooms = (min, max) => {
  if (min === null && max === null) return null;
  if (min === max) return `${min}`;
  if (min && max) return `${min}-${max}`;
  if (min) return `${min}+`;
  if (max) return `up to ${max}`;
  return null;
};

/**
 * Checks if a property type is residential
 * 
 * @param {string} propertyType - Main property type
 * @param {string} propertySubtype - Property subtype
 * @returns {boolean} Whether the property is residential
 */
const isResidentialProperty = (propertyType, propertySubtype) => {
  if (propertyType === 'Residential') return true;
  if (propertySubtype && PROPERTY_TYPES.RESIDENTIAL.subtypes.includes(propertySubtype)) return true;
  return false;
};

/**
 * Generates a confirmation message based on search criteria
 * 
 * @param {Object} filters - Current search filters
 * @returns {string|null} Formatted confirmation message or null if no valid filters
 */
export const generateConfirmationMessage = (filters) => {
  if (!filters || Object.values(filters).every(v => v === null ||
    (typeof v === 'object' && Object.values(v).every(x => x === null)))) {
    return null;
  }

  let parts = ['looking for'];

  // Handle property type/subtype
  if (filters.propertySubtype === 'Studio') {
    parts.push('studio flats');
  } else {
    let propertyDesc = [];

    // Add bedrooms if it's a residential property
    if (isResidentialProperty(filters.propertyType, filters.propertySubtype) &&
      filters.propertySubtype !== 'Studio') {
      const bedroomText = formatBedrooms(filters.bedrooms?.min, filters.bedrooms?.max);
      if (bedroomText) {
        propertyDesc.push(`${bedroomText} bedroom`);
      }
    }

    // Add property type/subtype
    if (filters.propertySubtype) {
      propertyDesc.push(filters.propertySubtype.toLowerCase());
    } else if (filters.propertyType) {
      propertyDesc.push(`${filters.propertyType.toLowerCase()} properties`);
    } else {
      propertyDesc.push('properties');
    }

    parts.push(propertyDesc.join(' '));
  }

  // Add location
  if (filters.location) {
    parts.push(`in ${filters.location}`);
  }

  // Add price
  const priceText = formatPrice(filters.price?.min, filters.price?.max);
  if (priceText) {
    parts.push(priceText);
  }

  return `Just to confirm, you're ${parts.join(' ')}? Do you want to refine these details?`;
};

/**
 * Extracts bedroom numbers from user input
 * 
 * @param {string} input - User's input text
 * @returns {Object} Object containing min and max bedroom numbers
 */
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

/**
 * Formats final preferences for API submission
 * 
 * @param {Object} state - Current conversation state
 * @returns {Object} Cleaned preferences object without null values
 */
export const formatFinalPreferences = (state) => {
  // Create a clean preferences object without any undefined values
  const preferences = {
    location: state.filters.location || null,
    propertyType: state.filters.propertyType || null,
    propertySubtype: state.filters.propertySubtype || null,
    bedrooms: {
      min: state.filters.bedrooms?.min || null,
      max: state.filters.bedrooms?.max || null
    },
    price: {
      min: state.filters.price?.min || null,
      max: state.filters.price?.max || null
    },
    // Additional preferences
    publicTransport: state.preferences.publicTransport || null,
    schools: state.preferences.schools || null,
    timeline: state.preferences.timeline || null,
    hasPreApprovedLoan: state.preferences.hasPreApprovedLoan || null
  };

  // Remove any null values to keep the object clean
  Object.keys(preferences).forEach(key => {
    if (preferences[key] === null) {
      delete preferences[key];
    }
  });

  return preferences;
};

/**
 * Formats conversation messages for API submission
 * 
 * @param {Array} messages - Array of chat messages
 * @returns {Array} Formatted messages with timestamps and options
 */
export const formatConversationSummary = (messages) => {
  return messages
    .map(msg => ({
      sender: msg.sender,
      text: msg.text,
      timestamp: msg.timestamp || new Date().toISOString(),
      options: msg.options || null
    }))
    .filter(msg => msg.text); // Filter out any messages without text
};