# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.keys import Keys
# import time
# import os
# from dotenv import load_dotenv
# from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# print("Loading environment variables...")
# load_dotenv()
# print("Environment variables loaded.")

# # SETUP
# # IMPORTANT: Use a raw string (r"...") for Windows paths to avoid issues with backslashes
# driver_path = r"C:\Users\asus\chromedriver\win64-137.0.7151.120\chromedriver-win64\chromedriver.exe"
# print(f"ChromeDriver path set to: {driver_path}")

# try:
#     service = Service(driver_path)
#     print("Selenium Service object created.")
#     driver = webdriver.Chrome(service=service)
#     print("Chrome WebDriver initialized.")
#     wait = WebDriverWait(driver, 30) # Increased wait time for robustness
#     print("WebDriverWait object created with 30-second timeout.")

#     # 1. OPEN MEROSHARE
#     print("Navigating to Meroshare website...")
#     driver.get("https://meroshare.cdsc.com.np")
#     print("Meroshare website opened successfully.")

#     # 2. LOGIN (Update with your own credentials)
#     accounts = [
#         {
#             "username": os.getenv("accounts1_USERNAME"),
#             "password": os.getenv("accounts1_PASSWORD"),
#             "dp": os.getenv("accounts1_DP"),  
#             "crn": os.getenv("accounts1_CRN")
#         }
#     ]
#     print('yaha pugyo')
#     # if not all([dp_id, username, password]):
#     #     raise ValueError("Error: Missing Meroshare credentials in .env file. Please ensure accounts1_DP, accounts1_USERNAME, and accounts1_PASSWORD are set.")
#     # print("Retrieved credentials from environment variables.")
    
#     visible_dp_dropdown_span = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, "span.select2-selection__rendered"))
#         )
#     print('yaha pugyo 1')
#     visible_dp_dropdown_span.click()
#     time.sleep(1) # Short pause to allow the dropdown list and search box to appear

#         # 2. Wait for the search input field to appear and type the DP name
#         # Select2 creates an input field inside the dropdown for searching.
#         # This input often has a class like 'select2-search__field' or it might be within a span.
#         # Inspect the Meroshare page carefully for the exact selector of this search input.
        
#         # Common Select2 search input selector:
#     search_input_xpath = "//input[@class='select2-search__field']"
#     print('yaha pugyo 2')    
#     dp_search_input = WebDriverWait(driver, 20).until(
#             EC.visibility_of_element_located((By.XPATH, search_input_xpath))
#         )
    
#     dp_search_input.send_keys(accounts[0]["dp"])
#     print('yaha pugyo 3')
#     time.sleep(2) # Give it time to filter the result   
#         # 3. Select the option from the dynamically loaded list after typing
#         # The options are usually <li> elements inside a <ul> that appears below the search box.
#         # The 'text()' part ensures we click the exact match.
#     dp_option_xpath = f"//ul[contains(@id, 'select2') and contains(@id, 'results')]//li[text()='{accounts[0]['dp']}']"
#     print('yaha pugyo 3')
#         # You might need to use a more robust locator if the text match isn't exact
#         # For example, if it's 'contains(text(), ...)' and you want an exact match
#         # or if the attribute is 'data-select2-id'.

#     dp_option = WebDriverWait(driver, 20).until(
#           EC.element_to_be_clickable((By.XPATH, dp_option_xpath))
#       )       
#     dp_option.click()       
#     time.sleep(1) # Small pause after selection
    
#         # --- Read the actual selected DP (Optional, but good for verification) ---       selected_dp_element = WebDriverWait(driver, 10).until(           EC.presence_of_element_located((By.CSS_SELECTOR, "span.select2-selection__rendered"))       )       actual_dp_selected = selected_dp_element.text        print(f"[{accounts['username']}] Selected DP: {actual_dp_selected}")

#         # --- Continue with the rest of the login process ---
#         # Wait for username field to be clickable before sending keys
#     username_input = WebDriverWait(driver, 10).until(
#           EC.element_to_be_clickable((By.ID, "username"))
#       )
#     username_input.send_keys(accounts[0]["username"])

#         # Wait for password field to be clickable
#     password_input = WebDriverWait(driver, 10).until(
#          EC.element_to_be_clickable((By.ID, "password"))
#      )
#     password_input.send_keys(accounts[0]["password"])

#         # Wait for login button to be clickable
#     login_button = WebDriverWait(driver, 10).until(
#          EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))
#      )
#     login_button.click()
#     time.sleep(5)
#     # print("Waiting for DP ID dropdown to be present...")
#     # dp_dropdown_element = wait.until(EC.presence_of_element_located((By.ID, "selectBranch")))
#     # print("DP ID dropdown found.")
#     # dp_dropdown_element.send_keys(dp_id)
#     # print(f"DP ID '{dp_id}' entered into dropdown.")

#     # print("Waiting for username field to be present...")
#     # username_field_element = wait.until(EC.presence_of_element_located((By.ID, "username")))
#     # print("Username field found.")
#     # username_field_element.send_keys(username)
#     # print(f"Username '{username}' entered.")

#     # print("Waiting for password field to be present...")
#     # password_field_element = wait.until(EC.presence_of_element_located((By.ID, "password")))
#     # print("Password field found.")
#     # password_field_element.send_keys(password)
#     # print("Password entered.")

