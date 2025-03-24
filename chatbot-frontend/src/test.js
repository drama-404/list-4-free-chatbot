import { initiateChat } from './utils/api';

// Function to test the chat initiation
export const testChatInitiation = async () => {
    try {
        const response = await initiateChat({
            location: "London",
            propertyType: "Residential",
            propertySubtype: "Detached",
            bedrooms: {
                min: 2,
                max: 4
            },
            price: {
                min: 200000,
                max: 500000
            }
        }, "user123");

        console.log('Chat initiated:', response);
        return response;
    } catch (error) {
        console.error('Error testing chat initiation:', error);
        throw error;
    }
}; 