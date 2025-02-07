import json
from bs4 import BeautifulSoup
import threading
from concurrent.futures import ThreadPoolExecutor
import requests
from queue import Queue
import time
from datetime import datetime

# Shared list to store all movie data
all_movies_data = []


def scrape_url(url):
    """Thread-based scraping function"""
    start_time = time.time()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    try:
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

def scrape_url_thread(url, results_queue):
    """Thread worker function"""
    start_time = time.time()
    result = scrape_url(url)
    if result:
        
        results_queue.put(result)
        elapsed_time = time.time() - start_time
        print(f"Thread completed URL: {url} - Time taken: {elapsed_time:.2f} seconds")

def thread_based_scraping(urls):
    """Thread pool based scraping"""
    print("\nStarting thread-based scraping...")
    start_time = time.time()
    start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Start time: {start_datetime}")
    print(f"Total URLs to process: {len(urls)}")
    
    results_queue = Queue()
    max_workers = min(32, 5)
    print(f"Using {max_workers} worker threads")
    
    # Create thread pool
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit URLs to thread pool
        futures = [
            executor.submit(scrape_url_thread, url, results_queue)
            for url in urls
        ]
    
    # Collect results from queue
    results = []
    successful_scrapes = 0
    while not results_queue.empty():
        results.append(results_queue.get())
        successful_scrapes += 1
    
    failed_scrapes = len(urls) - successful_scrapes
    total_time = time.time() - start_time
    end_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("\n" + "="*50)
    print("THREAD-BASED SCRAPING SUMMARY")
    print("="*50)
    print(f"Start time: {start_datetime}")
    print(f"End time: {end_datetime}")
    print(f"Total time elapsed: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
    print(f"Total URLs processed: {len(urls)}")
    print(f"Successful scrapes: {successful_scrapes}")
    print(f"Failed scrapes: {failed_scrapes}")
    print(f"Success rate: {(successful_scrapes/len(urls))*100:.2f}%")
    print(f"Average time per URL: {total_time/len(urls):.2f} seconds")
    print(f"Number of threads used: {max_workers}")
    print("="*50)
    
    return results

def save_results(results, filename):
    """Save results to JSON file"""
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {filename}")

def main():
    try:
        print("\nIMDb Scraping Process Started")
        print("="*50)
        start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Load URLs from JSON file
        with open("action_movies.json", 'r') as file:
            urls = json.load(file)
            
        
        # Thread-based scraping
        thread_results = thread_based_scraping(urls)
        save_results(thread_results, "prallel_scraping_results.json")
        
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()