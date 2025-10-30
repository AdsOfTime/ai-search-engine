// Test file to check imports
try {
  const api = require('./services/api.ts');
  console.log('API import successful:', api);
} catch (error) {
  console.error('API import failed:', error);
}