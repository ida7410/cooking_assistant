const config = {
  // API URL - automatically uses correct URL based on environment
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  
  // Environment
  isDevelopment: process.env.NODE_ENV === 'development',
  isProduction: process.env.NODE_ENV === 'production',
  
  // App Settings
  appName: 'Cooking Assistant',
  appVersion: '0.1.0',
  
  // Search Settings
  maxIngredients: 20,
  minIngredients: 1,
  
  // UI Settings
  resultsPerPage: 5,
  
  // Timeouts
  apiTimeout: 10000, // 10 seconds
};

export default config;