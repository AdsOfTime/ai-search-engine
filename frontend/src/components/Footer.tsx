import React from 'react';
import styled from 'styled-components';

const FooterContainer = styled.footer`
  background: ${props => props.theme?.colors?.backgroundLight || '#f8fafc'};
  border-top: 1px solid ${props => props.theme?.colors?.border || '#e2e8f0'};
  padding: ${props => props.theme?.spacing?.xl || '2rem'} 0;
  margin-top: auto;
`;

const FooterContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 ${props => props.theme?.spacing?.md || '1rem'};
  text-align: center;
`;

const FooterText = styled.p`
  color: ${props => props.theme?.colors?.textLight || '#64748b'};
  font-size: ${props => props.theme?.fontSizes?.sm || '0.875rem'};
`;

const Footer: React.FC = () => {
  return (
    <FooterContainer>
      <FooterContent>
        <FooterText>
          © 2025 AI Product Search Engine. Find the best products at competitive prices.
        </FooterText>
      </FooterContent>
    </FooterContainer>
  );
};

export default Footer;