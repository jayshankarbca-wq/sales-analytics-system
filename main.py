#!/usr/bin/env python3
from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter, save_enriched_data
from utils.data_processor import generate_sales_report
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data

def main():
    print("Welcome to Sales Analytics System")
    print("-" * 30)

    # 1. Read Data
    print("Reading data file...")
    raw_lines = read_sales_data('data/sales_data.txt')
    if not raw_lines:
        print("Exiting due to file error.")
        return

    # 2. Parse and Clean
    print("\nProcessing transactions...")
    transactions = parse_transactions(raw_lines)

    # 3. User Filter Interaction
    print("\nAvailable Filters:")
    regions = set(t['Region'] for t in transactions)
    print(f"Regions: {', '.join(regions)}")
    
    apply_filter = input("\nDo you want to apply filters? (y/n): ").lower()
    
    filtered_transactions = transactions
    if apply_filter == 'y':
        region = input("Enter region (or press Enter to skip): ").strip()
        min_amt = input("Enter min amount (or press Enter to skip): ").strip()
        
        region = region if region else None
        min_amt = float(min_amt) if min_amt else None
        
        filtered_transactions, _, summary = validate_and_filter(transactions, region=region, min_amount=min_amt)
        print(f"\nFilter Summary: {summary}")
    
    # 4. API Enrichment
    print("\nFetching API data...")
    api_products = fetch_all_products()
    if api_products:
        mapping = create_product_mapping(api_products)
        enriched_data = enrich_sales_data(filtered_transactions, mapping)
        save_enriched_data(enriched_data)
    else:
        print("Skipping enrichment due to API failure.")
        enriched_data = filtered_transactions # Fallback

    # 5. Report Generation
    print("\nGenerating report...")
    generate_sales_report(filtered_transactions, enriched_data)
    
    print("\nProcess Completed Successfully!")

if __name__ == "__main__":
    main()