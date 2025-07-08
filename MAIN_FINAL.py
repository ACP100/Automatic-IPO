import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

accountss = [
    {
        "username": os.getenv("accounts1_USERNAME"),
        "password": os.getenv("accounts1_PASSWORD"),
        "dp": os.getenv("accounts1_DP"),  
        "crn": os.getenv("accounts1_CRN")
    }
]

def apply_for_ipo(accounts):
    options = Options()
    # Uncomment the line below if you want to run in headless mode after debugging
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized") 

    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://meroshare.cdsc.com.np/")

        # --- Interact with the Select2 DP dropdown ---
        # 1. Wait for and click the visible placeholder/selected value span
        # This targets the visible part of the Select2 dropdown.
        # It's typically a span with class 'select2-selection__rendered' or 'select2-selection__placeholder'.
        # We'll use a more general CSS selector for robustness.
        
        visible_dp_dropdown_span = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span.select2-selection__rendered"))
        )
        visible_dp_dropdown_span.click()
        time.sleep(1) # Short pause to allow the dropdown list and search box to appear

        # 2. Wait for the search input field to appear and type the DP name
        # Select2 creates an input field inside the dropdown for searching.
        # This input often has a class like 'select2-search__field' or it might be within a span.
        # Inspect the Meroshare page carefully for the exact selector of this search input.
        
        # Common Select2 search input selector:
        search_input_xpath = "//input[@class='select2-search__field']"
        
        dp_search_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, search_input_xpath))
        )
        dp_search_input.send_keys(accounts["dp"])
        time.sleep(2) # Give it time to filter the results

        # 3. Select the option from the dynamically loaded list after typing
        # The options are usually <li> elements inside a <ul> that appears below the search box.
        # The 'text()' part ensures we click the exact match.
        dp_option_xpath = f"//ul[contains(@id, 'select2') and contains(@id, 'results')]//li[text()='{accounts['dp']}']"
        
        # You might need to use a more robust locator if the text match isn't exact
        # For example, if it's 'contains(text(), ...)' and you want an exact match
        # or if the attribute is 'data-select2-id'.

        dp_option = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, dp_option_xpath))
        )
        dp_option.click()
        time.sleep(1) # Small pause after selection

        # --- Read the actual selected DP (Optional, but good for verification) ---
        selected_dp_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.select2-selection__rendered"))
        )
        actual_dp_selected = selected_dp_element.text
        print(f"[{accounts['username']}] Selected DP: {actual_dp_selected}")

        # --- Continue with the rest of the login process ---
        # Wait for username field to be clickable before sending keys
        username_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "username"))
        )
        username_input.send_keys(accounts["username"])

        # Wait for password field to be clickable
        password_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "password"))
        )
        password_input.send_keys(accounts["password"])

        # Wait for login button to be clickable
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))
        )
        login_button.click()
        time.sleep(5) # Still good to have a pause after login for navigation

        # Check for new IPO
        # driver.get("https://meroshare.cdsc.com.np/#/asba")
        # time.sleep(5)

        # ipo_rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
        # if not ipo_rows:
        #    print(f"[{accounts['username']}] No IPOs available.")
        #    return
    # Navigate to ASBA page
        driver.get("https://meroshare.cdsc.com.np/#/asba")
        time.sleep(5)

    # Find all IPO listing containers
        ipo_cards = driver.find_elements(By.CSS_SELECTOR, "div.company-list")

    # Flag to track if any valid IPO was found
        found_valid_ipo = False

        for card in ipo_cards:
            try:
                share_type = card.find_element(By.CSS_SELECTOR, "span.share-of-type").text.strip()
                share_group = card.find_element(By.CSS_SELECTOR, "span.isin").text.strip()

            # Check the conditions
                if share_type == "IPO" and share_group == "Ordinary Shares":
                    print(f"[{accounts['username']}] Found valid IPO: ShareType='{share_type}', ShareGroup='{share_group}'")

                # Click the Apply button inside this card
                    apply_button = card.find_element(By.XPATH, ".//button[contains(text(), 'Apply')]")
                    apply_button.click()
                    found_valid_ipo = True
                    applied_kitta_input = driver.find_element(By.ID, "appliedKitta")
                    applied_kitta_input.clear()
                    applied_kitta_input.send_keys("10")
            
                    crn_number_input = driver.find_element(By.ID, "crnNumber")
                    crn_number_input.send_keys(accounts["crn"])
                    time.sleep(1)

                    driver.find_element(By.ID, "disclaimer").click()
                    driver.find_element(By.XPATH, "//button[contains(text(), 'Apply')]").click()
                    time.sleep(2)

                    print(f"[{accounts['username']}] Applied for IPO successfully!")
                    time.sleep(3)
                    break  # Exit the loop after applying for the first valid IPO
            except Exception as e:
                print(f"[{accounts['username']}] Skipped one IPO card due to error: {e}")
                continue

        if not found_valid_ipo:
            print(f"[{accounts['username']}] No valid IPOs (Ordinary + IPO type) found.")
            return
            
    except Exception as e:
        print(f"[{accounts['username']}] Failed: {str(e)}")

    finally:
        if driver:
            driver.quit()

for acc in accountss:
    apply_for_ipo(acc)
