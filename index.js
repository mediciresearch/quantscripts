const puppeteer = require("puppeteer-extra");
const axios = require("axios");
const fs = require("fs");

// add stealth plugin and use defaults (all evasion techniques)
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
puppeteer.use(StealthPlugin());

puppeteer.use(
  require("puppeteer-extra-plugin-user-preferences")({
    timeout: 30000,
    ignoreHTTPSErrors: true,
    userPrefs: {
      download: {
        prompt_for_download: false,
        open_pdf_in_system_reader: true,
      },
      plugins: {
        always_open_pdf_externally: false, // this should do the trick
      },
    },
  })
);

const executablePath =
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"; // Replace this with the path to your Chrome executable

puppeteer
  .launch({ executablePath: executablePath, headless: false })
  .then(async (browser) => {
    const page = await browser.newPage();

    // Set the download behavior for the browser
    const client = await page.target().createCDPSession();
    await client.send("Page.setDownloadBehavior", {
      behavior: "allow",
      downloadPath: "../notion", // Set your desired download directory here
    });

    await page.goto(
      "https://adamsstudymaterial.notion.site/Possibly-EVERY-Trading-Book-1b633f36da114214aab9aeaffb8a07be"
    );
    await page.waitForTimeout(1000);

    let i = 1;
    while (true) {
      const selector = `#notion-app > div > div:nth-child(1) > div > div:nth-child(1) > main > div > div.whenContentEditable > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(${i}) > div > div > div`;

      // Check if the item exists
      const itemExists = await page.$(selector);

      if (!itemExists) {
        console.log(`Item ${i} not found. Exiting loop.`);
        break;
      }

      // Set up a promise to capture the new tab/page when it's created
      const newPagePromise = new Promise((p) =>
        browser.once("targetcreated", (target) => p(target.page()))
      );

      // Click on the link to open the content in a new tab
      await page.click(selector);

      // Get the new page when it's created
      const newPage = await newPagePromise;
      // print("Tab opened");

      // Get the current URL of the new tab.
      const pdfUrl = await newPage.url();
      // print("pdf url attained");

      // await newPage.waitForTimeout(5000);

      if (pdfUrl && pdfUrl !== "about:blank") {
        // Parse the URL and extract the downloadNameParameter
        const urlObj = new URL(pdfUrl);
        const filename = urlObj.searchParams.get("downloadName");

        if (filename) {
          const response = await axios.get(pdfUrl, { responseType: "stream" });

          // Create a write stream to save the PDF using the filename
          const writer = fs.createWriteStream(`../notion/${filename}`);

          // Pipe the response stream into the write stream
          response.data.pipe(writer);

          await new Promise((resolve, reject) => {
            writer.on("finish", resolve);
            writer.on("error", reject);
          });
        } else {
          console.error("Failed to extract filename from URL.");
        }
      }

      // Wait for the download to complete. Adjust the wait time based on your needs.
      await newPage.waitForTimeout(2000); // Wait for 10 seconds or any other specific selector

      // Optionally, after the download is complete, close the new tab
      await newPage.close();

      i++; // Increment the value for the next iteration
    }
    // Continue with any other actions on the main page or close the browser
    await browser.close();
  });
