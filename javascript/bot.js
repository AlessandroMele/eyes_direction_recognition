const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();//{headless: false, executablePath: '/Applications/Firefox.app/'} );
  const page = await browser.newPage();
  await page.goto('https://edtech.westernu.edu/3D-eye-movement-simulator/');
  await delay(15000);
  
  //trying to hide laterals text
  await page.mouse.move(586, 678);
  await delay(1000);
  await page.mouse.click(586, 678);


  await page.mouse.move(386,589);
  await delay(1000);
  await page.mouse.click(386,589);

  const path = "/Users/alessandro/Desktop/vscode/deep_eyes_recognition/dataset/images_js/";
  const sinistra = 0;
  const destra = 781;
  const centro_sinistra = 325;
  const centro_destra = 481;
  const centro_verticale = 273;

  // sguardo a sinistra 
  for (let i=sinistra; i<centro_sinistra; i+=15) {
    await page.mouse.move(i,centro_verticale);
    let percentuale_orizzontale = (i/destra).toFixed(2);
    await page.screenshot({ path: `${path}(${percentuale_orizzontale}, 50).png`});
  }
  // sguardo al centro
  for (let i=centro_sinistra; i<centro_destra; i+=15) {
    await page.mouse.move(i,centro_verticale);
    let percentuale_orizzontale = (i/destra).toFixed(2);
    await page.screenshot({ path: `${path}(${percentuale_orizzontale}, 50).png`});
  }
  // sguardo a destra
  for (let i=centro_destra; i<destra; i+=15) {
    await page.mouse.move(i,centro_verticale);
    let percentuale_orizzontale = (i/destra).toFixed(2);
    await page.screenshot({ path: `${path}(${percentuale_orizzontale}, 50).png`});
  }

  const centro_orizzontale = 396;
  const alto = 0;
  const basso = 677;
  const alto_centro = 217;
  const basso_centro = 317;

  // sguardo in alto
  for (let i=alto; i<alto_centro; i+=12) {

    await page.mouse.move(centro_orizzontale,i);
    let percentuale_verticale = (i/basso).toFixed(2);
    await page.screenshot({ path: `${path}(50, ${percentuale_verticale}).png`});
  }

  // sguardo al centro
  for (let i=alto_centro; i<basso_centro; i+=12) {

    await page.mouse.move(centro_orizzontale,i);
      let percentuale_verticale = (i/basso).toFixed(2);
      await page.screenshot({ path: `${path}(50, ${percentuale_verticale}).png`});
    }

  // sguardo in basso
  for (let i=basso_centro; i<basso; i+=18) {

    await page.mouse.move(centro_orizzontale,i);
    let percentuale_verticale = (i/basso).toFixed(2);
    await page.screenshot({ path: `${path}(50, ${percentuale_verticale}).png`});
  }

  await browser.close();
})();

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));