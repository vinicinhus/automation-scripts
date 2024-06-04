const puppeteer = require('puppeteer')
const ac = require("@antiadmin/anticaptchaofficial");


(async () => {
    const browser = await puppeteer.launch({ headless: false, args: ['--start-maximized'] });
    const [page] = await browser.pages();
    await page.goto('https://your_site_with/recaptchav2/Enterprise/Proxyless.com');
    await page.setViewport({ width: 1366, height: 768 });

    await page.waitForSelector('#login-id');
    await page.type('#login-id', 'my-login');

    await page.waitForSelector('#password-id');
    await page.type('#password-id', 'my-secret-password');

    await page.waitForSelector('#button-id');
    await page.click('#button-id');

    const currentUrl = page.url();

    const recaptchaSiteKey = await page.evaluate(() => {
        const scriptTags = document.querySelectorAll('script[type="text/javascript"]');
        let recaptchaSiteKey = null;
        scriptTags.forEach(tag => {
          if (tag.textContent.includes('recaptchaSiteKey')) {
            const match = /recaptchaSiteKey='(.+?)'/.exec(tag.textContent);
            if (match && match[1]) {
              recaptchaSiteKey = match[1];
            }
          }
        });
        return recaptchaSiteKey;
      });

      ac.setAPIKey('your-site-recaptcha-api-key')
      
      // Solve reCAPTCHA
      const g_response = await ac.solveRecaptchaV2EnterpriseProxyless(
        websiteURL = currentUrl,
        websiteKey = recaptchaSiteKey
      ).catch(error => console.log(error));
    
      // Use g_response in page.evaluate()
      const result = await page.evaluate((g_response) => {
        for (let client in ___grecaptcha_cfg.clients) {
          let clientObj = ___grecaptcha_cfg.clients[client];
          for (let key in clientObj) {
            if (clientObj[key] && clientObj[key].hasOwnProperty(key)) {
              if (clientObj[key][key].hasOwnProperty("callback")) {
                clientObj[key][key].callback(g_response);
                return true;
              }
            }
          }
        }
        return false;
      }, g_response);

})();
