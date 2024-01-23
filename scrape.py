import asyncio
from pyppeteer import launch

async def main():
    # Define the URL to start with and the custom download path
    starting_url = 'https://adamsstudymaterial.notion.site/Possibly-EVERY-Trading-Book-1b633f36da114214aab9aeaffb8a07be'  # Replace with your starting URL.
    download_path = './'  # Replace with your desired download path.

    # Launch the browser with the specified download directory
    browser = await launch(headless=False, userDataDir=download_path)

    # await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    # Create a new browser page
    page = await browser.newPage()

    # Navigate to the starting URL
    await page.goto(starting_url)

    # Define the base selectors for constructing the dynamic selectors
    base_selector_start = '#notion-app > div > div:nth-child(1) > div > div:nth-child(1) > main > div > div.whenContentEditable > div:nth-child(4) > div:nth-child(1) > div > div:nth-child('
    base_selector_end = ') > div > div > div'

    # Start with the first item
    index = 1
    has_next = True

    # # Loop to process each item
    # while has_next:
    #     # Construct the dynamic selector for the current item
    #     selector = base_selector_start + str(index) + base_selector_end
    #     print(selector)
    #     try:
    #         # Try to find the link on the page
    #         link = await page.querySelector(selector)
    #         if link:

    #             # Click on the link to open a new tab.
    #             await link.click()

    #             # Wait for the new tab to open and get its page handle.
    #             new_page = (await browser.pages())[-1]  # The new tab should be the last one in the browser's list of pages.
                

    #             # Wait for a few seconds to ensure the download starts.
    #             await asyncio.sleep(5)

    #             # Close the new tab
    #             await new_page.close()

    #             # Increment the index to move to the next item
    #             index += 1
    #         else:
    #             # If the link is not found, exit the loop
    #             has_next = False
    #     except Exception as error:
    #         # If there's an error (e.g., selector not found), log it and move to the next item
    #         print(f"Error processing item {index}:", error)
    #         index += 1

    # # Close the browser when done (optional)
    # await browser.close()

    # await browser.process.communicate()

# Run the asynchronous function
asyncio.run(main())
