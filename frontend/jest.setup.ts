import '@testing-library/jest-dom';

jest.mock('bwip-js', () => ({
  toCanvas: jest.fn(),
}));

jest.mock('react-barcode', () => {
  const React = require('react');
  return function Barcode({ value }: { value: string }) {
    return React.createElement('div', { 'data-testid': 'barcode' }, value);
  };
});
