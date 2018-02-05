#!/usr/bin/env python3

import unittest
import os
import docker
from selenium import webdriver
import os.path
from testpack_helper_library.unittests.dockertests import Test1and1Common


class Test1and1NginxImage(Test1and1Common):
    @classmethod
    def setUpClass(cls):
        Test1and1Common.setUpClass()
        Test1and1Common.copy_test_files("testpack/files", "html", "/var/www")

    def check_success(self, page):
        driver = webdriver.PhantomJS()
        driver.get("http://%s:8080/%s" % (Test1and1Common.container_ip, page))
        self.assertTrue(
            driver.page_source.find('Success') > -1,
            msg="No success for %s" % page
        )

    def file_mode_test(self, filename: str, mode: str):
        # Compare (eg) drwx???rw- to drwxr-xrw-
        result = self.execRun("ls -ld %s" % filename)
        self.assertFalse(
            result.find("No such file or directory") > -1,
            msg="%s is missing" % filename
        )
        for char_count in range(0, len(mode)):
            self.assertTrue(
                mode[char_count] == '?' or (mode[char_count] == result[char_count]),
                msg="%s incorrect mode: %s" % (filename, result)
            )

    # <tests to run>

    def test_docker_logs(self):
        expected_log_lines = [
            "Loading php config",
            "Loading plugin /opt/configurability/goplugins/php.so"
        ]
        container_logs = self.container.logs().decode('utf-8')
        for expected_log_line in expected_log_lines:
            self.assertTrue(
                container_logs.find(expected_log_line) > -1,
                msg="Docker log line missing: %s from (%s)" % (expected_log_line, container_logs)
            )

    def test_nginx_var_www_html(self):
        self.file_mode_test("/var/www/html", "drwxrwxrwx")

    def test_php_curl(self):
        self.check_success("curltest.php")

    def test_php_gd(self):
        self.check_success("gdtest.php")

    def test_php_gettext(self):
        self.check_success("gettexttest.php")

    def test_php_imagick(self):
        self.check_success("imagicktest.php")

    def test_php_imap(self):
        self.check_success("imaptest.php")

    def test_php_intl(self):
        self.check_success("intltest.php")

    def test_php_mbstring(self):
        self.check_success("mbstringtest.php")

    def test_php_mcrypt(self):
        self.check_success("mcrypttest.php")

    def test_php_mysql(self):
        self.check_success("mysqltest.php")

    def test_php_phpversion(self):
        self.check_success("phpversion.php")

    def test_php_soap(self):
        self.check_success("soaptest.php")

    def test_php_sqlite(self):
        self.check_success("sqlitetest.php")

    def test_php_xml(self):
        self.check_success("xmltest.php")

    def test_php_zip(self):
        self.check_success("ziptest.php")

    def test_php_info(self):
        # We need to set the desired headers, then get a new driver for this to work
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.X-Forwarded-For'] = "1.2.3.4"
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.X-Forwarded-Port'] = "99"
        driver = webdriver.PhantomJS()
        driver.get("http://%s:8080/phpinfo.php" % Test1and1Common.container_ip)
        self.assertTrue(
            driver.page_source.find("REMOTE_ADDR']</td><td class=\"v\">1.2.3.4") > -1,
            msg="phpinfo not showing REMOTE_ADDR=1.2.3.4 "
        )
        self.assertTrue(
            driver.page_source.find("SERVER_PORT']</td><td class=\"v\">99") > -1,
            msg="phpinfo not showing SERVER_PORT=99"
        )

    # </tests to run>

if __name__ == '__main__':
    unittest.main(verbosity=1)
