const puppeteer = require('puppeteer');
const os = require("os");
const { readFileSync } = require('fs');
const { parse } = require('path');
const { report, exit } = require('process');

const arg = process.argv.slice(2);
const url = arg[0];


(async () => {
    const browser = await puppeteer.launch({
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    await page.tracing.start({ path: os.tmpdir() + "/profile.json" })
    await page.goto(url);
    await page.tracing.stop()
    await browser.close();


    let traceReportJSON = readFileSync(page.tracing._path);
    let report = JSON.parse(traceReportJSON);
    // jq '[.traceEvents[] | select(.name == "ResourceReceivedData") | .args.data.encodedDataLength | tonumber] | add' profile.json
    let uncompressedDataBytes = 0
    for (var event of report.traceEvents) {
        if (event.name == "ResourceReceivedData") {
            uncompressedDataBytes += event.args.data.encodedDataLength;
        }
    }

    const result = {
        "url": url,
        "bytes": uncompressedDataBytes,
        "kilobytes": uncompressedDataBytes / 1024
    };

    console.info("----------------------------------------------------")
    console.info("URL: " + url)
    console.info("Size: " + result.kilobytes + " KB")
    console.info("----------------------------------------------------")

    if (result.kilobytes > 512) {
        console.error("Site size is greater than 512KB.")
        exit(1);
    }
})();
