from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Replace with the Instagram username you want to scrape
username = 'thaker.prayag'

# Configure Selenium WebDriver
options = Options()
options.headless = True  # Run in headless mode (without opening a browser window)
service = Service(ChromeDriverManager().install())  # Ensure ChromeDriver is installed and managed

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=options)

try:
    # Construct URL
    url = f'https://www.instagram.com/{username}/'

    # Fetch the webpage
    driver.get(url)
    
    # Wait for profile picture to load (you may need to adjust timeout)
    driver.implicitly_wait(10)  # Maximum wait time in seconds
    
    # Find profile picture element
    img_element = driver.find_element(By.CSS_SELECTOR, 'img[class^="xpdipgo"]')  # Adjust CSS selector as per current HTML structure
    
    if img_element:
        profile_pic_url = img_element.get_attribute('src')
        print("Profile picture URL:", profile_pic_url)
    else:
        print("Profile picture not found.")
        
except Exception as e:
    print("Error fetching profile:", e)
finally:
    # Clean up resources
    driver.quit()
