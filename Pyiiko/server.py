# -*- coding: utf-8 -*-
import requests
import hashlib
from lxml import etree
from io import StringIO

DEFAULT_TIMEOUT = 4


class IikoServer:
    def __init__(self, ip, login, password, token=None):

        self.login = login
        self.password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        self.address = 'http://' + ip + '/resto/'
        self._token = (token or self.get_token())

    def token(self):
        return self._token

    def get_token(self):
        """Получение токена"""

        try:
            url = self.address + 'api/auth?login=' + self.login + "&pass=" + self.password
            return requests.get(url=url, timeout=DEFAULT_TIMEOUT).text

        except Exception as e:
            print(e)

    def quit(self):
        """Уничтожение токена"""

        try:
            logout = requests.get(
                self.address + 'api/logout?key=' + self._token).text
            print("\nТокен уничтожен: " + self._token)
            return logout

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def version(self):
        """Версия iiko"""
        try:
            ver = requests.get(
                self.address + '/get_server_info.jsp?encoding=UTF-8').text
            tree = etree.parse(StringIO(ver))
            version = ''.join(tree.xpath(r'//version/text()'))
            return version

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    "----------------------------------Корпорации----------------------------------"

    def departments(self):
        """Иерархия подразделений"""
        try:
            urls = self.address + "api/corporation/departments?key=" + self._token
            return requests.get(url=urls, timeout=DEFAULT_TIMEOUT).content
        except Exception as e:
            print(e)

    def stores(self):
        """Список складов"""
        try:
            ur = self.address + 'api/corporation/stores?key=' + self._token
            return requests.get(ur, timeout=DEFAULT_TIMEOUT).content
        except Exception as e:
            print(e)

    def groups(self):
        """Список групп и отделений"""
        try:
            ur = self.address + 'api/corporation/groups?key=' + self._token
            return requests.get(ur, timeout=DEFAULT_TIMEOUT).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def terminals(self):
        """Терминалы"""
        try:
            ur = self.address + 'api/corporation/terminals?key=' + self._token
            return requests.get(ur, timeout=DEFAULT_TIMEOUT).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def departments_find(self, **kwargs):
        """Поиск подразделения"""
        try:
            ur = self.address + 'api/corporation/departments/search?key=' + self._token
            return requests.get(
                ur, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def stores_find(self, code):
        """Список складов"""
        try:
            ur = self.address + 'api/corporation/stores/search?key=' + self._token
            return requests.get(ur, params=code).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def groups_search(self, **kwargs):
        """Поиск групп отделений"""
        try:
            urls = self.address + 'api/corporation/terminal/search?key=' + self._token
            return requests.get(
                url=urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def terminals_search(self, anonymous=False, **kwargs):
        """Поиск терминала"""
        try:
            urls = self.address + 'api/corporation/terminal/search?key=' + self._token + '&anonymous=' + anonymous
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    "----------------------------------Работники----------------------------------"

    def employees(self):
        """Работники"""
        try:
            urls = self.address + 'api/employees?key=' + self._token
            return requests.get(urls, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    "----------------------------------События----------------------------------"

    def events(self, **kwargs):
        """События"""
        try:
            ur = self.address + 'api/events?key=' + self._token
            return requests.get(
                ur, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def events_filter(self, body):
        """Список событий по фильтру событий и номеру заказа"""
        try:
            ur = self.address + 'api/events?key=' + self._token
            return requests.post(
                ur, data=body, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def events_meta(self):
        """Дерево событий"""
        try:
            urls = self.address + 'api/events/metadata?key=' + self._token
            return requests.get(urls, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    "----------------------------------Продукты----------------------------------"

    def products(self, includeDeleted=True):
        """Номенклатура"""
        try:
            urls = self.address + 'api/products?key=' + self._token
            return requests.get(
                urls, params=includeDeleted, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def products_find(self, **kwargs):
        """Номенклатура"""
        try:
            urls = self.address + 'api/products/search/?key=' + self._token
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    "----------------------------------Поставщики----------------------------------"

    def suppliers(self):
        """Список всех поставщиков"""
        try:
            urls = self.address + 'api/suppliers?key=' + self._token
            return requests.get(urls, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def suppliers_find(self, name='', code=''):
        """Поиск поставщика"""
        try:
            urls = self.address + 'api/suppliers?key=' + self._token
            payload = {'name': name, 'code': code}
            return requests.get(
                urls, params=payload, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def suppliers_price(self, code, date=None):
        """Поиск поставщика"""
        try:
            urls = self.address + '/resto/api/suppliers/' + code + '/pricelist?key=' + self._token
            return requests.get(
                urls, params=date, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    "----------------------------------Отчеты----------------------------------"

    def olap(self, **kwargs):
        """OLAP-отчет"""
        try:
            urls = self.address + '/resto/api/reports/olap?key' + self._token
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def store_operation(self, **kwargs):
        """Отчет по складским операциям"""
        try:
            urls = self.address + '/resto/api/reports/storeOperations?key=' + self._token
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def store_presets(self):
        """Пресеты отчетов по складским операциям"""
        try:
            urls = self.address + '/resto/api/reports/storeReportPresets?key=' + self._token
            return requests.get(urls, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def product_expense(self, departament, **kwargs):
        """Расход продуктов по продажам"""
        try:
            urls = self.address + '/resto/api/reports/productExpense?key=' + self._token + \
                   '&department=' + departament
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def sales(self, departament, **kwargs):
        """Отчет по выручке"""

        try:
            urls = self.address + '/resto/api/reports/sales?key=' + self._token + \
                   '&department=' + departament
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def mounthly_plan(self, departament, **kwargs):
        """План по выручке за день"""
        try:
            urls = self.address + '/resto/api/reports/monthlyIncomePlan?key=' + self._token + \
                   '&department=' + departament
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def ingredient_entry(self, departament, **kwargs):
        """Отчет о вхождении товара в блюдо"""
        try:
            urls = self.address + '/resto/api/reports/ingredientEntry?key=' + self._token + \
                   '&department=' + departament
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def olap2(self, **kwargs):
        """Поля OLAP-отчета"""
        try:
            urls = self.address + '/resto/api/v2/reports/olap/columns?key=' + self._token
            return requests.get(urls, params=kwargs, timeout=DEFAULT_TIMEOUT).json()

        except Exception as e:
            print(e)

    "----------------------------------Накладные----------------------------------"

    def invoice_in(self, **kwargs):
        """Выгрузка приходных накладных"""
        try:
            urls = self.address + '/resto/api/documents/export/incomingInvoice?key=' + self._token
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def invoice_out(self, **kwargs):
        """Выгрузка расходных накладных"""
        try:
            urls = self.address + '/resto/api/documents/export/outgoingInvoice?key=' + self._token
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def invoice_number_in(self, current_year=True, **kwargs):
        """Выгрузка приходной накладной по ее номеру"""

        try:
            urls = self.address + '/resto/api/documents/export/incomingInvoice/byNumber?key=' \
                   + self._token + '&currentYear' + current_year
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def invoice_number_out(self, current_year=True, **kwargs):
        """Выгрузка расходной накладной по ее номеру"""
        try:
            urls = self.address + '/resto/api/documents/export/outgoingInvoice/byNumber?key=' \
                   + self._token + '&currentYear' + current_year
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def production_doc(self, token, xml):
        """Загрузка акта приготовления"""
        try:
            target_url = self.address + '/api/documents/import/productionDocument?key' + token
            headers = {'Content-type': 'text/xml'}
            return requests.post(
                target_url, body=xml, headers=headers,
                timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    "----------------------------------Получение данных по кассовым сменам:----------------------------------"

    def close_session(self, **kwargs):
        """Список кассовых смен"""
        try:
            urls = self.address + 'resto/api/closeSession/list?key=' \
                   + self._token
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def session(self, start=None, end=None):
        """Информация о кассовых сменах"""
        try:
            urls = self.address + '/resto/api/events/sessions?key=' \
                   + self._token + '&from_time=' + start + '&to_time=' + end
            return requests.get(urls, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    "----------------------------------EDI----------------------------------"

    def edi(self, edi, gln, inn='', kpp='', name=''):
        """Список заказов для участника EDI senderId и поставщика seller"""
        try:
            urls = self.address + 'edi/' + edi + '/orders/bySeller'
            payload = {'gln': gln, 'inn': inn, 'kpp': kpp, 'name': name}
            return requests.get(
                urls, params=payload, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)
