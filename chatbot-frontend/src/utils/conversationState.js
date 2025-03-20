export const CONVERSATION_STATES = {
    INITIAL: 'INITIAL',
    CONFIRM_SEARCH: 'CONFIRM_SEARCH',
    EDIT_FILTERS: 'EDIT_FILTERS',
    PUBLIC_TRANSPORT: 'PUBLIC_TRANSPORT',
    SCHOOLS: 'SCHOOLS',
    TIMELINE: 'TIMELINE',
    FINANCIAL_READINESS: 'FINANCIAL_READINESS',
    EMAIL_REQUEST: 'EMAIL_REQUEST',
    COMPLETED: 'COMPLETED'
  };
  
  export const initialState = {
    currentState: CONVERSATION_STATES.INITIAL,
    filters: {
      location: null,
      propertyType: null,
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