import requests

def fetch_all_products():
    """Fetches all products from DummyJSON API."""
    try:
        response = requests.get('https://dummyjson.com/products?limit=100')
        response.raise_for_status()
        data = response.json()
        print("Successfully fetched products from API.")
        return data['products']
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return []

def create_product_mapping(api_products):
    """Creates a mapping of product IDs to product info."""
    mapping = {}
    for p in api_products:
        mapping[p['id']] = {
            'title': p['title'],
            'category': p['category'],
            'brand': p.get('brand', 'Unknown'),
            'rating': p.get('rating', 0.0)
        }
    return mapping

def enrich_sales_data(transactions, product_mapping):
    """Enriches transaction data with API product information."""
    enriched = []
    for t in transactions:
        t_copy = t.copy()
        
        # Extract numeric ID from P101 -> 101, P5 -> 5
        try:
            prod_id_str = t['ProductID']
            # Remove non-numeric characters to find ID (assuming format P123)
            numeric_part = ''.join(filter(str.isdigit, prod_id_str))
            
            # Note: The mapping logic relies on the assumption that P101 maps to ID 1 or 101.
            # DummyJSON IDs are 1, 2, 3...
            # We will use modulo 100 or direct mapping if IDs match. 
            # Given the assignment implies matching, let's assume P101 -> 1 (example logic)
            # OR simple direct integer conversion if the IDs align.
            # Let's try to map P101 -> 1, P102 -> 2 for demonstration
            # as DummyJSON has IDs 1-100.
            
            pid = int(numeric_part)
            # Adjusting mapping logic: Assignment says P101 -> 101. 
            # But DummyJSON only goes to 100 (or 194). 
            # If P101 doesn't exist, we just check existence.
            
            if pid in product_mapping:
                api_data = product_mapping[pid]
                t_copy['API_Category'] = api_data['category']
                t_copy['API_Brand'] = api_data['brand']
                t_copy['API_Rating'] = api_data['rating']
                t_copy['API_Match'] = True
            else:
                # Fallback logic: Try mapping P101 -> 1 (common in these assignments)
                # If P101 (101) not found, try 101 % 100 or similar? 
                # Strict instruction: "If ID exists... add fields".
                # We will stick to strict ID matching.
                t_copy['API_Category'] = None
                t_copy['API_Brand'] = None
                t_copy['API_Rating'] = None
                t_copy['API_Match'] = False
                
        except Exception:
            t_copy['API_Match'] = False
            
        enriched.append(t_copy)
    return enriched