"""
Day 49 - Automated Job Applications

tags: selenium webdriver
"""
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

ACCOUNT_EMAIL = "email"
ACCOUNT_PASSWORD = "password"
ACCOUNT_PHONE = "123456"
URL = (
    "https://www.linkedin.com/jobs/search/?f_LF=f_AL&geoId=102257491"
    "&keywords=python%20developer"
    "&location=London%2C%20England%2C%20United%20Kingdom"
    "&redirect=false&position=1&pageNum=0"
)

# Keep the browser open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)


def abort_application() -> None:
    """Cancel the application if it's multi-step or too complex."""
    # Click Close button
    close_button = driver.find_element(By.CLASS_NAME, value="artdeco-modal__dismiss")
    close_button.click()

    time.sleep(2)
    # Click Discard button
    discard_button = driver.find_elements(
        By.CLASS_NAME, value="artdeco-modal__confirm-dialog-btn"
    )[1]
    discard_button.click()


def main() -> None:
    """Run the main code."""
    # Click Reject Cookies button
    time.sleep(2)
    reject_button = driver.find_element(
        By.CSS_SELECTOR, value='button[action-type="DENY"]'
    )
    reject_button.click()

    # Click Sign In button
    time.sleep(2)
    signin_button = driver.find_element(By.LINK_TEXT, value="Sign in")
    signin_button.click()

    # Sign In
    time.sleep(5)
    email_field = driver.find_element(By.ID, value="username")
    email_field.send_keys(ACCOUNT_EMAIL)
    password_field = driver.find_element(By.ID, value="password")
    password_field.send_keys(ACCOUNT_PASSWORD)
    password_field.send_keys(Keys.ENTER)

    # If there's a captcha, manually enter it
    input("Press Enter when you have solved the Captcha.")

    # Get Listings
    time.sleep(5)
    all_listings = driver.find_elements(
        By.CSS_SELECTOR, value=".job-card-container--clickable"
    )

    # Apply for the jobs
    for listing in all_listings:
        print("Opening Listing")
        listing.click()
        time.sleep(2)
        try:
            # Click Apply button
            apply_button = driver.find_element(
                By.CSS_SELECTOR, value=".jobs-s-apply button"
            )
            apply_button.click()

            # Insert Phone number
            time.sleep(5)
            phone = driver.find_element(By.CSS_SELECTOR, value="input[id*=phoneNumber]")
            if phone.text is None:
                phone.send_keys(ACCOUNT_PHONE)

            # Check the Submit button
            submit_button = driver.find_element(By.CSS_SELECTOR, value="footer button")
            if submit_button.get_attribute("data-control-name") == "continue-unify":
                abort_application()
                print("Complex application, skipped.")
                continue
            else:
                # Click Submit
                print("Submitting job application.")
                submit_button.click()

            # Click Close button
            time.sleep(2)
            close_button = driver.find_element(
                By.CLASS_NAME, value="artdeco-modal__dismiss"
            )
            close_button.click()
        except NoSuchElementException:
            abort_application()
            print("No application button, skipped.")
            continue

    time.sleep(5)
    driver.quit()


if __name__ == "__main__":
    main()
