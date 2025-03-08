from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import yfinance as yf
from py_vollib.black_scholes_merton import black_scholes_merton
from py_vollib.black_scholes_merton.greeks import analytical as bsm_analytical
import datetime
import json
    
from data.tickers import sp500_tickers

app = FastAPI()

# Create a common menu bar HTML snippet
# Create a common menu bar HTML snippet
menu_bar_html = """
<nav class="menu-bar">
    <div class="menu-container">
        <a href="/" class="logo">BlackScholes.org</a>
        <ul class="menu-links">
            <li><a href="/">Home</a></li>
            <li><a href="/us_equities">US Equities</a></li>
        </ul>
    </div>
</nav>
<style>
    /* Menu Bar Styles */
    .menu-bar {
        background-color: #2563eb;
        padding: 10px 20px;
    }
    .menu-container {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .menu-links {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
    }
    .menu-links li {
        margin-left: 20px;
    }
    .menu-links a {
        color: white;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s;
    }
    .menu-links a:hover {
        color: #d1d5db;
    }
    .logo {
        color: white;
        font-size: 1.25rem;
        font-weight: bold;
        text-decoration: none;
    }
    @media (max-width: 768px) {
        .menu-container {
            flex-direction: column;
            align-items: flex-start;
        }
        .menu-links {
            flex-direction: column;
            width: 100%;
        }
        .menu-links li {
            margin: 10px 0;
        }
    }
</style>
"""


