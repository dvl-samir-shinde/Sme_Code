import json
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime

def data_scraper(url):
    """Synchronous scraping function"""

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    try:
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            print(f"Error: Status code {response.status_code} for {url}")
            return None


 
        soup = BeautifulSoup(response.text, "html.parser")
 

        all_data_new = soup.get_text().split("\n")

        
        result = [item.strip() for item in all_data_new if item.strip()]

        

        
        
        elapsed_time = time.time() - start_time
        print(f"URL: {url} - Scraped in {elapsed_time:.2f} seconds")

        
        return result

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def save_results(results, filename):
    """Save results to JSON file"""
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {filename}")

def data_reader():
    try:
        # Record start time and date
        total_start_time = time.time()
        start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nStarting scraping process at: {start_datetime}")
        
        # Load URLs from JSON file
        with open("action_movies.json", 'r') as file:
            urls = json.load(file)
            
        print(f"Total URLs to process: {len(urls)}")
        print("\nStarting synchronous scraping...")
        
        # Scrape URLs one by one
        results = []
        successful_scrapes = 0
        failed_scrapes = 0
        
        for i, url in enumerate(urls, 1):
            print(f"\nProcessing URL {i}/{len(urls)}")
            result = data_scraper(url) # url 
            if result:
                results.append(result)
                successful_scrapes += 1
            else:
                failed_scrapes += 1
        
        # Calculate total time and statistics
        total_time = time.time() - total_start_time
        end_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Print summary
        print("\n" + "="*50)
        print("SCRAPING PROCESS SUMMARY")
        print("="*50)
        print(f"Start time: {start_datetime}")
        print(f"End time: {end_datetime}")
        print(f"Total time elapsed: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
        print(f"Total URLs processed: {len(urls)}")
        print(f"Successful scrapes: {successful_scrapes}")
        print(f"Failed scrapes: {failed_scrapes}")
        print(f"Success rate: {(successful_scrapes/len(urls))*100:.2f}%")
        print(f"Average time per URL: {total_time/len(urls):.2f} seconds")
        print("="*50)
        
        # Save results
        save_results(results, "synchronous_scraping_results.json")
        
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    data_reader()