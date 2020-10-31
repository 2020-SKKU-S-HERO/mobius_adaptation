var webdriver = require('selenium-webdriver');
var By = require('selenium-webdriver').By;
var cheerio = require('cheerio');
var request = require('request');

var chromeCapabilities = webdriver.Capabilities.chrome()
var chromeOptions = {
	'args': ["--headless","--no-sandbox","--disable-dev-shm-usage"]
};
chromeCapabilities.set('chromeOptions', chromeOptions);
var url = "ets.krx.co.kr/contents/ETS/03/03010000/ETS03010000.jsp";
(async function example(){
	var driver = await new webdriver.Builder()
		.forBrowser("chrome")
		.withCapabilities(chromeCapabilities)
		.build();
	try{
		await driver.get(url);
	} finally{
		await driver.quit();
	}
})();
