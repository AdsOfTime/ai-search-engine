import React, { useState } from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import { MagnifyingGlassIcon, Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';

const HeaderContainer = styled.header`
  background: ${props => props.theme.colors.white};
  border-bottom: 1px solid ${props => props.theme.colors.border};
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  height: 80px;
`;

const HeaderContent = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 ${props => props.theme.spacing.md};
  max-width: 1200px;
  margin: 0 auto;
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  font-size: ${props => props.theme.fontSizes.xl};
  font-weight: 700;
  color: ${props => props.theme.colors.primary};
  cursor: pointer;
`;

const SearchContainer = styled.div`
  flex: 1;
  max-width: 600px;
  margin: 0 ${props => props.theme.spacing.lg};
  position: relative;
`;

const SearchInput = styled.input`
  width: 100%;
  height: 48px;
  padding: 0 ${props => props.theme.spacing.md} 0 50px;
  border: 2px solid ${props => props.theme.colors.border};
  border-radius: ${props => props.theme.borderRadius.full};
  font-size: ${props => props.theme.fontSizes.base};
  transition: border-color 0.2s ease;

  &:focus {
    border-color: ${props => props.theme.colors.primary};
    outline: none;
  }
`;

const SearchIcon = styled(MagnifyingGlassIcon)`
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: ${props => props.theme.colors.textLight};
`;

const NavLinks = styled.nav`
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.lg};

  @media (max-width: ${props => props.theme.breakpoints.md}) {
    display: none;
  }
`;

const NavLink = styled.button`
  background: none;
  color: ${props => props.theme.colors.text};
  font-size: ${props => props.theme.fontSizes.base};
  padding: ${props => props.theme.spacing.sm} ${props => props.theme.spacing.md};
  border-radius: ${props => props.theme.borderRadius.md};
  transition: background-color 0.2s ease;

  &:hover {
    background-color: ${props => props.theme.colors.secondary};
  }
`;

const MobileMenuButton = styled.button`
  display: none;
  background: none;
  color: ${props => props.theme.colors.text};
  padding: ${props => props.theme.spacing.sm};

  @media (max-width: ${props => props.theme.breakpoints.md}) {
    display: block;
  }
`;

const CategoryTabs = styled.div`
  display: flex;
  gap: ${props => props.theme.spacing.md};
  margin-top: ${props => props.theme.spacing.sm};
`;

const CategoryTab = styled.button<{ active?: boolean }>`
  background: ${props => props.active ? props.theme.colors.primary : 'transparent'};
  color: ${props => props.active ? props.theme.colors.white : props.theme.colors.text};
  border: 1px solid ${props => props.active ? props.theme.colors.primary : props.theme.colors.border};
  padding: ${props => props.theme.spacing.sm} ${props => props.theme.spacing.md};
  border-radius: ${props => props.theme.borderRadius.full};
  font-size: ${props => props.theme.fontSizes.sm};
  transition: all 0.2s ease;

  &:hover {
    border-color: ${props => props.theme.colors.primary};
    color: ${props => props.active ? props.theme.colors.white : props.theme.colors.primary};
  }
`;

interface HeaderProps {}

const Header: React.FC<HeaderProps> = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  const categories = [
    { id: '', label: 'All Categories' },
    { id: 'cosmetics', label: 'Cosmetics' },
    { id: 'fashion', label: 'Fashion' },
    { id: 'healthcare', label: 'Healthcare' }
  ];

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      const params = new URLSearchParams({
        q: searchQuery.trim(),
        ...(selectedCategory && { category: selectedCategory })
      });
      navigate(`/search?${params.toString()}`);
    }
  };

  const handleLogoClick = () => {
    navigate('/');
  };

  return (
    <HeaderContainer>
      <HeaderContent>
        <Logo onClick={handleLogoClick}>
          AI Product Search
        </Logo>

        <SearchContainer>
          <form onSubmit={handleSearch}>
            <SearchIcon />
            <SearchInput
              type="text"
              placeholder="Search for cosmetics, fashion, or healthcare products..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </form>
          
          <CategoryTabs>
            {categories.map(category => (
              <CategoryTab
                key={category.id}
                active={selectedCategory === category.id}
                onClick={() => setSelectedCategory(category.id)}
              >
                {category.label}
              </CategoryTab>
            ))}
          </CategoryTabs>
        </SearchContainer>

        <NavLinks>
          <NavLink onClick={() => navigate('/trending')}>
            Trending
          </NavLink>
          <NavLink onClick={() => navigate('/deals')}>
            Best Deals
          </NavLink>
          <NavLink onClick={() => navigate('/about')}>
            About
          </NavLink>
        </NavLinks>

        <MobileMenuButton onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
          {mobileMenuOpen ? (
            <XMarkIcon style={{ width: 24, height: 24 }} />
          ) : (
            <Bars3Icon style={{ width: 24, height: 24 }} />
          )}
        </MobileMenuButton>
      </HeaderContent>
    </HeaderContainer>
  );
};

export default Header;