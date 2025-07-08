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
from selenium.webdriver.support.ui import Select
print('ok')
load_dotenv()

accounts = [
    {
        "username": os.getenv("ACCOUNT1_USERNAME"),
        "password": os.getenv("ACCOUNT1_PASSWORD"),
        "dp": os.getenv("ACCOUNT1_DP"),
        "crn": os.getenv("ACCOUNT1_CRN"),
        "pin": os.getenv("ACCOUNT1_PIN")
    }
]

def apply_for_ipo(account):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")

    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://meroshare.cdsc.com.np/")

        visible_dp_dropdown_span = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span.select2-selection__rendered"))
        )
        visible_dp_dropdown_span.click()
        time.sleep(1)

        search_input_xpath = "//input[@class='select2-search__field']"
        dp_search_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, search_input_xpath))
        )
        dp_search_input.send_keys(account["dp"])
        time.sleep(2)

        dp_option_xpath = f"//ul[contains(@id, 'select2') and contains(@id, 'results')]//li[text()='{account['dp']}']"
        dp_option = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, dp_option_xpath))
        )
        dp_option.click()
        time.sleep(1)

        selected_dp_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.select2-selection__rendered"))
        )
        actual_dp_selected = selected_dp_element.text
        print(f"[{account['username']}] Selected DP: {actual_dp_selected}")

        username_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "username"))
        )
        username_input.send_keys(account["username"])

        password_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "password"))
        )
        password_input.send_keys(account["password"])

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))
        )
        login_button.click()
        time.sleep(5)

        driver.get("https://meroshare.cdsc.com.np/#/asba")
        time.sleep(3)

        ipo_cards = driver.find_elements(By.CSS_SELECTOR, "div.company-list")
        found_valid_ipo = False
        print(ipo_cards)
        for card in ipo_cards:
            try:
                share_type = card.find_element(By.CSS_SELECTOR, "span.share-of-type").text.strip()
                share_group = card.find_element(By.CSS_SELECTOR, "span.isin").text.strip()
                print('o hello')

                if share_type == "IPO" and share_group == "Ordinary Shares":
                    print(f"[{account['username']}] Found valid IPO: ShareType='{share_type}', ShareGroup='{share_group}'")
                    # apply_button = card.find_element(By.XPATH, ".//button[contains(text(), 'Apply')]")
                    # apply_button.click()
                    apply_button = card.find_element(By.XPATH, ".//button[contains(@class, 'btn-issue') and .//i[text()='Apply']]")
                    driver.execute_script("arguments[0].click();", apply_button)  # ensures click works with Angular

                    found_valid_ipo = True
                    time.sleep(3)
                    break
            except Exception as e:
                print(f"[{account['username']}] Skipped one IPO card due to error: {e}")
                continue

        if not found_valid_ipo:
            print(f"[{account['username']}] No valid IPOs (Ordinary + IPO type) found.")
            return

  

# Click the bank dropdown
        print('ohho')
        bank_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "selectBank"))
        )
        bank_dropdown.click()
        time.sleep(1)

# Select the bank option manually (since it's Angular-styled)
        bank_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), 'CITIZENS BANK INTERNATIONAL LTD.')]"))
        )
        bank_option.click()
        time.sleep(1)

        # Wait for the Account Number dropdown to be present
        account_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "accountNumber"))
)

# Create Select object from the element
        account_dropdown = Select(account_select)

# Wait until it has more than 1 option (i.e., real accounts are loaded)
        WebDriverWait(driver, 10).until(lambda d: len(account_dropdown.options) > 1)

# Select the first actual account (not the placeholder)
        account_dropdown.select_by_index(1)

        print(f"[{account['username']}] Selected bank account: {account_dropdown.first_selected_option.text}")


# Fill branch field (readonly → remove readonly via JS)
        branch_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "selectBranch")))
        driver.execute_script("arguments[0].removeAttribute('readonly')", branch_input)
        branch_input.clear()
        branch_input.send_keys("Bhaktapur")  # <-- CHANGE THIS TO YOUR BRANCH
        time.sleep(1)

# Fill applied kitta
        applied_kitta_input = driver.find_element(By.ID, "appliedKitta")
        applied_kitta_input.clear()
        applied_kitta_input.send_keys("10")

# Fill CRN
        crn_input = driver.find_element(By.ID, "crnNumber")
        crn_input.clear()
        crn_input.send_keys(account["crn"])

# Click disclaimer checkbox
        disclaimer_checkbox = driver.find_element(By.ID, "disclaimer")
        driver.execute_script("arguments[0].click();", disclaimer_checkbox)


        proceed_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(., 'Proceed')]"))
        )
        time.sleep(1) 
        driver.execute_script("arguments[0].click();", proceed_btn)

        print(f"[{account['username']}] Proceed button clicked — application should now be submitted.")
        time.sleep(3) 

        print(f"[{account['username']}] IPO application submitted successfully.")
        time.sleep(2)


    except Exception as e:
        print(f"[{account['username']}] Failed: {str(e)}")

    finally:
        if driver:
            driver.quit()

for acc in accounts:
    apply_for_ipo(acc)




