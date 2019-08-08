import random
import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener


class MyListener(AbstractEventListener):
    def before_find(self, by, value, driver):
        print(by, value)

    def after_find(self, by, value, driver):
        print(by, value, "found")

    def on_exception(self, exception, driver):
        print(exception)
        now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        driver.get_screenshot_as_file(('screenshots/{}_screen_{}.png'.format(__name__, now)))


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    wd = EventFiringWebDriver(webdriver.Chrome(options=options), MyListener())
    # wd = webdriver.Chrome(options=options)
    # print(wd.desired_capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_admin_menu_items(driver):
    driver.implicitly_wait(10)
    driver.get('http://localhost/litecart/admin')
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()
    left_menu_items = driver.find_elements_by_css_selector('ul#box-apps-menu li')
    item_count = 0
    for item in range(len(left_menu_items)):
        left_menu_items = driver.find_elements_by_css_selector('ul#box-apps-menu li#app-')
        left_menu_item_header = left_menu_items[item_count].text
        left_menu_items[item_count].click()
        item_count += 1
        left_menu_sub_items = driver.find_elements_by_css_selector('.selected li')
        sub_item_count = 0
        if len(left_menu_sub_items) > 0:
            for sub_item in range(len(left_menu_sub_items)):
                left_menu_sub_items = driver.find_elements_by_css_selector('.selected li')
                sub_item_header = left_menu_sub_items[sub_item_count].text
                left_menu_sub_items[sub_item_count].click()
                sub_item_count += 1
                assert sub_item_header != ''
        else:
            assert left_menu_item_header != ''


def test_stickers(driver):
    driver.implicitly_wait(10)
    driver.get('http://localhost/litecart/en/')
    products = driver.find_elements_by_css_selector('.product')
    for product in products:
        stickers = product.find_elements_by_css_selector('div[class^=sticker]')
        assert len(stickers) == 1
        assert product.find_element_by_css_selector('div[class^=sticker]').is_displayed()
        WebDriverWait(driver, 10).until(EC.title_is('webdriver - Пошук Google'))


def test_sorted_countries_in_table(driver):
    driver.implicitly_wait(10)
    driver.get('http://localhost/litecart/admin/?app=countries&doc=countries')
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()
    countries = driver.find_elements_by_css_selector('.dataTable a:not([title])')
    countries_list = []
    for country in countries:
        countries_list.append(country.text)
    assert sorted(countries_list) == countries_list


def test_sorted_zones(driver):
    driver.implicitly_wait(10)
    driver.get('http://localhost/litecart/admin/?app=countries&doc=countries')
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()
    zones = driver.find_elements_by_css_selector('.dataTable .row td:nth-child(6)')
    country_index = 2
    countries_with_multiple_zones = []
    for zone in zones:
        if zone.text == '0':
            country_index += 1
        else:
            countries_with_multiple_zones.append(country_index)
            country_index += 1
    for country in countries_with_multiple_zones:
        driver.get('http://localhost/litecart/admin/?app=countries&doc=countries')
        driver.find_element_by_css_selector('.dataTable .row:nth-child({}) a'.format(country)).click()
        names_list = []
        names = driver.find_elements_by_css_selector('.dataTable td:nth-child(3)')
        for name in names:
            if name.text != '':
                names_list.append(name.text)
        assert sorted(names_list) == names_list


def test_sorted_geo_zones(driver):
    driver.implicitly_wait(10)
    driver.get('http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones')
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()
    geo_zones = driver.find_elements_by_css_selector('.dataTable a:not([title])')
    country_number = 0
    for zone in geo_zones:
        driver.get('http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones')
        countries = driver.find_elements_by_css_selector('.dataTable a:not([title])')
        countries[country_number].click()
        country_number += 1
        zone_values = driver.find_elements_by_css_selector('.dataTable td:nth-child(3) option')
        final_zones_list = []
        for zone_value in zone_values:
            if zone_value.get_attribute('selected'):
                final_zones_list.append(zone_value.text)
        assert sorted(final_zones_list) == final_zones_list


