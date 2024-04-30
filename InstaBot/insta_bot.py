import logging
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from data import USERNAME, PASSWORD, PROXY_USER, PROXY_PASS, PROXY_PORT, PROXY_HOST
from selenium_driver import get_chromedriver



logging.basicConfig(level=logging.INFO, filename="insta.log",
							format="%(asctime)s %(levelname)s %(message)s")


class InstaBot():


	def __init__(self, proxy, use_proxy, name):
		self.browser = get_chromedriver(proxy=proxy, use_proxy=use_proxy, name=name)


	def login(self):
		self.browser.get('https://www.instagram.com/accounts/login/')
		self.browser.implicitly_wait(30)
		self.browser.find_element(By.NAME, 'username').send_keys(USERNAME)
		self.browser.implicitly_wait(5)
		self.browser.find_element(By.NAME, 'password').send_keys(PASSWORD)
		self.browser.implicitly_wait(5)
		self.browser.find_element(By.XPATH, "//button[@type='submit']").click()


	def open(self):
		self.browser.get('https://www.instagram.com')


	def close(self):
		self.browser.close()
		self.browser.quit()


	def get_all_following(self, account, fsm):

		self.browser.get(f'https://www.instagram.com/{account}/')
		self.browser.implicitly_wait(3)

		# Экстраважная вещь. Индекс: 0 - посты, 1 - подписчики, 2 - на кого подписан пользователь

		following_header = self.browser.find_elements(By.CLASS_NAME, "_ac2a")[1]
		following_count = int(''.join(following_header.text.split(' ')))

		logging.info(f'Количество страниц, на которые подписан "{account}": {following_count}')

		loops_count = following_count // 6
		logging.info(f"Число итераций: {loops_count}")

		following_header.click()

		time.sleep(4)

		following_list = self.browser.find_element(By.CLASS_NAME, "_aano")

		try:
			for i in range(loops_count):
				self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", following_list)
				# self.browser.implicitly_wait(random.randrange(0, 4))
				time.sleep(random.randrange(2, 4))

			urls = []

			following_urls = following_list.find_elements(By.TAG_NAME, "a")
			for url in following_urls:
				urls.append(url.get_attribute('href'))
			following_urls = list(set(urls))

			logging.info(f'Количество собранных аккаунтов - {len(following_urls)}')

			if fsm:
				return following_urls
			else:
				# сохраняем всех на кого подписан пользователь в файл
				with open(f"{account}_followers.txt", "w") as text_file:
					for link in following_urls:
						text_file.write(link + "\n")


		except Exception as ex:
			logging.exception(ex)
			self.browser.close()
			self.browser.quit()


	def get_all_posts_urls(self, account, fsm):

		self.browser.get(f'https://www.instagram.com/{account}/')
		self.browser.implicitly_wait(3)

		posts_amount = self.browser.find_elements(By.CLASS_NAME, "_ac2a")[0]
		posts_amount = int(''.join(posts_amount.text.split(',')))

		logging.info(f'Количество постов, которые опубликовал "{account}": {posts_amount}')

		loops_count = posts_amount // 12

		posts_urls = []

		for i in range(loops_count[:3]):

			hrefs = self.browser.find_elements(By.TAG_NAME, 'a')
			hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
			posts_urls.extend(list(set(hrefs)))
			self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			self.browser.implicitly_wait(random.randrange(2, 4))


		posts_urls = list(set(posts_urls))

		if fsm:
			return posts_urls
		else:
			with open(f'{account}_linkposts.txt', 'w') as file:
				for post_url in posts_urls:
					file.write(post_url + '\n')


	def get_urls_from_description_from_all_posts(self, links):

		for link in links:
			try:
				self.browser.get(link)
				self.browser.implicitly_wait(3)
				hrefs = self.browser.find_elements(By.TAG_NAME, 'a')
				hrefs = [item.get_attribute('href') for item in hrefs if "/tags/" not in item.get_attribute('href')]
				print(hrefs)
			except TypeError:
				pass


	def send_direct_message(self, usernames="", message="", img_path=''):

		self.browser.get
		self.browser.implicitly_wait(random.randrange(2, 4))

		direct_message_button = "/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a"

		if not self.xpath_exists(direct_message_button):
			print("Кнопка отправки сообщений не найдена!")
			self.close_browser()
		else:
			print("Отправляем сообщение...")
			direct_message = browser.find_element_by_xpath(direct_message_button).click()
			self.browser.implicitly_wait(random.randrange(2, 4))

		# отключаем всплывающее окно
		if self.xpath_exists("/html/body/div[4]/div/div"):
			browser.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
		self.browser.implicitly_wait(random.randrange(2, 4))

		send_message_button = browser.find_element_by_xpath(
			"/html/body/div[1]/section/div/div[2]/div/div/div[2]/div/button").click()
		self.browser.implicitly_wait(random.randrange(2, 4))

		# отправка сообщения нескольким пользователям
		for user in usernames:
			# вводим получателя
			to_input = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/div[1]/div/div[2]/input")
			to_input.send_keys(user)
			self.browser.implicitly_wait(random.randrange(2, 4))

			# выбираем получателя из списка
			users_list = browser.find_element_by_xpath(
				"/html/body/div[4]/div/div/div[2]/div[2]").find_element_by_tag_name("button").click()
			self.browser.implicitly_wait(random.randrange(2, 4))

		next_button = browser.find_element_by_xpath(
			"/html/body/div[4]/div/div/div[1]/div/div[2]/div/button").click()
		self.browser.implicitly_wait(random.randrange(2, 4))

		# отправка текстового сообщения
		if message:
			text_message_area = browser.find_element_by_xpath(
				"/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
			text_message_area.clear()
			text_message_area.send_keys(message)
			self.browser.implicitly_wait(random.randrange(2, 4))
			text_message_area.send_keys(Keys.ENTER)
			print(f"Сообщение для {usernames} успешно отправлено!")
			self.browser.implicitly_wait(random.randrange(2, 4))

		# отправка изображения
		if img_path:
			send_img_input = browser.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/form/input")
			send_img_input.send_keys(img_path)
			print(f"Изображение для {usernames} успешно отправлено!")
			self.browser.implicitly_wait(random.randrange(2, 4))


	def ban_check(self):
		text = self.browser.find_element(By.TAG_NAME, 'span').text
		if text == 'Не удается получить доступ к сайту':
			logging.error(f'Прокси {PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT} словил бан')
		else:
			logging.error('Абсолютно непонятно, что происходит')


	def get_hat(self, url):
		self.browser.get(url)
		time.sleep(10)
		try:
			hat = self.browser.find_element(By.CSS_SELECTOR, 'div._aa_y._aa_z').find_element(By.TAG_NAME, 'header').find_element(By.TAG_NAME, 'section').text
			return hat
		except Exception:
			pass 
