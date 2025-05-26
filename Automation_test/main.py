import os
import time
import configparser
from datetime import datetime

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from logger_config import setup_logger

logger = setup_logger(__name__)


def get_options(platform: str):
	config = configparser.ConfigParser()
	config.read("device_setup.ini")
	caps = config[platform.lower()]

	if platform.lower() == "android":
		options = UiAutomator2Options()
	elif platform.lower() == "ios":
		options = XCUITestOptions()
		options.platform_version = caps["platformVersion"]
	else:
		logger.error(f"Unsupported platform: {platform.lower()}")
		raise ValueError("Unsupported platform")

	options.device_name = caps["deviceName"]
	options.platform_name = caps["platformName"]
	options.browser_name = caps["browserName"]
	options.automation_name = caps["automationName"]

	return options


def take_screenshot(driver, label, folder="screenshots"):
	os.makedirs(folder, exist_ok=True)
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	filename = f"{timestamp}_{label}.png"
	path = os.path.join(folder, filename)
	driver.save_screenshot(path)
	logger.info(f"[Screenshot] Saved: {path}")


def click(driver, target_xpath):
	element = WebDriverWait(driver, 20).until(
		EC.presence_of_element_located((By.XPATH, target_xpath))
	)
	element.click()


def wait_for_page_loaded(driver, target_xpath, timeout=20):
	try:
		WebDriverWait(driver, timeout).until(
			EC.presence_of_element_located((By.XPATH, target_xpath))
		)
		logger.info("found target element")

		WebDriverWait(driver, timeout).until(
			lambda d: d.execute_script("return document.readyState") == "complete"
		)
		logger.info("loading js successfully")

	except Exception as e:
		logger.error(f"There are some error at loading page: {e}")


def click_all_card_slides(driver, folder):
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	slides = driver.find_elements(By.CSS_SELECTOR, ".cubre-o-slide__item.swiper-slide")
	valid_slides = []

	for card, slide in enumerate(slides):
		try:
			slide.find_element(By.CLASS_NAME, "cubre-m-compareCard__title")
			valid_slides.append(slide)
		except Exception as e:
			logger.debug(f"slide no. {card + 1} has no card | {e}")

	logger.info(f"found {len(valid_slides)} slides have card")

	for card, slide in enumerate(valid_slides):
		try:
			logger.info(f"Click card no. {card + 1}")
			take_screenshot(driver, f"card_{card + 1}", folder=folder)
			driver.execute_script("arguments[0].scrollIntoView(false);", slide)
			slide.click()
			time.sleep(1)
		except Exception as e:
			logger.debug(f"click card no. {card + 1} failed: {e}")


def create_screenshot_folder() -> str:
	timestamp = datetime.now().strftime("run_%Y%m%d_%H%M%S")
	folder = os.path.join("screenshots", timestamp)
	os.makedirs(folder, exist_ok=True)
	logger.info(f"Created screenshot folder: {folder}")
	return folder


def preprocess(platform: str):
	try:
		folder = create_screenshot_folder()
		config = configparser.ConfigParser()
		config.read("web.conf")
		options = get_options(platform)
		driver = webdriver.Remote("http://localhost:4723", options=options)
		logger.info("Initialized Appium driver successfully")
		return folder, config, options, driver
	except Exception as e:
		logger.error(f"Initialization error: {e}")
		return None


def test_get_all_credit_cards(driver, config, folder):
	driver.get("https://www.cathaybk.com.tw/cathaybk/")

	wait_for_page_loaded(driver, config["Xpath"]["hamburger_menu_btn"])
	take_screenshot(driver, "homepage", folder=folder)
	click(driver, config["Xpath"]["hamburger_menu_btn"])
	logger.info("Click hamburger btn successfully")

	wait_for_page_loaded(driver, config["Xpath"]["product_introduction_btn"])
	click(driver, config["Xpath"]["product_introduction_btn"])
	logger.info("Click product introduction btn successfully")

	wait_for_page_loaded(driver, config["Xpath"]["credit_card_btn"])
	click(driver, config["Xpath"]["credit_card_btn"])
	logger.info("Click credit card btn successfully")

	wait_for_page_loaded(driver, config["Xpath"]["credit_card_introduction_btn"])
	click(driver, config["Xpath"]["credit_card_introduction_btn"])
	logger.info("Click card introduction btn successfully")

	wait_for_page_loaded(driver, config["Xpath"]["credit_card_page_main_location"])
	click_all_card_slides(driver, folder)
	logger.info("Test finished")


def main(platform: str):
	logger.info(f"Starting test on: {platform}")
	setup = preprocess(platform)
	if not setup:
		logger.error("Initialization failed. Exiting.")
		return

	folder, config, options, driver = setup
	try:
		test_get_all_credit_cards(driver, config, folder)
	except Exception as e:
		logger.error(f"Test execution failed: {e}")
	finally:
		driver.quit()
		logger.info("Driver closed successfully.")


if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description="Run Appium test for specified platform.")
	parser.add_argument(
		"-p", "--platform",
		required=True,
		choices=["android", "ios"],
		help="Select the testing platform: android or ios"
	)

	args = parser.parse_args()
	main(args.platform)
