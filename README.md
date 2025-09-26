# Stock-Screener

A full-stack web application for managing and screening stock portfolios with real-time financial data integration.

## Features

- **Portfolio Management**: Add and remove stocks with real-time data fetching
- **Advanced Filtering**: Screen stocks by dividend yield, P/E ratios, and moving averages
- **Real-time Data**: Automatic synchronization with Yahoo Finance API
- **Responsive UI**: Clean, modern interface built with Semantic UI
- **Background Processing**: Non-blocking data updates for optimal performance

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework with automatic API documentation
- **SQLAlchemy** - Python ORM for database operations
- **yahooquery** - Yahoo Finance API integration 

### Frontend
- **Jinja2** - Server-side templating
- **jQuery** - JavaScript library for DOM manipulation and AJAX
- **Semantic UI** - CSS framework for responsive design

### Database
- **SQLite** 

## Key Functionality

### Stock Management
- Add multiple stocks via modal interface (bulk entry supported)
- Remove stocks with confirmation dialogs
- Real-time data fetching in background tasks

### Financial Screening
Filter stocks by:
- **Dividend Yield**: Minimum dividend percentage
- **Forward P/E Ratio**: Maximum price-to-earnings ratio
- **Moving Averages**: Stocks trading above 50-day or 200-day MA
- **Combined Filters**: Mix and match criteria for advanced screening

### Data Integration
- Automatic fetching of real-time stock data
- Updates: price, P/E ratios, moving averages, dividend yields
- Background processing prevents UI blocking
- Error handling for invalid symbols or API failures

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main dashboard with filtering |
| `POST` | `/stock` | Add new stock to portfolio |
| `DELETE` | `/stock/{id}` | Remove stock from portfolio |

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/stock-portfolio-manager.git
   cd stock-portfolio-manager
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**
   ```bash
   # Database will be created automatically on first run
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the application**
   - Web Interface: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

## Usage

### Adding Stocks
1. Click "Add Stock Symbol" button
2. Enter stock symbols (one per line): `AAPL`, `MSFT`, `GOOGL`
3. Click "Add Stock Symbols"
4. Data will be fetched automatically in the background

### Filtering Stocks
Use the filter form to screen stocks:
- **P/E Ratio**: Enter maximum ratio (e.g., `20`)
- **Dividend Yield**: Enter minimum percentage (e.g., `2.5`)
- **Moving Averages**: Check boxes for bullish signals
- Click "Filter" to apply criteria

### Removing Stocks
- Click the red "Remove" button next to any stock
- Confirm deletion in the popup dialog
- Stock will be removed with smooth animation

## Project Structure

```
SP500-Stock-Screener/
│
├── main.py              # FastAPI application and routes
├── models.py            # SQLAlchemy database models
├── database.py          # Database configuration
├── requirements.txt     # Python dependencies
│
├── templates/
│   ├── layout.html      # Base HTML template
│   └── home.html        # Main dashboard template
```

## Future Enhancements

- [ ] Multiple portfolios
- [ ] Stock performance charts
- [ ] Alerts for price movements
- [ ] Export portfolio data to CSV/Excel
- [ ] Additional Metrics (YoY Growth, technical indicators, ect...)