def test_styles(driver):
    driver.implicitly_wait(10)
    driver.get('http://localhost/litecart/en/')
    first_product = driver.find_element_by_css_selector('#box-campaigns .product ')
    product_name_main_page = first_product.find_element_by_css_selector('.name').text
    regular_price_main_page = first_product.find_element_by_css_selector('.regular-price')
    campaign_price_main_page = first_product.find_element_by_css_selector('.campaign-price')
    line_regular_price_main_page = regular_price_main_page.value_of_css_property('text-decoration-line')
    color_campaign_price_main_page = campaign_price_main_page.value_of_css_property('color')
    first_product.click()
    product_name_product_page = driver.find_element_by_css_selector('.title[itemprop=name]').text
    regular_price_product_page = driver.find_element_by_css_selector('.regular-price')
    campaign_price_product_page = driver.find_element_by_css_selector('.campaign-price')
    line_regular_price_product_page = regular_price_product_page.value_of_css_property('text-decoration-line')
    color_campaign_price_product_page = campaign_price_product_page.value_of_css_property('color')
    assert product_name_main_page == product_name_product_page
    assert line_regular_price_main_page == line_regular_price_product_page
    assert color_campaign_price_main_page == color_campaign_price_product_page


def test_new_user_creation(driver):
    driver.implicitly_wait(10)
    mail_address = 'test_{}@test.ru'.format(random.randint(1000, 10000))
    password = 'test_qwerty_1234@#$'
    driver.get('http://localhost/litecart/en/')
    driver.find_element_by_css_selector('a[href="http://localhost/litecart/en/create_account"]').click()
    driver.find_element_by_css_selector('input[name=firstname]').send_keys('test')
    driver.find_element_by_css_selector('input[name=lastname]').send_keys('test')
    driver.find_element_by_css_selector('input[name=address1]').send_keys('test')
    driver.find_element_by_css_selector('input[name=postcode]').send_keys('222222')
    driver.find_element_by_css_selector('input[name=city]').send_keys('test')
    driver.find_element_by_css_selector('input[name=email]').send_keys(mail_address)
    driver.find_element_by_css_selector('input[name=phone]').send_keys('+7575')
    driver.find_element_by_css_selector('input[name=password]').send_keys(password)
    driver.find_element_by_css_selector('input[name=confirmed_password]').send_keys(password)
    driver.find_element_by_css_selector('button[name="create_account"]').click()
    driver.find_element_by_css_selector('a[href="http://localhost/litecart/en/logout"]').click()
    driver.find_element_by_css_selector('input[name=email]').send_keys(mail_address)
    driver.find_element_by_css_selector('input[name=password]').send_keys(password)
    driver.find_element_by_css_selector('button[name="login"]').click()
    driver.find_element_by_css_selector('a[href="http://localhost/litecart/en/logout"]').click()


def input_calendar(driver, xpath):
    driver.find_element_by_xpath(xpath).click()
    ActionChains(driver) \
        .key_down(Keys.ARROW_UP) \
        .key_up(Keys.ARROW_UP) \
        .key_down(Keys.ARROW_LEFT) \
        .key_up(Keys.ARROW_LEFT) \
        .key_down(Keys.ARROW_UP) \
        .key_up(Keys.ARROW_UP) \
        .key_down(Keys.ARROW_LEFT) \
        .key_up(Keys.ARROW_LEFT) \
        .key_down(Keys.ARROW_UP) \
        .key_up(Keys.ARROW_UP) \
        .key_down(Keys.ARROW_LEFT) \
        .key_up(Keys.ARROW_LEFT) \
        .perform()


