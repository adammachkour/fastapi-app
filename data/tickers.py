
sp500_tickers = [
    'MSTR',
    'SPY',
    'AAPL', 
    'MSFT', 
    'NVDA', 
    'GOOG', 
    'GOOGL', 
    'META', 
    'BRK.B', 
    'TSLA', 
    'AVGO', 
    'LLY', 
    'WMT', 
    'JPM', 
    'UNH', 
    'V', 
    'XOM', 
    'ORCL', 
    'MA', 
    'PG', 
    'HD', 
    'COST', 
    'JNJ', 
    'ABBV', 
    'KO', 
    'BAC', 
    'NFLX', 
    'MRK', 
    'CVX', 
    'AMD', 
    'CRM', 
    'TMUS', 
    'TMO', 
    'PEP', 
    'LIN', 
    'ADBE', 
    'ACN', 
    'MCD', 
    'CSCO', 
    'IBM', 
    'GE', 
    'DHR', 
    'ABT', 
    'AXP', 
    'TXN', 
    'WFC', 
    'CAT', 
    'QCOM', 
    'VZ', 
    'PM', 
    'NOW', 
    'DIS', 
    'NEE', 
    'INTU', 
    'AMGN', 
    'ISRG', 
    'AMAT', 
    'MS', 
    'GS', 
    'PFE', 
    'CMCSA', 
    'SPGI', 
    'RTX', 
    'UBER', 
    'T', 
    'LOW', 
    'UNP', 
    'PGR', 
    'BKNG', 
    'BLK', 
    'LMT', 
    'SYK', 
    'HON', 
    'NKE', 
    'TJX', 
    'ETN', 
    'BSX', 
    'COP', 
    'ELV', 
    'VRTX', 
    'ANET', 
    'MU', 
    'BX', 
    'C', 
    'SCHW', 
    'KKR', 
    'CB', 
    'PLD', 
    'ADI', 
    'UPS', 
    'MDT', 
    'DE', 
    'REGN', 
    'ADP', 
    'SBUX', 
    'MMC', 
    'PANW', 
    'AMT', 
    'LRCX', 
    'KLAC', 
    'GILD', 
    'HCA', 
    'BMY', 
    'FI', 
    'INTC', 
    'MDLZ', 
    'SO', 
    'CI', 
    'SHW', 
    'BA', 
    'ICE', 
    'DUK', 
    'ZTS', 
    'MO', 
    'TT', 
    'MCO', 
    'CL', 
    'EQIX', 
    'WM', 
    'GD', 
    'CTAS', 
    'PH', 
    'ABNB', 
    'CEG', 
    'PYPL', 
    'SNPS', 
    'TDG', 
    'CME', 
    'CMG', 
    'ITW', 
    'APH', 
    'WELL', 
    'CVS', 
    'NOC', 
    'AON', 
    'MMM', 
    'CDNS', 
    'MSI', 
    'FCX', 
    'PNC', 
    'CARR', 
    'ECL', 
    'TGT', 
    'MAR', 
    'USB', 
    'CRWD', 
    'BDX', 
    'EOG', 
    'GEV', 
    'CSX', 
    'APD', 
    'ORLY', 
    'FDX', 
    'MCK', 
    'RSG', 
    'EMR', 
    'PSA', 
    'NXPI', 
    'DHI', 
    'AFL', 
    'NEM', 
    'AJG', 
    'SLB', 
    'ROP', 
    'FTNT', 
    'ADSK', 
    'MET', 
    'HLT', 
    'TFC', 
    'COF', 
    'NSC', 
    'WMB', 
    'PSX', 
    'MPC', 
    'SPG', 
    'O', 
    'AEP', 
    'AZO', 
    'URI', 
    'TRV', 
    'BK', 
    'DLR', 
    'SRE', 
    'OKE', 
    'GM', 
    'JCI', 
    'PCAR', 
    'MNST', 
    'LEN', 
    'KDP', 
    'CCI', 
    'GWW', 
    'FANG', 
    'ROST', 
    'CPRT', 
    'ALL', 
    'KMI', 
    'KMB', 
    'D', 
    'PAYX', 
    'RCL', 
    'OXY', 
    'AIG', 
    'STZ', 
    'FICO', 
    'CHTR', 
    'AMP', 
    'TEL', 
    'FIS', 
    'MSCI', 
    'MPWR', 
    'CMI', 
    'LHX', 
    'KVUE', 
    'COR', 
    'PEG', 
    'PWR', 
    'VLO', 
    'MCHP', 
    'PRU', 
    'F', 
    'IQV', 
    'KHC', 
    'A', 
    'ACGL', 
    'PCG', 
    'ODFL', 
    'IDXX', 
    'GEHC', 
    'OTIS', 
    'NDAQ', 
    'GIS', 
    'HES', 
    'FAST', 
    'KR', 
    'CTVA', 
    'HWM', 
    'VST', 
    'EXC', 
    'EW', 
    'AME', 
    'IR', 
    'YUM', 
    'CNC', 
    'IT', 
    'HSY', 
    'DOW', 
    'HUM', 
    'GLW', 
    'EA', 
    'SYY', 
    'CTSH', 
    'LVS', 
    'VRSK', 
    'EXR', 
    'DD', 
    'CBRE', 
    'ED', 
    'XEL', 
    'BKR', 
    'EFX', 
    'EL', 
    'NUE', 
    'RMD', 
    'DFS', 
    'VICI', 
    'LULU', 
    'IRM', 
    'HIG', 
    'HPQ', 
    'EIX', 
    'GRMN', 
    'DAL', 
    'VMC', 
    'MLM', 
    'AVB', 
    'XYL', 
    'TRGP', 
    'WAB', 
    'ON', 
    'PPG', 
    'MTD', 
    'LYB', 
    'EBAY', 
    'TSCO', 
    'CSGP', 
    'ROK', 
    'CDW', 
    'WEC', 
    'NVR', 
    'AXON', 
    'WTW', 
    'PHM', 
    'MTB', 
    'BRO', 
    'FITB', 
    'ADM', 
    'ANSS', 
    'BIIB', 
    'AWK', 
    'EQR', 
    'ETR', 
    'K', 
    'FTV', 
    'KEYS', 
    'FSLR', 
    'VLTO', 
    'DXCM', 
    'IFF', 
    'TTWO', 
    'CAH', 
    'DOV', 
    'VTR', 
    'DTE', 
    'STT', 
    'HPE', 
    'SW', 
    'GPN', 
    'SBAC', 
    'CHD', 
    'FE', 
    'HAL', 
    'MRNA', 
    'RJF', 
    'LYV', 
    'NTAP', 
    'BR', 
    'TYL', 
    'SMCI', 
    'WY', 
    'DVN', 
    'TROW', 
    'DECK', 
    'PPL', 
    'ROL', 
    'ES', 
    'WDC', 
    'STE', 
    'CCL', 
    'AEE', 
    'HUBB', 
    'STX', 
    'BF.B', 
    'BLDR', 
    'WST', 
    'MKC', 
    'ZBH', 
    'GDDY', 
    'TER', 
    'BBY', 
    'PTC', 
    'COO', 
    'EQT', 
    'CPAY', 
    'LDOS', 
    'WRB', 
    'INVH', 
    'ATO', 
    'HBAN', 
    'TSN', 
    'WAT', 
    'CBOE', 
    'CINF', 
    'ARE', 
    'RF', 
    'CMS', 
    'WBD', 
    'BALL', 
    'TDY', 
    'CLX', 
    'OMC', 
    'MOH', 
    'PFG', 
    'BAX', 
    'APTV', 
    'GPC', 
    'SYF', 
    'DRI', 
    'STLD', 
    'EXPE', 
    'FOXA', 
    'J', 
    'PKG', 
    'DG', 
    'UAL', 
    'ULTA', 
    'ALGN', 
    'ZBRA', 
    'CNP', 
    'ESS', 
    'NRG', 
    'HOLX', 
    'LH', 
    'VRSN', 
    'FOX', 
    'CFG', 
    'MAA', 
    'MAS', 
    'EXPD', 
    'NTRS', 
    'AVY', 
    'LUV', 
    'JBHT', 
    'CTRA', 
    'FDS', 
    'HRL', 
    'L', 
    'DGX', 
    'IP', 
    'EG', 
    'GEN', 
    'SWK', 
    'TXT', 
    'AMCR', 
    'IEX', 
    'PODD', 
    'PNR', 
    'DOC', 
    'SWKS', 
    'DLTR', 
    'LNT', 
    'ENPH', 
    'CAG', 
    'RVTY', 
    'KIM', 
    'CF', 
    'NI', 
    'KEY', 
    'AKAM', 
    'NWS', 
    'UHS', 
    'CE', 
    'SNA', 
    'NWSA', 
    'TRMB', 
    'DPZ', 
    'NDSN', 
    'UDR', 
    'MRO', 
    'CPB', 
    'AES', 
    'POOL', 
    'EVRG', 
    'JBL', 
    'BG', 
    'VTRS', 
    'DVA', 
    'AOS', 
    'CPT', 
    'EMN', 
    'REG', 
    'SJM', 
    'JKHY', 
    'JNPR', 
    'FFIV', 
    'BXP', 
    'HST', 
    'CHRW', 
    'INCY', 
    'ALLE', 
    'TECH', 
    'RL', 
    'MGM', 
    'KMX', 
    'IPG', 
    'TAP', 
    'SOLV', 
    'TFX', 
    'EPAM', 
    'ALB', 
    'TPR', 
    'CTLT', 
    'BEN', 
    'WYNN', 
    'LKQ', 
    'AIZ', 
    'HII', 
    'CRL', 
    'HAS', 
    'PNW', 
    'MHK', 
    'QRVO', 
    'MTCH', 
    'MKTX', 
    'LW', 
    'FRT', 
    'DAY', 
    'PAYC', 
    'GL', 
    'GNRC', 
    'HSIC', 
    'BIO', 
    'NCLH', 
    'APA', 
    'CZR', 
    'MOS', 
    'BWA', 
    'FMC', 
    'IVZ', 
    'WBA', 
    'AAL', 
    'PARA', 
    'BBWI', 
    'ETSY',
]
