import os
from datetime import datetime

# --- PART 2: DATA PROCESSING ---

def calculate_total_revenue(transactions):
    return sum(t['Quantity'] * t['UnitPrice'] for t in transactions)

def region_wise_sales(transactions):
    stats = {}
    total_revenue = calculate_total_revenue(transactions)
    
    for t in transactions:
        reg = t['Region']
        sales = t['Quantity'] * t['UnitPrice']
        
        if reg not in stats:
            stats[reg] = {'total_sales': 0.0, 'transaction_count': 0}
        
        stats[reg]['total_sales'] += sales
        stats[reg]['transaction_count'] += 1

    # Calculate percentage
    for reg in stats:
        if total_revenue > 0:
            stats[reg]['percentage'] = round((stats[reg]['total_sales'] / total_revenue) * 100, 2)
        else:
            stats[reg]['percentage'] = 0.0

    return dict(sorted(stats.items(), key=lambda x: x[1]['total_sales'], reverse=True))

def top_selling_products(transactions, n=5):
    prod_stats = {}
    for t in transactions:
        name = t['ProductName']
        if name not in prod_stats:
            prod_stats[name] = {'qty': 0, 'revenue': 0.0}
        prod_stats[name]['qty'] += t['Quantity']
        prod_stats[name]['revenue'] += t['Quantity'] * t['UnitPrice']
    
    sorted_prods = sorted(prod_stats.items(), key=lambda x: x[1]['qty'], reverse=True)
    return [(k, v['qty'], v['revenue']) for k, v in sorted_prods[:n]]

def customer_analysis(transactions):
    cust_stats = {}
    for t in transactions:
        cid = t['CustomerID']
        amt = t['Quantity'] * t['UnitPrice']
        prod = t['ProductName']
        
        if cid not in cust_stats:
            cust_stats[cid] = {'total_spent': 0.0, 'purchase_count': 0, 'products': set()}
        
        cust_stats[cid]['total_spent'] += amt
        cust_stats[cid]['purchase_count'] += 1
        cust_stats[cid]['products'].add(prod)

    # Format output
    result = {}
    for cid, data in cust_stats.items():
        result[cid] = {
            'total_spent': data['total_spent'],
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(data['total_spent'] / data['purchase_count'], 2),
            'products_bought': list(data['products'])
        }
    
    return dict(sorted(result.items(), key=lambda x: x[1]['total_spent'], reverse=True))

def daily_sales_trend(transactions):
    daily = {}
    for t in transactions:
        date = t['Date']
        amt = t['Quantity'] * t['UnitPrice']
        cid = t['CustomerID']
        
        if date not in daily:
            daily[date] = {'revenue': 0.0, 'transaction_count': 0, 'customers': set()}
            
        daily[date]['revenue'] += amt
        daily[date]['transaction_count'] += 1
        daily[date]['customers'].add(cid)
        
    # Convert set to count and sort
    final_daily = {}
    for date in sorted(daily.keys()):
        final_daily[date] = {
            'revenue': daily[date]['revenue'],
            'transaction_count': daily[date]['transaction_count'],
            'unique_customers': len(daily[date]['customers'])
        }
    return final_daily

def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)
    if not daily:
        return (None, 0, 0)
    peak_day = max(daily.items(), key=lambda x: x[1]['revenue'])
    return (peak_day[0], peak_day[1]['revenue'], peak_day[1]['transaction_count'])

def low_performing_products(transactions, threshold=10):
    prod_stats = {}
    for t in transactions:
        name = t['ProductName']
        if name not in prod_stats:
            prod_stats[name] = {'qty': 0, 'revenue': 0.0}
        prod_stats[name]['qty'] += t['Quantity']
        prod_stats[name]['revenue'] += t['Quantity'] * t['UnitPrice']
        
    low_performers = []
    for name, data in prod_stats.items():
        if data['qty'] < threshold:
            low_performers.append((name, data['qty'], data['revenue']))
            
    return sorted(low_performers, key=lambda x: x[1])

# --- PART 4: REPORT GENERATION ---

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    try:
        # This line requires 'import os' which is now added at the top
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Calculate Metrics
        total_rev = calculate_total_revenue(transactions)
        total_tx = len(transactions)
        avg_order = total_rev / total_tx if total_tx > 0 else 0
        dates = sorted([t['Date'] for t in transactions])
        date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"
        
        regions = region_wise_sales(transactions)
        top_prods = top_selling_products(transactions)
        top_custs = list(customer_analysis(transactions).items())[:5]
        daily = daily_sales_trend(transactions)
        peak_day = find_peak_sales_day(transactions)
        low_prods = low_performing_products(transactions)
        
        # API Stats
        enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match'))
        enrich_success = (enriched_count / len(enriched_transactions) * 100) if enriched_transactions else 0
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("SALES ANALYTICS REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Records Processed: {total_tx}\n")
            f.write("="*50 + "\n\n")
            
            f.write("OVERALL SUMMARY\n")
            f.write(f"Total Revenue: {total_rev:,.2f}\n")
            f.write(f"Total Transactions: {total_tx}\n")
            f.write(f"Average Order Value: {avg_order:,.2f}\n")
            f.write(f"Date Range: {date_range}\n\n")
            
            f.write("REGION-WISE PERFORMANCE\n")
            f.write(f"{'Region':<15} {'Sales':<15} {'% of Total':<15} {'Transactions':<15}\n")
            f.write("-" * 60 + "\n")
            for reg, data in regions.items():
                f.write(f"{reg:<15} {data['total_sales']:<15,.2f} {data['percentage']:<15} {data['transaction_count']:<15}\n")
            f.write("\n")
            
            f.write("TOP 5 PRODUCTS\n")
            f.write(f"{'Rank':<5} {'Product Name':<30} {'Quantity':<10} {'Revenue':<15}\n")
            for i, (name, qty, rev) in enumerate(top_prods, 1):
                f.write(f"{i:<5} {name:<30} {qty:<10} {rev:<15,.2f}\n")
            f.write("\n")
            
            f.write("TOP 5 CUSTOMERS\n")
            f.write(f"{'Rank':<5} {'Customer ID':<15} {'Total Spent':<15} {'Orders':<10}\n")
            for i, (cid, data) in enumerate(top_custs, 1):
                f.write(f"{i:<5} {cid:<15} {data['total_spent']:<15,.2f} {data['purchase_count']:<10}\n")
            f.write("\n")
            
            f.write("DAILY SALES TREND\n")
            f.write(f"{'Date':<15} {'Revenue':<15} {'Tx Count':<10} {'Unique Cust':<10}\n")
            for date, data in daily.items():
                f.write(f"{date:<15} {data['revenue']:<15,.2f} {data['transaction_count']:<10} {data['unique_customers']:<10}\n")
            f.write("\n")
            
            f.write("PRODUCT PERFORMANCE ANALYSIS\n")
            f.write(f"Best Selling Day: {peak_day[0]} (Revenue: {peak_day[1]:,.2f})\n")
            f.write("Low Performing Products:\n")
            for p in low_prods:
                f.write(f"- {p[0]}: {p[1]} sold\n")
            f.write("\n")
            
            f.write("API ENRICHMENT SUMMARY\n")
            f.write(f"Total Enriched: {enriched_count}\n")
            f.write(f"Success Rate: {enrich_success:.2f}%\n")

        print(f"Report generated successfully at {output_file}")
    except Exception as e:
        print(f"Error generating report: {e}")