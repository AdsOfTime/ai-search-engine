import React from 'react';

const SearchSuggestions: React.FC = () => {
  const suggestions = [
    'Moisturizer for dry skin',
    'Waterproof mascara',
    'Running shoes',
    'Vitamin C serum',
    'Pain relief cream'
  ];

  return (
    <div style={{ 
      display: 'flex', 
      gap: '0.5rem', 
      flexWrap: 'wrap', 
      justifyContent: 'center',
      marginTop: '1rem'
    }}>
      {suggestions.map((suggestion, index) => (
        <button
          key={index}
          style={{
            background: 'transparent',
            border: '1px solid #e2e8f0',
            borderRadius: '20px',
            padding: '0.5rem 1rem',
            fontSize: '0.875rem',
            cursor: 'pointer',
            transition: 'all 0.2s ease'
          }}
          onClick={() => {
            window.location.href = `/search?q=${encodeURIComponent(suggestion)}`;
          }}
        >
          {suggestion}
        </button>
      ))}
    </div>
  );
};

export default SearchSuggestions;