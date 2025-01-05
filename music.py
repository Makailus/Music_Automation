from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # Correct import
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def search_and_play_music(song_name, headless=True):
    """
    Automates the process of searching for a song on JioSaavn, clicking the first result,
    and playing the song by clicking the 'Play' button.
    
    Parameters:
        song_name (str): The name of the song to search.
        headless (bool): Whether to run the browser in headless mode.
    """
    # Set up Chrome options
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")  # Enable headless mode
    
    # Set up the ChromeDriver using WebDriver Manager (automatically handles installation)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Go to JioSaavn's search page for the song
    search_url = f"https://www.jiosaavn.com/search/song/{song_name.replace(' ', '%20')}"
    print(f"Searching for '{song_name}' on JioSaavn...")
    driver.get(search_url)

    try:
        # Wait for the page to load and the first search result to appear
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.u-color-js-gray'))
        )

        # Click on the first song in the search results
        first_song = driver.find_element(By.CSS_SELECTOR, 'a.u-color-js-gray')
        print("Found the song! Redirecting to the song page...")
        first_song.click()

        # Wait for the song page to load and display the play button
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.c-btn.c-btn--primary[data-btn-icon="q"]'))
        )

        # Find and click the play button
        play_button = driver.find_element(By.CSS_SELECTOR, 'a.c-btn.c-btn--primary[data-btn-icon="q"]')
        print("Found play button! Playing the song...")
        play_button.click()

        # Keep the browser open to allow the song to play
        input("Press Enter to stop playback and close the browser...")

    except Exception as e:
        print("An error occurred while searching for or playing the song.")
        print(f"Error: {e}")

    # Close the browser after the task is complete
    driver.quit()

# Example usage
if __name__ == "__main__":
    song_name = input("Enter the song you want to play: ")
    headless_input = input("Do you want to run the browser in headless mode? (y/n): ").strip().lower()
    headless = headless_input == "y"  # Set headless mode based on user input
    
    search_and_play_music(song_name, headless)