@app.get("/", response_class=HTMLResponse)
async def get_landing_page():
    html_content = f"""
    <html>
    <head>
        <title>Black-Scholes Option Pricer</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Inter', sans-serif;
                background-color: #f9fafb;
                color: #111827;
                text-align: center;
                margin: 0;
                padding: 0;
            }}
            .container {{
                padding: 100px 20px;
            }}
            h1 {{
                font-size: 3rem;
                margin-bottom: 10px;
            }}
            h2 {{
                font-size: 1.5rem;
                color: #555;
                margin-bottom: 30px;
            }}
            p {{
                font-size: 1rem;
                line-height: 1.5;
                max-width: 800px;
                margin: 0 auto 20px;
            }}
            a {{
                color: #2563eb;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .services {{
                display: flex;
                justify-content: space-between;
                gap: 20px;
                margin-top: 40px;
                flex-wrap: wrap;
            }}
            .service {{
                flex: 1 1 30%;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
                transition: transform 0.3s, box-shadow 0.3s;
            }}
            .service:hover {{
                transform: translateY(-5px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }}
            .service h3 {{
                font-size: 1.25rem;
                margin-bottom: 10px;
                color: #2563eb;
            }}
            .service p {{
                font-size: 1rem;
                margin-bottom: 20px;
                color: #4b5563;
            }}
            .service button {{
                padding: 10px 20px;
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                transition: background-color 0.3s;
            }}
            .service button:hover {{
                background-color: #1d4ed8;
            }}

        </style>
    </head>
    <body>
        {menu_bar_html}
        <div class="container">
            <h1>Black-Scholes Option Pricer</h1>
            <h2>BlackScholes.org</h2>
            <p>
                The Black-Scholes formula provides a theoretical estimate of the price of European-style options. It is derived from the Black–Scholes equation, a partial differential equation that prices options by continuously buying and selling the underlying asset to perfectly hedge the option contract, thereby eliminating option risk.
                To learn more about the Black-Scholes model, you can read the original paper:
            </p>
            <p>
                <a href="http://www.jstor.org/stable/1831029?origin=JSTOR-pdf" target="_blank">
                    The Pricing of Options and Corporate Liabilities
                </a>
            </p>
            <!-- Services Section -->
            <div class="services">
                <!-- Option Price Container -->
                <div class="service">
                    <h3>Option pricer</h3>
                    <p>Browse and price options on US stocks</p>
                    <button onclick="location.href='/us_equities'">US Equities</button>
                </div>


            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/us_equities", response_class=HTMLResponse)
async def get_us_equities():
    html_content = f"""
    <html>
    <head>
        <title>Options Data App</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{
                font-family: 'Inter', sans-serif;
                background-color: #f9fafb;
                color: #111827;
                font-size: 0.75rem;
                margin: 0;
                padding: 0;
            }}
            .container {{
                width: 75%;
                max-width: 1600px;
                margin: 0 auto;
                padding: 16px;
            }}
            /* Existing styles */
            .card {{
                background-color: #ffffff;
                border-radius: 0.5rem;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                padding: 16px;
                margin-bottom: 16px;
            }}
            .button {{
                background-color: #2563eb;
                color: white;
                padding: 0.25rem 0.5rem;
                font-size: 0.75rem;
                border-radius: 0.375rem;
                transition: background-color 0.3s;
            }}
            .button:hover {{
                background-color: #1d4ed8;
            }}
            .info-container {{
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .ticker-info {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }}
            .table-container {{
                overflow-x: auto;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 16px;
            }}
            th, td {{
                padding: 6px;
                text-align: left;
                border-bottom: 1px solid #e5e7eb;
                font-size: 0.75rem;
            }}
            .clickable-contract {{
                cursor: pointer;
                color: #2563eb;
                text-decoration: underline;
            }}
            .clickable-contract:hover {{
                color: #1d4ed8;
            }}
            input {{
                font-size: 0.75rem;
            }}
            .chart-container {{
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        {menu_bar_html}
        <div class="container">
            <!-- Ticker Selection Section -->
            <div class="card">
                <h2 class="text-lg font-bold mb-4">Select a Ticker</h2>
                <div class="info-container">
                    <form id="tickerForm" class="flex items-center space-x-8">
                        <input type="text" id="tickerInput" value="AAPL" class="p-1 border border-gray-300 rounded w-full md:w-1/2" placeholder="Enter a ticker (e.g., AAPL)">
                        <button type="submit" class="button">Submit</button>
                    </form>
                    <div id="tickerInfo" class="ticker-info">
                        <!-- Ticker info will be displayed here -->
                    </div>
                </div>
                <p id="errorMessage" class="error text-red-500 mt-2"></p>
            </div>

            <!-- Options Chains Section -->
            <div class="card">
                <h2 class="text-lg font-bold mb-4">Options Chains</h2>
                <label for="maturitySelect" class="block mb-2">Select Option Maturity Date:</label>
                <select id="maturitySelect" class="p-1 border border-gray-300 rounded mb-4 w-full md:w-1/2">
                    <!-- Option dates will be added here dynamically -->
                </select>
                <div class="table-container">
                    <div id="optionChain">
                        <!-- Option chain data will be inserted here dynamically -->
                    </div>
                </div>
            </div>
        </div>

        <script>
            window.onload = function() {{
                const ticker = 'AAPL';
                document.getElementById('tickerInput').value = ticker;
                const errorMessage = document.getElementById('errorMessage');
                errorMessage.textContent = '';

                loadTickerInfo(ticker);
            }};

            document.getElementById('tickerForm').onsubmit = async function(event) {{
                event.preventDefault();
                const ticker = document.getElementById('tickerInput').value.toUpperCase();
                const errorMessage = document.getElementById('errorMessage');
                errorMessage.textContent = '';

                const validTickers = {json.dumps(sp500_tickers)};
                if (!validTickers.includes(ticker)) {{
                    errorMessage.textContent = 'Select a valid ticker';
                    return;
                }}

                await loadTickerInfo(ticker);
            }};

            async function loadTickerInfo(ticker) {{
                try {{
                    const response = await fetch(`/get_ticker_info?ticker=${{ticker}}`);
                    const data = await response.text();
                    document.getElementById('tickerInfo').innerHTML = data;

                    await loadOptionDates(ticker);
                }} catch (error) {{
                    console.error('Error loading ticker info:', error);
                    document.getElementById('tickerInfo').innerHTML = '<p>Error loading ticker information.</p>';
                }}
            }}

            async function loadOptionDates(ticker) {{
                try {{
                    const response = await fetch(`/get_option_dates?ticker=${{ticker}}`);
                    const dates = await response.json();

                    const maturitySelect = document.getElementById('maturitySelect');
                    maturitySelect.innerHTML = '';
                    dates.forEach(date => {{
                        const option = document.createElement('option');
                        option.value = date;
                        option.text = date;
                        maturitySelect.appendChild(option);
                    }});

                    if (dates.length > 0) {{
                        await loadOptionChain(ticker, dates[0]);
                    }}

                    maturitySelect.onchange = function() {{
                        const selectedDate = maturitySelect.value;
                        loadOptionChain(ticker, selectedDate);
                    }};
                }} catch (error) {{
                    console.error('Error loading option dates:', error);
                    document.getElementById('optionChain').innerHTML = '<p>Error loading option dates.</p>';
                }}
            }}

            async function loadOptionChain(ticker, date) {{
                try {{
                    const response = await fetch(`/get_option_chain?ticker=${{ticker}}&date=${{date}}`);
                    const data = await response.text();
                    document.getElementById('optionChain').innerHTML = data;
                }} catch (error) {{
                    console.error('Error loading option chain:', error);
                    document.getElementById('optionChain').innerHTML = '<p>Error loading option chain.</p>';
                }}
            }}

            function openContractPage(contractSymbol) {{
                window.location.href = `/option_contract?contract=${{contractSymbol}}`;
            }}
        </script>
    <footer style="text-align: center; margin: 20px;">
        <a href="https://www.linkedin.com/in/adam-machkour/" target="_blank" 
           style="text-decoration: none; color: #2563eb; padding: 10px 10px; border: 1px solid #2563eb; border-radius: 3px; transition: background-color 0.3s, color 0.3s;">
            Created by Adam Machkour
        </a>
    </footer>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/get_ticker_info", response_class=HTMLResponse)
async def get_ticker_info(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        
        # Fetch the necessary data
        last_price = round(stock.history(period="1d")['Close'].iloc[0], 2)
        bid = round(stock.info.get('bid', 0), 2)
        ask = round(stock.info.get('ask', 0), 2)
        bid_size = round(stock.info.get('bidSize', 0))
        ask_size = round(stock.info.get('askSize', 0))
        volume = stock.info.get('volume', 'N/A')

        # Fetch additional information
        day_range = stock.info.get('dayLow', 'N/A'), stock.info.get('dayHigh', 'N/A')
        day_range_formatted = f"{round(day_range[0], 2)} - {round(day_range[1], 2)}" if 'N/A' not in day_range else 'N/A'
        
        week_52_range = stock.info.get('fiftyTwoWeekLow', 'N/A'), stock.info.get('fiftyTwoWeekHigh', 'N/A')
        week_52_range_formatted = f"{round(week_52_range[0], 2)} - {round(week_52_range[1], 2)}" if 'N/A' not in week_52_range else 'N/A'
        
        ex_dividend_date = stock.info.get('exDividendDate', 'N/A')
        
        # Format ex-dividend date if it exists and is an integer timestamp
        if isinstance(ex_dividend_date, int):
            ex_dividend_date = datetime.datetime.fromtimestamp(ex_dividend_date).strftime('%b %d, %Y')
        elif isinstance(ex_dividend_date, datetime.date):
            ex_dividend_date = ex_dividend_date.strftime('%b %d, %Y')
        else:
            ex_dividend_date = 'N/A'
        
        forward_dividend = stock.info.get('dividendRate', 'N/A')
        forward_yield = round(stock.info.get('dividendYield', 0), 2) if stock.info.get('dividendYield') else 'N/A'

        # Create HTML for ticker information
        html_content = f"""
        <div>
            <table style="width: 100%; border-collapse: collapse; margin-top: 16px;">
                <tr>
                    <th style="padding: 10px; text-align: center;">Last Price</th>
                    <th style="padding: 10px; text-align: center;">Bid</th>
                    <th style="padding: 10px; text-align: center;">Ask</th>
                    <th style="padding: 10px; text-align: center;">Volume</th>
                    <th style="padding: 10px; text-align: center;">Day's Range</th>
                    <th style="padding: 10px; text-align: center;">52-Week Range</th>
                    <th style="padding: 10px; text-align: center;">Ex-Dividend Date</th>
                    <th style="padding: 10px; text-align: center;">Forward Dividend & Yield</th>
                </tr>
                <tr>
                    <td style="padding: 10px; text-align: center;">{last_price}</td>
                    <td style="padding: 10px; text-align: center;">{bid} x {bid_size}</td>
                    <td style="padding: 10px; text-align: center;">{ask} x {ask_size}</td>
                    <td style="padding: 10px; text-align: center;">{volume}</td>
                    <td style="padding: 10px; text-align: center;">{day_range_formatted}</td>
                    <td style="padding: 10px; text-align: center;">{week_52_range_formatted}</td>
                    <td style="padding: 10px; text-align: center;">{ex_dividend_date}</td>
                    <td style="padding: 10px; text-align: center;">{forward_dividend} ({forward_yield}%)</td>
                </tr>
            </table>
        </div>
        """

        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"An error occurred: {e}", status_code=500)

        
@app.get("/get_option_dates", response_class=JSONResponse)
async def get_option_dates(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        dates = stock.options
        return JSONResponse(content=dates)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/get_option_chain", response_class=HTMLResponse)
async def get_option_chain(ticker: str, date: str):
    try:
        stock = yf.Ticker(ticker)
        options_chain = stock.option_chain(date)
        calls = options_chain.calls
        puts = options_chain.puts

        merged_df = calls.merge(puts, on='strike', how='outer', suffixes=('_call', '_put')).fillna('-')

        options_html = "".join([
            f"<tr>"
            f"<td class='clickable-contract' onclick='openContractPage(\"{row['contractSymbol_call']}\")'>{row['contractSymbol_call'] if row['contractSymbol_call'] != '-' else '-'}</td>"
            f"<td>{round(row['lastPrice_call'], 2) if row['lastPrice_call'] != '-' else '-'}</td>"
            f"<td>{round(row['bid_call'], 2) if row['bid_call'] != '-' else '-'}</td>"
            f"<td>{round(row['ask_call'], 2) if row['ask_call'] != '-' else '-'}</td>"
            f"<td>{round(row['change_call'], 2) if row['change_call'] != '-' else '-'}</td>"
            f"<td>{row['volume_call'] if row['volume_call'] != '-' else '-'}</td>"
            f"<td>{row['openInterest_call'] if row['openInterest_call'] != '-' else '-'}</td>"
            f"<td>{round(row['impliedVolatility_call'] * 100, 2) if row['impliedVolatility_call'] != '-' else '-'}%</td>"
            f"<td>{row['strike']}</td>"
            f"<td class='clickable-contract' onclick='openContractPage(\"{row['contractSymbol_put']}\")'>{row['contractSymbol_put'] if row['contractSymbol_put'] != '-' else '-'}</td>"
            f"<td>{round(row['lastPrice_put'], 2) if row['lastPrice_put'] != '-' else '-'}</td>"
            f"<td>{round(row['bid_put'], 2) if row['bid_put'] != '-' else '-'}</td>"
            f"<td>{round(row['ask_put'], 2) if row['ask_put'] != '-' else '-'}</td>"
            f"<td>{round(row['change_put'], 2) if row['change_put'] != '-' else '-'}</td>"
            f"<td>{row['volume_put'] if row['volume_put'] != '-' else '-'}</td>"
            f"<td>{row['openInterest_put'] if row['openInterest_put'] != '-' else '-'}</td>"
            f"<td>{round(row['impliedVolatility_put'] * 100, 2) if row['impliedVolatility_put'] != '-' else '-'}%</td>"
            f"</tr>"
            for _, row in merged_df.iterrows()
        ])

        tab_content_html = f"""
        <table border="1">
            <tr>
                <th>Contract Name</th><th>Last Price</th><th>Bid</th><th>Ask</th><th>Change</th><th>Volume</th><th>Open Interest</th><th>IV</th>
                <th>Strike</th>
                <th>Contract Name</th><th>Last Price</th><th>Bid</th><th>Ask</th><th>Change</th><th>Volume</th><th>Open Interest</th><th>IV</th>
            </tr>
            {options_html}
        </table>
        """
        return HTMLResponse(content=tab_content_html)

    except Exception as e:
        return HTMLResponse(content=f"An error occurred: {e}", status_code=500)


def get_us_yield(days_to_expiration):
    try:
        treasury_symbols = {
            90: '^IRX',   # 13-week (3-month)
            180: '^IRX',  # Approximation for 6-month
            365: '^IRX',  # 1-year (using 1-year for simplicity)
            730: '^FVX',  # 2-year (using 5-year for simplicity)
            1825: '^TNX'  # 5-year (using 10-year for simplicity)
        }

        closest_days = min(treasury_symbols.keys(), key=lambda x: abs(x - days_to_expiration))
        symbol = treasury_symbols[closest_days]

        yield_data = yf.Ticker(symbol).history(period='1d')
        yield_rate = yield_data['Close'].iloc[0] / 100
        return yield_rate
    except Exception as e:
        print(f"Error fetching US yield: {e}")
        return 0.01


@app.get("/option_contract", response_class=HTMLResponse)
async def option_contract(contract: str):
    try:
        ticker = next((t for t in sp500_tickers if contract.startswith(t)), None)
        
        if ticker is None:
            return HTMLResponse(content="Unable to determine the ticker symbol from the contract.", status_code=400)

        option_type = 'c' if 'C' in contract else 'p'
        optionType = 'call' if option_type == 'c' else 'put'  # Compute optionType for JavaScript
        
        option = yf.Ticker(ticker)
        expiration_dates = option.options
        contract_details = None

        for exp_date in expiration_dates:
            options_chain = option.option_chain(exp_date)
            calls = options_chain.calls
            puts = options_chain.puts

            if contract in calls['contractSymbol'].values:
                contract_details = calls[calls['contractSymbol'] == contract].iloc[0]
                expiration_date = exp_date
                break
            elif contract in puts['contractSymbol'].values:
                contract_details = puts[puts['contractSymbol'] == contract].iloc[0]
                expiration_date = exp_date
                break

        if contract_details is None:
            return HTMLResponse(content="Option contract not found.", status_code=404)

        last_price = contract_details['lastPrice']
        bid = contract_details['bid']
        ask = contract_details['ask']
        change = contract_details['change']
        volume = contract_details['volume']
        strike_price = contract_details['strike']
        implied_vol = contract_details['impliedVolatility']
        underlying_price = option.history(period='1d')['Close'].iloc[0]

        # Get the annualized dividend yield as the default dividend rate
        dividend_yield = option.info.get('dividendYield', 0)

        days_to_expiration = (datetime.datetime.strptime(expiration_date, '%Y-%m-%d') - datetime.datetime.now()).days
        risk_free_rate = get_us_yield(days_to_expiration)

        time_to_expiration = days_to_expiration / 365

        try:
            bs_price = round(black_scholes_merton(
                option_type, underlying_price, strike_price, time_to_expiration,
                risk_free_rate, implied_vol, dividend_yield
            ), 2)
            delta = round(bsm_analytical.delta(
                option_type, underlying_price, strike_price, time_to_expiration,
                risk_free_rate, implied_vol, dividend_yield
            ), 6)
            gamma = round(bsm_analytical.gamma(
                option_type, underlying_price, strike_price, time_to_expiration,
                risk_free_rate, implied_vol, dividend_yield
            ), 6)
            theta = round(bsm_analytical.theta(
                option_type, underlying_price, strike_price, time_to_expiration,
                risk_free_rate, implied_vol, dividend_yield
            ), 6)
            vega = round(bsm_analytical.vega(
                option_type, underlying_price, strike_price, time_to_expiration,
                risk_free_rate, implied_vol, dividend_yield
            ), 6)
            rho = round(bsm_analytical.rho(
                option_type, underlying_price, strike_price, time_to_expiration,
                risk_free_rate, implied_vol, dividend_yield
            ), 6)
        except Exception as e:
            bs_price = delta = gamma = theta = vega = rho = 'N/A'

        html_content = f"""
        <html>
        <head>
            <title>{contract} - Option Summary</title>
            <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <!-- Include jStat library for statistical functions -->
            <script src="https://cdnjs.cloudflare.com/ajax/libs/jstat/1.9.4/jstat.min.js"></script>
            <style>
                body {{
                    font-family: 'Inter', sans-serif;
                    background-color: #f9fafb;
                    color: #111827;
                    font-size: 0.875rem;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    width: 75%;
                    max-width: 1600px;
                    margin: 0 auto;
                    padding: 16px;
                }}
                .card {{
                    background-color: #ffffff;
                    border-radius: 0.5rem;
                    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                    padding: 16px;
                    margin-bottom: 16px;
                }}
                .button {{
                    background-color: #2563eb;
                    color: white;
                    padding: 0.75rem;
                    font-size: 1rem;
                    border-radius: 0.375rem;
                    transition: background-color 0.3s;
                    width: 100%;
                    text-align: center;
                }}
                .button:hover {{
                    background-color: #1d4ed8;
                }}
                .flex-container {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 20px;
                }}
                .flex-item {{
                    flex: 1 1 48%;
                }}
                .flex-center {{
                    display: flex;
                    justify-content: center;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 16px;
                }}
                th, td {{
                    padding: 8px;
                    text-align: left;
                    border-bottom: 1px solid #e5e7eb;
                }}
                input {{
                    font-size: 0.875rem;
                }}
                .chart-container {{
                    margin-top: 20px;
                }}
                @media (max-width: 768px) {{
                    .flex-item {{
                        flex: 1 1 100%;
                    }}
                }}
                {menu_bar_html}
            </style>
        </head>
        <body>
        {menu_bar_html}
        <div class="container">
            <div class="container">
                <!-- Top Row: Contract Summary (Left) and Option Data (Right) -->
                <div class="flex-container">
                    <!-- Contract Summary (with inputs) -->
                    <div class="card flex-item">
                        <h2 class="text-xl font-bold mb-4">Contract Summary: {contract}</h2>
                        <form id="calculate-form">
                            <table>
                                <tr><th>Underlying Security</th><td>{ticker}</td></tr>
                                <tr><th>Option Type</th><td>{'Call' if option_type == 'c' else 'Put'}</td></tr>
                                <tr>
                                    <th>Strike Price</th>
                                    <td>
                                        {strike_price}
                                        <input type="hidden" id="strike_price" value="{strike_price}">
                                    </td>
                                </tr>
                                <tr>
                                    <th>Maturity Date</th>
                                    <td>
                                        {expiration_date}
                                        <input type="hidden" id="expiration_date" value="{expiration_date}">
                                    </td>
                                </tr>
                                <!-- Input Fields -->
                                <tr>
                                    <th>Underlying Price</th>
                                    <td><input type="number" step="0.01" id="underlying_price" value="{underlying_price}" class="p-1 border border-gray-300 rounded w-full"></td>
                                </tr>
                                <tr>
                                    <th>Implied Volatility %</th>
                                    <td><input type="number" step="0.01" id="implied_vol" value="{implied_vol * 100}" class="p-1 border border-gray-300 rounded w-full"></td>
                                </tr>
                                <tr>
                                    <th>Risk-Free Rate %</th>
                                    <td><input type="number" step="0.01" id="risk_free_rate" value="{risk_free_rate * 100}" class="p-1 border border-gray-300 rounded w-full"></td>
                                </tr>
                                <tr>
                                    <th>Dividend Rate %</th>
                                    <td><input type="number" step="0.01" id="dividend_rate" value="{dividend_yield}" class="p-1 border border-gray-300 rounded w-full"></td>
                                </tr>
                            </table>
                            <div class="flex-center">
                                <button type="button" onclick="recalculate()" class="button mt-4">Recalculate Value and Greeks</button>
                            </div>
                        </form>
                    </div>
                    <!-- Option Data -->
                    <div class="card flex-item">
                        <h3 class="text-lg font-bold mb-4">Option Data</h3>
                        <table>
                            <tr><th>Last Price</th><td>{last_price}</td></tr>
                            <tr><th>Bid</th><td>{bid}</td></tr>
                            <tr><th>Ask</th><td>{ask}</td></tr>
                            <tr><th>Change</th><td>{change}</td></tr>
                            <tr><th>Volume</th><td>{volume}</td></tr>
                        </table>
                        <!-- Option Price History Chart -->
                        <div class="chart-container">
                            <h4 class="text-md font-bold mb-2">Option Price History</h4>
                            <canvas id="priceChart"></canvas>
                        </div>
                    </div>
                </div>

                <!-- Middle Row: Value and Greeks (Left) and Charts (Right) -->
                <div class="flex-container">
                    <!-- Value and Greeks (Greeks Table) -->
                    <div class="card flex-item">
                        <h3 class="text-lg font-bold mb-4">Value and Greeks</h3>
                        <div id="bs-greeks">
                            <table>
                                <tr><th>Black-Scholes Price</th><td>{bs_price}</td></tr>
                                <tr><th>Delta</th><td>{delta}</td></tr>
                                <tr><th>Gamma</th><td>{gamma}</td></tr>
                                <tr><th>Theta</th><td>{theta}</td></tr>
                                <tr><th>Vega</th><td>{vega}</td></tr>
                                <tr><th>Rho</th><td>{rho}</td></tr>
                            </table>
                        </div>
                    </div>
                    <!-- Charts (Delta and Gamma) -->
                    <div class="card flex-item">
                        <h3 class="text-lg font-bold mb-4">Charts</h3>
                        <!-- Greeks Chart -->
                        <div class="chart-container">
                            <h4 class="text-md font-bold mb-2">Delta and Gamma</h4>
                            <canvas id="greeksChart"></canvas>
                        </div>
                    </div>
                </div>
            <script>
                function recalculate() {{
                    const strikePrice = parseFloat(document.getElementById('strike_price').value);
                    const expirationDate = document.getElementById('expiration_date').value;
                    const underlyingPrice = parseFloat(document.getElementById('underlying_price').value);
                    const impliedVol = parseFloat(document.getElementById('implied_vol').value) / 100;
                    const riskFreeRate = parseFloat(document.getElementById('risk_free_rate').value) / 100;
                    const dividendRate = parseFloat(document.getElementById('dividend_rate').value) / 100;

                    fetch(`/recalculate?contract={contract}&strike_price=${{strikePrice}}&expiration_date=${{expirationDate}}&underlying_price=${{underlyingPrice}}&implied_vol=${{impliedVol}}&risk_free_rate=${{riskFreeRate}}&dividend_rate=${{dividendRate}}`)
                        .then(response => response.text())
                        .then(data => {{
                            document.getElementById('bs-greeks').innerHTML = data;
                            // Redraw the Greeks chart with updated parameters
                            drawGreeksChart();
                        }})
                        .catch(error => console.error('Error:', error));
                }}

                // Draw the option price history chart
                async function drawPriceChart(contractSymbol) {{
                    try {{
                        const response = await fetch(`/get_contract_price_history?contract=${{contractSymbol}}`);
                        const data = await response.json();

                        if (!data.prices || !data.dates || data.prices.length === 0) {{
                            console.error('No price history data available.');
                            document.getElementById('priceChart').parentElement.innerHTML = '<p>No price history data available.</p>';
                            return;
                        }}

                        const ctx = document.getElementById('priceChart').getContext('2d');
                        new Chart(ctx, {{
                            type: 'line',
                            data: {{
                                labels: data.dates,
                                datasets: [{{
                                    label: 'Option Price',
                                    data: data.prices,
                                    borderColor: 'rgba(75, 192, 192, 1)',
                                    borderWidth: 2,
                                    fill: false,
                                }}]
                            }},
                            options: {{
                                scales: {{
                                    x: {{
                                        title: {{
                                            display: true,
                                            text: 'Date'
                                        }}
                                    }},
                                    y: {{
                                        title: {{
                                            display: true,
                                            text: 'Price'
                                        }},
                                        beginAtZero: false
                                    }}
                                }}
                            }}
                        }});
                    }} catch (error) {{
                        console.error('Error fetching price history:', error);
                    }}
                }}

                // Function to draw the Greeks chart
                function drawGreeksChart() {{
                    const strikePrice = parseFloat(document.getElementById('strike_price').value);
                    const expirationDate = document.getElementById('expiration_date').value;
                    const impliedVol = parseFloat(document.getElementById('implied_vol').value) / 100;
                    const riskFreeRate = parseFloat(document.getElementById('risk_free_rate').value) / 100;
                    const dividendRate = parseFloat(document.getElementById('dividend_rate').value) / 100;
                    const optionType = "{optionType}";

                    const daysToExpiration = (new Date(expirationDate) - new Date()) / (1000 * 3600 * 24);
                    const timeToExpiration = daysToExpiration / 365;

                    // Check for valid time to expiration
                    if (timeToExpiration <= 0) {{
                        console.error('Time to expiration must be positive.');
                        document.getElementById('greeksChart').parentElement.innerHTML = '<p>Cannot display Greeks chart: Time to expiration must be positive.</p>';
                        return;
                    }}

                    const underlyingPrices = [];
                    const deltas = [];
                    const gammas = [];

                    // Define the range around the strike price
                    const priceStep = strikePrice * 0.01; // 1% steps
                    const priceRange = strikePrice * 0.2; // +/-20%
                    const minPrice = strikePrice - priceRange;
                    const maxPrice = strikePrice + priceRange;

                    for (let S = minPrice; S <= maxPrice; S += priceStep) {{
                        underlyingPrices.push(S.toFixed(2));
                        const d1 = (Math.log(S / strikePrice) + (riskFreeRate - dividendRate + 0.5 * Math.pow(impliedVol, 2)) * timeToExpiration) / (impliedVol * Math.sqrt(timeToExpiration));

                        // Delta calculation
                        let delta;
                        if (optionType === 'call') {{
                            delta = Math.exp(-dividendRate * timeToExpiration) * jStat.normal.cdf(d1, 0, 1);
                        }} else {{
                            delta = Math.exp(-dividendRate * timeToExpiration) * (jStat.normal.cdf(d1, 0, 1) - 1);
                        }}
                        deltas.push(delta);

                        // Gamma calculation
                        const gamma = (Math.exp(-dividendRate * timeToExpiration) * jStat.normal.pdf(d1, 0, 1)) / (S * impliedVol * Math.sqrt(timeToExpiration));
                        gammas.push(gamma);
                    }}

                    const ctx = document.getElementById('greeksChart').getContext('2d');
                    new Chart(ctx, {{
                        type: 'line',
                        data: {{
                            labels: underlyingPrices,
                            datasets: [
                                {{
                                    label: 'Delta',
                                    data: deltas,
                                    borderColor: 'rgba(54, 162, 235, 1)',
                                    fill: false,
                                    yAxisID: 'y',
                                }},
                                {{
                                    label: 'Gamma',
                                    data: gammas,
                                    borderColor: 'rgba(255, 99, 132, 1)',
                                    fill: false,
                                    yAxisID: 'y1',
                                }}
                            ]
                        }},
                        options: {{
                            scales: {{
                                x: {{
                                    title: {{
                                        display: true,
                                        text: 'Underlying Price'
                                    }}
                                }},
                                y: {{
                                    title: {{
                                        display: true,
                                        text: 'Delta'
                                    }},
                                    position: 'left',
                                }},
                                y1: {{
                                    title: {{
                                        display: true,
                                        text: 'Gamma'
                                    }},
                                    position: 'right',
                                    grid: {{
                                        drawOnChartArea: false,
                                    }},
                                }}
                            }}
                        }}
                    }});
                }}

                // Call drawPriceChart and drawGreeksChart when the page loads
                window.onload = function() {{
                    drawPriceChart('{contract}');
                    drawGreeksChart();
                }};
            </script>
        <footer style="text-align: center; margin: 20px;">
            <a href="https://www.linkedin.com/in/adam-machkour/" target="_blank" 
               style="text-decoration: none; color: #2563eb; padding: 10px 10px; border: 1px solid #2563eb; border-radius: 3px; transition: background-color 0.3s, color 0.3s;">
                Created by Adam Machkour
            </a>
        </footer>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)

    except Exception as e:
        return HTMLResponse(content=f"An error occurred: {e}", status_code=500)


@app.get("/get_contract_price_history", response_class=JSONResponse)
async def get_contract_price_history(contract: str):
    try:
        option = yf.Ticker(contract)
        hist = option.history(period="1mo")  # Fetch 1 month of historical data
        prices = hist['Close'].tolist()
        dates = hist.index.strftime('%Y-%m-%d').tolist()
        return JSONResponse(content={"prices": prices, "dates": dates})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/recalculate", response_class=HTMLResponse)
async def recalculate(
    contract: str,
    strike_price: float,
    expiration_date: str,
    underlying_price: float,
    implied_vol: float,
    risk_free_rate: float,
    dividend_rate: float
):
    try:
        option_type = 'c' if 'C' in contract else 'p'

        days_to_expiration = (datetime.datetime.strptime(expiration_date, '%Y-%m-%d') - datetime.datetime.now()).days
        time_to_expiration = days_to_expiration / 365

        try:
            bs_price = round(black_scholes_merton(
                option_type, underlying_price, strike_price, time_to_expiration,
                risk_free_rate, implied_vol, dividend_rate
            ), 2)
            delta = round(bsm_analytical.delta(
                option_type, underlying_price, strike_price, time_to_expiration,
                risk_free_rate, implied_vol, dividend_rate
            ), 6)
            gamma = round(bsm_analytical.gamma(
                option_type, underlying_price, strike_price, time_to_expiration,
                risk_free_rate, implied_vol, dividend_rate
            ), 6)
            theta = round(bsm_analytical.theta(
                option_type, underlying_price, strike_price, time_to_expiration,
                risk_free_rate, implied_vol, dividend_rate
            ), 6)
            vega = round(bsm_analytical.vega(
                option_type, underlying_price, strike_price, time_to_expiration,
                risk_free_rate, implied_vol, dividend_rate
            ), 6)
            rho = round(bsm_analytical.rho(
                option_type, underlying_price, strike_price, time_to_expiration,
                risk_free_rate, implied_vol, dividend_rate
            ), 6)
        except Exception as e:
            bs_price = delta = gamma = theta = vega = rho = 'N/A'

        result_html = f"""
        <table>
            <tr><th>Black-Scholes Price</th><td>{bs_price}</td></tr>
            <tr><th>Delta</th><td>{delta}</td></tr>
            <tr><th>Gamma</th><td>{gamma}</td></tr>
            <tr><th>Theta</th><td>{theta}</td></tr>
            <tr><th>Vega</th><td>{vega}</td></tr>
            <tr><th>Rho</th><td>{rho}</td></tr>
        </table>
        """
        return HTMLResponse(content=result_html)

    except Exception as e:
        return HTMLResponse(content=f"An error occurred: {e}", status_code=500)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
