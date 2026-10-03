// Shared browser launch for spotlight scripts. playwright-core is installed per run in the work folder
// (npm i --prefix . playwright-core), so it resolves from the current directory.
import { createRequire } from "node:module";
import { existsSync } from "node:fs";

export async function launch(extraArgs = []) {
  const require = createRequire(process.cwd() + "/");
  let chromium;
  try {
    ({ chromium } = require("playwright-core"));
  } catch {
    console.error(`playwright-core isn't installed in ${process.cwd()}; run: npm i --prefix . playwright-core`);
    process.exit(2);
  }
  const executablePath = process.env.CHROMIUM || [
    "/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/Applications/Chromium.app/Contents/MacOS/Chromium",
  ].find(existsSync);  // undefined: playwright's own downloaded browser
  return chromium.launch({
    executablePath,
    args: ["--no-sandbox", "--force-color-profile=srgb", "--font-render-hinting=none", "--disable-gpu", ...extraArgs],
  });
}
