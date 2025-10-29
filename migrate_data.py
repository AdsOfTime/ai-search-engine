import csv
import uuid
import os
from pathlib import Path

def migrate_csv_to_sql():
    # Find the CSV file
    csv_file = "backend/scraped_products_20251029_190757.csv"
    
    if not os.path.exists(csv_file):
        print("CSV file not found")
        return
    
    print(f"Processing: {csv_file}")
    
    sql_statements = []
    count = 0
    
    with open(csv_file, 'r', encoding='utf-8', errors='ignore') as file:
        try:
            # Try to detect delimiter
            sample = file.read(1024)
            file.seek(0)
            
            # Use csv.Sniffer to detect format
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            
            reader = csv.DictReader(file, delimiter=delimiter)
            
            for row in reader:
                if count >= 1000:  # Limit for initial deployment
                    break
                    
                product_id = str(uuid.uuid4())
                
                # Clean and format data
                name = (row.get('name') or row.get('Name') or '').replace("'", "''").strip()[:200]
                if not name:
                    continue
                    
                brand = (row.get('brand') or row.get('Brand') or '').replace("'", "''").strip()[:100]
                category = (row.get('category') or row.get('Category') or 'general').replace("'", "''").strip()[:100]
                
                # Handle price
                price_str = row.get('price') or row.get('Price') or '0'
                try:
                    # Remove currency symbols and convert
                    price_clean = ''.join(filter(lambda x: x.isdigit() or x == '.', str(price_str)))
                    price = float(price_clean) if price_clean else 0
                    price = min(price, 9999.99)  # Cap at reasonable price
                except:
                    price = 0
                
                # Handle rating
                rating_str = row.get('rating') or row.get('Rating') or '0'
                try:
                    rating = float(rating_str)
                    rating = min(max(rating, 0), 5)  # Ensure rating is between 0-5
                except:
                    rating = 0
                
                # Handle description
                description = (row.get('description') or row.get('Description') or '').replace("'", "''").strip()[:500]
                
                # Handle URL
                url = (row.get('url') or row.get('URL') or '').replace("'", "''").strip()[:500]
                
                # Create SQL statement
                sql = f"""INSERT INTO products (id, name, brand, category, price, rating, description, image_url, in_stock, created_at) 
VALUES ('{product_id}', '{name}', '{brand}', '{category}', {price}, {rating}, '{description}', '{url}', 1, datetime('now'));"""
                
                sql_statements.append(sql)
                count += 1
        
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return
    
    # Write SQL file
    with open('data_migration.sql', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_statements))
    
    print(f'✅ Data migration SQL generated: {count} products')
    print('File: data_migration.sql')

if __name__ == "__main__":
    migrate_csv_to_sql()