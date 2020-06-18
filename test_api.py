#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/6/16 
# @Author : ytq
# @File : test_api.py
# @Software: PyCharm

import jsonpath
import pytest
import requests
import yaml


class TestDemo:
    __login_url = "http://106.53.223.46:9091/api/v1/user/login"
    __list_url = "http://106.53.223.46:9091/api/v1/menu/list"
    __logout_url = "http://106.53.223.46:9091/api/v1/user/logout"
    __confirm_url = "http://106.53.223.46:9091/api/v1/menu/confirm"

    def login(self, username="user01", password="pwd"):
        data = {
            "authRequest": {
                "userName": username,
                "password": password
            }
        }
        return requests.post(self.__login_url, json=data).json()

    def get_headers(self):
        access_token = self.login()["access_token"]
        return {
            'access_token': access_token
        }

    @pytest.mark.parametrize("username, password,rst",
                             [("user01", "pwd", "200"), ("user10", "pwd1", "401"), ("user20", "pwd", "401")])
    def test_login(self, username, password, rst):
        ret = self.login(username, password)
        assert ret["code"] == rst

    @pytest.mark.parametrize("username, password,rst",
                             [("user01", "pwd", "200"), ("user10", "pwd1", "401"), ("user20", "pwd", "401")])
    def test_logout(self, username, password, rst):
        login_ret = self.login(username, password)
        if login_ret["code"] == "200":
            access_token = login_ret["access_token"]
        else:
            access_token = None
        headers = {"access_token": access_token}
        ret = requests.delete(self.__logout_url, headers=headers).json()
        assert ret["code"] == rst

    def test_get_list(self):
        heard = self.get_headers()
        ret = requests.get(self.__list_url, headers=heard).json()
        menu_name = jsonpath.jsonpath(ret, "$..menu_name")
        pytest.assume(len(menu_name) == 18)
        pytest.assume("烧饼" in menu_name)

    @pytest.mark.parametrize("oder_list,rst", yaml.safe_load(open("order.yaml")))
    def test_confirm(self, oder_list, rst):
        heard = self.get_headers()
        data = oder_list
        ret = requests.post(self.__confirm_url, headers=heard, json=data).json()
        pytest.assume(rst["total"] == ret["total"])
        pytest.assume(rst["total_price"] == ret["total_price"])
