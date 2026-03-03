// API client for backend communication

import axios from 'axios';
import config from "./config";
import { RecipeSearchResponse } from '@/types/recipe';


// create axios instance with config
const apiClient = axios.create({
    baseURL: config.apiUrl,
    timeout: config.apiTimeout,
    headers: {
        'Content-Type': 'application/json',
    },
})

// add request interceptor for logging (dev only)
if (config.isDevelopment) {
    apiClient.interceptors.request.use(request => {
        console.log('API Request:', request.method?.toUpperCase(), request.url);
        return request;
    });
}

// add response interceptor for error handling
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (config.isDevelopment) {
            console.error('API Error:', error.response?.data || error.message);
        }
        return Promise.reject(error);
    }
);


/**
 * search for recipes based on ingredients
 * @param ingredients  - List of ingredient names
 * @returns Recipe search results
 */
export async function searchRecipes(ingredients: string[]): Promise<RecipeSearchResponse> {
    const response = await apiClient.post<RecipeSearchResponse>('/recipe/search', ingredients);
    return response.data;
}