#     # print("Waiting for Login button to be clickable...")
#     # login_button_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]")))
#     # print("Login button found and is clickable.")
#     # login_button_element.click()
#     # print("Login button clicked.")

#     # --- IMPORTANT: CAPTCHA / Post-Login Check ---
#     # This is the most critical point for Meroshare. If a CAPTCHA appears,
#     # the script will typically time out here as the 'My ASBA' link won't load.
#     print("Waiting for 'My ASBA' link to be clickable (checking for login success)...")
#     my_asba_link_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'My ASBA')]")))
#     print("'My ASBA' link found and is clickable. Login appears successful (or CAPTCHA bypassed manually).")
#     my_asba_link_element.click()
#     print("Navigated to 'My ASBA' section.")

#     # 4. CLICK 'Application Report'
#     print("Waiting for 'Application Report' link to be clickable...")
#     application_report_link_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Application Report')]")))
#     print("'Application Report' link found and is clickable.")
#     application_report_link_element.click()
#     print("Clicked 'Application Report'.")

#     # 5. CLICK FIRST 'Report' BUTTON
#     print("Waiting for 'Report' buttons to be present...")
#     report_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Report')]")))
#     print(f"Found {len(report_buttons)} 'Report' button(s).")
#     if report_buttons:
#         print("Clicking the first 'Report' button...")
#         report_buttons[0].click()
#         print("First 'Report' button clicked.")
#         # 6. WAIT FOR STATUS TO LOAD AND GET STATUS
#         print("Waiting for IPO Status element to be present in the report popup...")
#         status_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Status')]/following-sibling::div")))
#         status = status_element.text
#         print("IPO Status element found.")
#     else:
#         status = "No IPO applications found with a 'Report' button."
#         print(status)

#     # 7. PRINT RESULT
#     print("\n--- Final Result ---")
#     print(f"IPO Status: {status}")
#     print("--------------------")

# except ValueError as ve:
#     print(f"Script Configuration Error: {ve}")
# except TimeoutException:
#     print("\nError: A TimeoutException occurred.")
#     print("This usually means an element was not found within the specified time.")
#     print("Common causes for this with Meroshare are:")
#     print("  1. CAPTCHA on the login page (most likely blocking progression).")
#     print("  2. Incorrect login credentials (preventing navigation to the dashboard).")
#     print("  3. Meroshare website structure has changed, and an XPath/ID is now incorrect.")
#     print("  4. Slow internet connection or website server response.")
#     driver.save_screenshot("meroshare_timeout_error.png")
#     print("Screenshot saved as 'meroshare_timeout_error.png' for debugging.")
# except NoSuchElementException as nsee:
#     print(f"\nError: A NoSuchElementException occurred: {nsee}")
#     print("This means an element with the specified locator could not be found on the page.")
#     print("Possible causes:")
#     print("  1. The HTML structure of Meroshare has changed.")
#     print("  2. The element was not yet loaded when the script tried to find it (though WebDriverWait should help).")
#     driver.save_screenshot("meroshare_element_not_found_error.png")
#     print("Screenshot saved as 'meroshare_element_not_found_error.png' for debugging.")
# except WebDriverException as wde:
#     print(f"\nError: A WebDriver-related exception occurred: {wde}")
#     print("This can happen if:")
#     print("  1. Chromedriver is not at the specified path.")
#     print("  2. Chromedriver version does not match your Chrome browser version.")
#     print("  3. Chromedriver executable does not have proper permissions.")
#     print("Please check the initial setup steps and Chromedriver compatibility.")
# except Exception as e:
#     print(f"\nAn unexpected error occurred: {e}")
#     driver.save_screenshot("meroshare_unexpected_error.png")
#     print("Screenshot saved as 'meroshare_unexpected_error.png' for debugging.")

# finally:
#     # Optional: Close browser after a delay
#     print("Waiting 5 seconds before closing the browser...")
#     time.sleep(5)
#     if 'driver' in locals() and driver: # Check if driver object exists before quitting
#         driver.quit()
#         print("Browser closed.")
#     else:
#         print("Browser was not initialized or already closed.")





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

accounts = [
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
#  4. CLICK 'Application Report'
        print("Waiting for 'Application Report' link to be clickable...")
        application_report_link_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Application Report')]")))
        print("'Application Report' link found and is clickable.")
        application_report_link_element.click()
        print("Clicked 'Application Report'.")

    # 5. CLICK FIRST 'Report' BUTTON
        print("Waiting for 'Report' buttons to be present...")
        report_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Report')]")))
        print(f"Found {len(report_buttons)} 'Report' button(s).")
        if report_buttons:
            print("Clicking the first 'Report' button...")
            report_buttons[0].click()
            print("First 'Report' button clicked.")
        # 6. WAIT FOR STATUS TO LOAD AND GET STATUS
            print("Waiting for IPO Status element to be present in the report popup...")
            status_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Status')]/following-sibling::div")))
            status = status_element.text
            print("IPO Status element found.")
        else:
            status = "No IPO applications found with a 'Report' button."
            print(status)

    # 7. PRINT RESULT
        print("\n--- Final Result ---")
        print(f"IPO Status: {status}")
        print("--------------------")

   
            
    except Exception as e:
        print(f"[{accounts['username']}] Failed: {str(e)}")

    finally:
        if driver:
            driver.quit()

for acc in accounts:
    apply_for_ipo(acc)