def test_add_new_product(driver):
    driver.implicitly_wait(10)
    unique_name = 'name_{}'.format(random.randint(1000, 10000))
    driver.get('http://localhost/litecart/admin/?app=catalog&doc=catalog')
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()
    driver.find_element_by_css_selector('.button[href*="edit_product"]').click()
    driver.find_element_by_xpath("//label[contains(.,' Enabled')]").click()
    driver.find_element_by_xpath("//input[@name='name[en]']").send_keys(unique_name)
    driver.find_element_by_xpath("//td[contains(text(),'Male')]/..//input").click()
    driver.find_element_by_xpath("//input[@name='quantity']").clear()
    driver.find_element_by_xpath("//input[@name='quantity']").send_keys('10')
    driver.find_element_by_xpath("//select[@name='sold_out_status_id']").click()
    driver.find_element_by_xpath("//option[contains(text(), 'Temporary sold out')]").click()
    driver.find_element_by_xpath("//input[@name='new_images[]']").send_keys("D:\\test_image\\test_image.png")
    date_valid_from_xpath = "//input[@name='date_valid_from']"
    date_valid_to_xpath = "//input[@name='date_valid_to']"
    input_calendar(driver, date_valid_from_xpath)
    input_calendar(driver, date_valid_to_xpath)
    driver.find_element_by_xpath("//a[contains(text(),'Information')]").click()
    driver.find_element_by_xpath("//div[@class='trumbowyg-editor']").send_keys('Description')
    driver.find_element_by_xpath("//button[@name='save']").click()
    products = driver.find_elements_by_css_selector('.dataTable .row td:nth-child(3)')
    products_list = []
    for product in products:
        products_list.append(product.text)
    assert unique_name in products_list


def test_shopping_cart(driver):
    driver.implicitly_wait(3)
    for i in range(3):
        driver.get('http://localhost/litecart/en/')
        driver.find_elements_by_css_selector('.product')[i].click()
        if len(driver.find_elements_by_css_selector('.options')) != 0:
            driver.find_element_by_css_selector('.options').click()
            driver.find_elements_by_css_selector('option')[1].click()
        driver.find_element_by_css_selector('[name=add_cart_product]').click()
        wait = WebDriverWait(driver, 10)
        alert = wait.until(EC.alert_is_present())
        alert.dismiss()
        driver.refresh()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#cart .quantity'), str(i + 1)))
    driver.find_element_by_xpath("//a[contains(text(), 'Checkout »')]").click()
    item_count = len(driver.find_elements_by_css_selector('td.item'))
    for i in range(item_count):
        element = driver.find_element_by_css_selector('td.item')
        remove_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[value=Remove]')))
        remove_button.click()
        wait.until(EC.staleness_of(element))
        assert item_count - 1 == len(driver.find_elements_by_css_selector('td.item'))
        item_count -= 1


def test_new_window(driver):
    driver.implicitly_wait(3)
    driver.get('http://localhost/litecart/admin/?app=countries&doc=countries')
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()
    countries = driver.find_elements_by_css_selector('.dataTable td:nth-child(5) a')
    countries[random.randint(0, len(countries))].click()
    links = driver.find_elements_by_css_selector('.fa.fa-external-link')
    wait = WebDriverWait(driver, 10)
    for link in links:
        main_window = driver.current_window_handle
        all_windows = driver.window_handles
        link.click()
        wait.until(EC.new_window_is_opened(all_windows))
        new_window = [i for i in driver.window_handles if i not in all_windows]
        driver.switch_to.window(new_window[0])
        driver.close()
        driver.switch_to.window(main_window)


def test_category_logs(driver):
    driver.implicitly_wait(3)
    driver.get('http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=0')
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()
    goods = driver.find_elements_by_css_selector('.dataTable td:nth-child(3) a[href*=product_id]')
    for good in range(len(goods)):
        driver.find_elements_by_css_selector('.dataTable td:nth-child(3) a[href*=product_id]')[good].click()
        assert driver.get_log('browser') == []
        driver.get('http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=0')
