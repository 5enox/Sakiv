from playwright.sync_api import sync_playwright


def get_data(url, parent_xpath):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000, wait_until='load')

        # Wait for the parent element to be loaded
        page.wait_for_selector(f"xpath={parent_xpath}")

        # Get the parent element's children
        sections = page.query_selector_all(f"xpath={parent_xpath}/*")
        data = {}

        for section in sections:
            # Extract the label and value from each section
            label_element = section.query_selector('div:nth-child(1)')
            value_element = section.query_selector('div:nth-child(2)')

            if label_element and value_element:
                label = label_element.inner_text().strip().split('\n')[0]
                value = value_element.inner_text().strip()
                data[label] = value

        browser.close()
        return data
