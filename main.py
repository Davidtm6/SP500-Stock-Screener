"""
Stock Portfolio Management API

A FastAPI-based REST API for managing a stock portfolio with real-time data integration.

Features:
- Stock symbol CRUD operations
- Real-time stock data fetching from Yahoo Finance
- Advanced filtering by financial metrics
- Background data synchronization
- SQLAlchemy ORM with SQLite support

Dependencies:
- FastAPI: Web framework and API documentation
- SQLAlchemy: ORM and database abstraction
- yahooquery: Yahoo Finance API client
"""
import models 
from yahooquery import Ticker
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from models import Stock

# =====================================
# APPLICATION INITIALIZATION
# =====================================
app = FastAPI()
models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")
class StockRequest(BaseModel):
    symbol: str
    

def get_db():
    """
    Database session dependency for FastAPI route handlers
    
    Creates a new SQLAlchemy database session for each request.
    Ensures proper session cleanup using try/finally pattern.
    
    Yields:
        Session: SQLAlchemy database session
    Usage:
        @app.get("/endpoint")
        def my_route(db: Session = Depends(get_db)):
            # Use db session here
            
    Note:
        This is a generator function that FastAPI automatically manages.
        Session is automatically closed after request completion.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# =====================================
# WEB INTERFACE ROUTES
# =====================================
"""
Stock screener dashboard homepage with filtering capabilities
Renders the main web interface allowing users to view and filter stocks
based on various financial metrics. Supports multiple filter combinations.

Args:
    request (Request): FastAPI request object for template rendering
    dividend_yield (float): Minimum dividend yield filter (%)
    forward_pe (float): Maximum forward P/E ratio filter
    ma50 (float): Filter stocks above 50-day moving average
    ma200 (float): Filter stocks above 200-day moving average
    db (Session): Database session dependency
    
Returns:
    TemplateResponse: Rendered HTML template with filtered stock data
"""
@app.get("/")
def home(request: Request, dividend_yield = None, forward_pe = None, ma50 = None, ma200 = None,db = Depends(get_db)):

    stocks = db.query(Stock)

    if dividend_yield:
        stocks = stocks.filter(Stock.dividend_yield > dividend_yield)
    if forward_pe:
        stocks = stocks.filter(Stock.forward_pe < forward_pe)
    if ma50:
        stocks = stocks.filter(Stock.price > Stock.ma50)
    if ma200:
        stocks = stocks.filter(Stock.price > Stock.ma200)

    stocks=stocks.all()

    return templates.TemplateResponse("home.html", {"request": request, "stocks": stocks, 
                                      "dividend_yield": dividend_yield, "forward_pe": 
                                      forward_pe, "": ma50, "ma200": ma200})



# =====================================
# BACKGROUND DATA PROCESSING
# =====================================
"""
Background task to fetch real-time stock data from Yahoo Finance.
Retrieves current market data for a specific stock and updates the database.
Runs asynchronously to avoid blocking the API response.

Args:
    stock_id (int): Database ID of the stock to update
    
Data Retrieved:
    - Previous close price
    - Forward P/E ratio
    - 50-day moving average
    - 200-day moving average  
    - Dividend yield (converted to percentage)
"""
def fetch_stock_data(id: int):
    db = SessionLocal()

    stock = db.query(Stock).filter(Stock.id == id).first()
    symbol=stock.symbol

    data = Ticker(symbol)

    stock.price = data.summary_detail[symbol]['previousClose']
    stock.forward_pe = data.summary_detail[symbol]['forwardPE']
    stock.ma50 = data.summary_detail[symbol]['fiftyDayAverage']
    stock.ma200 = data.summary_detail[symbol]['twoHundredDayAverage']

    if data.summary_detail[symbol].get('dividendYield') is not None:
        stock.dividend_yield = data.summary_detail[symbol]['dividendYield'] * 100
    else:
        stock.dividend_yield = 0.00
    
    db.add(stock)
    db.commit()


# =====================================
# REST API ENDPOINTS
# =====================================
"""
Creates a new stock entry in the portfolio
Adds a new stock to the database with the provided symbol, then
queues a background task to fetch real-time data from Yahoo Finance.

Args:
    stock_request: Validated request containing stock symbol
    background_tasks: FastAPI background task manager
    db: Database session dependency
    
Process:
    1. Create new Stock record with symbol
    2. Save to database to get assigned ID
    3. Queue background task to fetch market data
    4. Return immediate success response
"""
@app.post("/stock")
async def create_stock(stock_request: StockRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    stock = Stock()
    stock.symbol = stock_request.symbol
    db.add(stock)
    db.commit()

    # Queue background task to fetch stock data
    background_tasks.add_task(fetch_stock_data, stock.id)

    return {"code": "success", "message": "Stock created"}



"""
Deletes the specified stock from the database.

Args:
    stock_id (int): Database ID of the stock to delete
    db: Database session dependency
    
Process:
    1. Find stock by ID
    2. Store symbol for response message
    3. Delete from database
    4. Return confirmation with symbol name
"""
@app.delete("/stock/{stock_id}")
def delete_stock(stock_id: int, db: Session = Depends(get_db)):
    # Find the stock using the ID
    stock = db.query(Stock).filter(Stock.id == stock_id).first()    
    if not stock:
        return {"code": "error", "message": "Stock not found"}
    
    symbol = stock.symbol  
    db.delete(stock)
    db.commit()
    return {"code": "success", "message": f"Stock {symbol} deleted successfully"}

