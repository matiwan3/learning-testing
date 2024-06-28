const puppeteer = require('puppeteer');
const URL_LIST = require('./constants/url');
const SAFE_SCRAP_DELAY = 2000;

function getFormattedDate() {
    let date = new Date();
    return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}-${date.getHours().toString().padStart(2, '0')}-${date.getMinutes().toString().padStart(2, '0')}`;
}

function delay(time) {
    return new Promise(function (resolve) {
        setTimeout(resolve, time);
    });
}

async function getSiteData(url) {
    return new Promise(async (resolve, reject) => {
        try {
            const browser = await puppeteer.launch();
            let domain = url.match(/www\.(.*?)\./)[1];
            const page = await browser.newPage();
            await page.goto(url);
            await delay(SAFE_SCRAP_DELAY);
            let formattedDate = getFormattedDate();
            await page.screenshot({ path: `screenshots/${domain}-${formattedDate}.png` });
            await delay(1000);
            const data = await page.title();
            await browser.close();
            resolve(data);
        } catch (e) {
            reject(e);
        }
    });
}


try {
    if (URL_LIST !== null) {
        console.log(URL_LIST);
        for (key in URL_LIST) {
            {
                getSiteData(URL_LIST[key]).then((data) => {
                    console.log(data);
                }).catch((e) => {
                    console.log(e);
                });
            }
        }
    }
} catch (e) {
    console.log(e);
}