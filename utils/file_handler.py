import os

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.
    """
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return []

    encodings = ['utf-8', 'latin-1', 'cp1252']
    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as f:
                lines = f.readlines()
                # Skip header and empty lines
                return [line.strip() for line in lines[1:] if line.strip()]
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
    
    print("Error: Could not decode file with standard encodings.")
    return []

def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries.
    """
    valid_transactions = []
    invalid_count = 0
    total_parsed = len(raw_lines)

    for line in raw_lines:
        try:
            parts = line.split('|')
            if len(parts) != 8:
                invalid_count += 1
                continue

            trans_id, date, prod_id, prod_name, qty_str, price_str, cust_id, region = parts

            # 1. Clean Numeric Fields (Remove commas)
            qty_str = qty_str.replace(',', '').strip()
            price_str = price_str.replace(',', '').strip()

            # 2. Convert Types
            quantity = int(qty_str)
            unit_price = float(price_str)

            # 3. Clean Product Name (Remove commas)
            prod_name = prod_name.replace(',', '')

            # 4. Validation Rules (REMOVE if...)
            if (not trans_id.startswith('T') or
                quantity <= 0 or
                unit_price <= 0 or
                not cust_id or
                not region):
                invalid_count += 1
                continue

            # If valid, build dictionary
            transaction = {
                'TransactionID': trans_id,
                'Date': date,
                'ProductID': prod_id,
                'ProductName': prod_name,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'CustomerID': cust_id,
                'Region': region.strip()
            }
            valid_transactions.append(transaction)

        except (ValueError, IndexError):
            invalid_count += 1
            continue

    print(f"Total records parsed: {total_parsed}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_transactions)}")
    
    return valid_transactions

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Filters transactions based on user criteria.
    """
    filtered = []
    invalid_count = 0 
    
    # Summary dictionary
    summary = {
        'total_input': len(transactions),
        'invalid': 0, # Assuming input is already cleaned by parse_transactions
        'filtered_by_region': 0,
        'filtered_by_amount': 0,
        'final_count': 0
    }

    for t in transactions:
        # Filter by Region
        if region and t['Region'].lower() != region.lower():
            summary['filtered_by_region'] += 1
            continue
        
        # Filter by Amount (Quantity * UnitPrice)
        total_amount = t['Quantity'] * t['UnitPrice']
        if min_amount is not None and total_amount < min_amount:
            summary['filtered_by_amount'] += 1
            continue
        if max_amount is not None and total_amount > max_amount:
            summary['filtered_by_amount'] += 1
            continue

        filtered.append(t)

    summary['final_count'] = len(filtered)
    return filtered, 0, summary

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file.
    """
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            # Write Header
            header = "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
            f.write(header)
            
            for t in enriched_transactions:
                line = (f"{t['TransactionID']}|{t['Date']}|{t['ProductID']}|{t['ProductName']}|"
                        f"{t['Quantity']}|{t['UnitPrice']}|{t['CustomerID']}|{t['Region']}|"
                        f"{t.get('API_Category', 'None')}|{t.get('API_Brand', 'None')}|"
                        f"{t.get('API_Rating', 'None')}|{t.get('API_Match', False)}\n")
                f.write(line)
        print(f"Successfully saved enriched data to {filename}")
    except Exception as e:
        print(f"Error saving enriched data: {e}")