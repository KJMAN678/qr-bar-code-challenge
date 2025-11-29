import '@testing-library/jest-dom';
import React from 'react';

jest.mock('qrcode.react', () => ({
  QRCodeSVG: ({ value }: { value: string }) => React.createElement('div', { 'data-testid': 'qr-code' }, value),
}));

jest.mock('react-barcode', () => {
  return function Barcode({ value }: { value: string }) {
    return React.createElement('div', { 'data-testid': 'barcode' }, value);
  };
});
