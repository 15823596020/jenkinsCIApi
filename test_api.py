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
    def login(self, username="user01", password="pwd"):
        url = "http://106.53.223.46:9091/api/v1/user/login"
        data = {
            "authRequest": {
                "userName": username,
                "password": password
            }
        }
        return requests.post(url, json=data).json()

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

    def test_get_list(self):
        heard = self.get_headers()
        url = "http://106.53.223.46:9091/api/v1/menu/list"
        ret = requests.get(url, headers=heard).json()
        menu_name = jsonpath.jsonpath(ret, "$..menu_name")
        pytest.assume(len(menu_name) == 18)
        pytest.assume("烧饼" in menu_name)

    @pytest.mark.parametrize("oder_list,rst", yaml.safe_load(open("order.yaml")))
    def test_confirm(self, oder_list, rst):
        heard = self.get_headers()
        data = oder_list
        url = "http://106.53.223.46:9091/api/v1/menu/confirm"
        ret = requests.post(url, headers=heard, json=data).json()
        pytest.assume(rst["total"] == ret["total"])
        pytest.assume(rst["total_price"] == ret["total_price"])
