import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'
import Page from './page'

describe('Page', () => {
  it('renders a heading', () => {
    render(<Page />)

    const heading = screen.getByRole('heading', { level: 1 })

    expect(heading).toBeInTheDocument()
  })

  it('renders the form elements', () => {
    render(<Page />)

    expect(screen.getByLabelText('テキスト')).toBeInTheDocument()
    expect(screen.getByLabelText('コードの種類')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'コードを作成' })).toBeInTheDocument()
  })
})
