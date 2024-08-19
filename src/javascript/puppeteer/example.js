const puppeteer = require("puppeteer");
const PuppeteerHelper = require("./puppeteer_helper");

(async () => {
  // Launch the browser and open a new page
  const browser = await puppeteer.launch({ headless: false }); // Set headless: true to run in headless mode
  const page = await browser.newPage();

  // Initialize the PuppeteerHelper with the page instance
  const puppeteerHelper = new PuppeteerHelper(page);

  // Navigate to the desired URL
  await page.goto("https://example.com");

  // Example usage of PuppeteerHelper methods

  // Type into an input element
  await puppeteerHelper.typeIntoElement("input#username", "example_user");

  // Clear the input field
  await puppeteerHelper.clearElementText("input#username");

  // Type into the input field again
  await puppeteerHelper.typeIntoElement("input#username", "example_user");

  // Click a button
  await puppeteerHelper.clickElement("button#submit");

  // Select an option from a dropdown by value
  await puppeteerHelper.selectDropdownOptionByValue(
    "select#options",
    "option2"
  );

  // Check if a specific element is present on the page
  const isPresent = await puppeteerHelper.isElementPresent(
    "div#success-message"
  );
  console.log(`Success message present: ${isPresent}`);

  // Close the browser
  await browser.close();
})();
