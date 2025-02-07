import json
import asyncio
from bs4 import BeautifulSoup
import aiohttp
import time
from datetime import datetime

# List to store all movie data
all_movies_data = []

# Asynchronous function to scrape data from a given URL
async def data_scraper(session, url_, start_time):
    # Add headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    try:
        # Fetch the page content with headers
        async with session.get(url_, headers=headers) as response:
            if response.status != 200:
                print(f"Error: Status code {response.status} for {url_}")
                return None
                
            html = await response.text()
            
            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
 

            all_data_new = soup.get_text().split("\n")


        
        
            
            # Clean up empty strings and whitespace
            all_data_new = [item.strip() for item in all_data_new if item.strip()]

            # Calculate elapsed time for this URL
            elapsed_time = time.time() - start_time
            print(f"URL: {url_} - Scraped in {elapsed_time:.2f} seconds")
         
            return all_data_new

    except Exception as e:
        print(f"Error scraping {url_}: {e}")
        return None

# Asynchronous function to read data and scrape URLs
async def data_reader():
    try:
        # Record start time and date
        total_start_time = time.time()
        start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nStarting scraping process at: {start_datetime}")
        
        # Load URLs from the JSON file
        with open("action_movies.json", 'r') as file:
            urls = json.load(file)
        
        print(f"Total URLs to process: {len(urls)}")
        print("\nStarting asynchronous scraping...")

        # Create timeout for requests
        timeout = aiohttp.ClientTimeout(total=30)
        
        # Create an aiohttp session with the timeout
        async with aiohttp.ClientSession(timeout=timeout) as session:
            # Create tasks with timing information
            

            tasks = [data_scraper(session, url, time.time()) for url in urls]
            
            # Run all tasks concurrently
            results = await asyncio.gather(*tasks) # 

        # Filter out None results and add to the list
        successful_scrapes = 0
        failed_scrapes = 0
        
        for result in results:
            if result:
                all_movies_data.append(result)
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

        # Save the results to a file
        with open("async_scraping_results.json", "w") as file:
            json.dump(all_movies_data, file, indent=2)

        print(f"\nResults saved to all_movies_data.json")

    except Exception as e:
        print(f"Error in data_reader: {e}")

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(data_reader())
























