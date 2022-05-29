const puppeteer = require('puppeteer');
const path = "/Users/alessandro/Desktop/vscode/deep_eyes_recognition/dataset/images_js/";

const x_destra = [0, 273];
const x_centro = [274, 325];
const x_sinistra = [326, 781];

const y_alto = [0, 217];
const y_medio = [218, 317];
const y_basso = [318, 677];

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('https://edtech.westernu.edu/3D-eye-movement-simulator/');
    await delay(50000);

    for (let x = 0; x < x_sinistra[1]; x += 15){
        for (let y = 0; y < y_basso[1]; y += 15){
            delay(1000);
            await page.mouse.move(x, y);
            
            let percentuale_orizzontale = (x/x_sinistra[1]).toFixed(2);
            let percentuale_verticale = (y/y_basso[1]).toFixed(2);
            
            // sguardo alto destra 
            if( (x >= x_destra[0] && x <= x_destra[1]) && (y >= y_alto[0] && y <= y_alto[1]) )
                await page.screenshot({ path: `${path}alto_destra/${percentuale_orizzontale}_${percentuale_verticale}.png`});
            // sguardo alto centro 
            else if((x >= x_centro[0] && x <= x_centro[1]) && (y >= y_alto[0] && y <= y_alto[1]) )
                await page.screenshot({ path: `${path}/alto_centro/${percentuale_orizzontale}_${percentuale_verticale}.png`});
            // sguardo alto sinistra 
            else if( (x >= x_sinistra[0] && x <= x_sinistra[1]) && (y >= y_alto[0] && y <= y_alto[1]) )
                await page.screenshot({ path: `${path}/alto_sinistra/${percentuale_orizzontale}_${percentuale_verticale}.png`});
            //sguardo medio destra
            else if( (x >= x_destra[0] && x <= x_destra[1]) && (y >= y_medio[0] && y <= y_medio[1]) )
                await page.screenshot({ path: `${path}/medio_destra/${percentuale_orizzontale}_${percentuale_verticale}.png`});
            //sguardo medio centro
            else if( (x >= x_centro[0] && x <= x_centro[1]) && (y > y_medio[0] && y <= y_medio[1]) )
                await page.screenshot({ path: `${path}/medio_centro/${percentuale_orizzontale}_${percentuale_verticale}.png`});
            //sguardo medio sinistra
            else if( (x >= x_sinistra[0] && x <= x_sinistra[1]) && (y >= y_medio[0] && y <= y_medio[1]) )
                await page.screenshot({ path: `${path}/medio_sinistra/${percentuale_orizzontale}_${percentuale_verticale}.png`});
            //sguardo basso destra
            else if( (x >= x_destra[0] && x <= x_destra[1]) && (y >= y_basso[0] && y <= y_basso[1]) )
                await page.screenshot({ path: `${path}/basso_destra/${percentuale_orizzontale}_${percentuale_verticale}.png`});
            //sguardo basso centro
            else if( (x >= x_centro[0] && x <= x_centro[1]) && (y >= y_basso[0] && y <= y_basso[1]) )
                await page.screenshot({ path: `${path}/basso_centro/${percentuale_orizzontale}_${percentuale_verticale}.png`});
            //sguardo basso sinistra
            else if( (x >= x_sinistra[0] && x <= x_sinistra[1]) && (y >= y_basso[0] && y <= y_basso[1]) )
                await page.screenshot({ path: `${path}/basso_sinistra/${percentuale_orizzontale}_${percentuale_verticale}.png`});
            else
                console.log("not recognized");
        }
    }
    await browser.close();
})();

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));