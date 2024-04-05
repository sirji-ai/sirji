from playwright.sync_api import sync_playwright
import time
from urllib.parse import urlparse, parse_qs

def search_for(query):
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False)

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        )
        page = context.new_page()

        # Navigate to Google
        page.goto('https://www.google.com')

        # Perform the search
        page.fill('input[name=q]', query)
        page.press('input[name=q]', 'Enter')

        time.sleep(10)  # Ensure search results have loaded

        filtered_urls = []
        exclude_domains_list = ['maps.google.com', 'accounts.google.com']  # Assuming maps.google.com is the domain to block

        # Extract all URLs
        links = page.query_selector_all('a[href]')
        seen_domains = set()
        for link in links:
            url = link.get_attribute('href')
            if not url:
                continue

            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            
            if not (parsed_url.path == '/url' and 'url' in query_params):
                continue

            target_url = query_params['url'][0]
            target_url_parsed = urlparse(target_url)
            domain = target_url_parsed.netloc
            # Check if the domain exists and is not in the blocked domains list
            if domain and domain not in exclude_domains_list and domain not in seen_domains:
                seen_domains.add(domain)
                filtered_urls.append(target_url)

        browser.close()
        return filtered_urls[:10]
