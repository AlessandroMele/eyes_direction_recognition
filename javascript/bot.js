const path = require('./path.js');
save_path = path.save_path;
classes = path.classes;

const puppeteer = require('puppeteer');

const x_destra = [460, 670];
const x_centro = [671, 800];
const x_sinistra = [801, 1050];

const y_alto = [205, 290];
const y_medio = [291, 375];
const y_basso = [376, 475];

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setViewport({width: 1511, height: 792});
    await page.goto('https://edtech.westernu.edu/3D-eye-movement-simulator/');
    await delay(40000);
    
    //hiding blinking
    await page.mouse.click(629, 674);
    await delay(4000);
    
    //hiding text
    await page.mouse.click(754, 674);
    await delay(4000);
    
    for (let x = x_destra[0]; x < x_sinistra[1]; x += 50){
        for (let y = y_alto[0]; y < y_basso[1]; y += 40){
            await delay(2000);
            await page.mouse.move(x, y);
            
            let percentuale_orizzontale = ((x-x_destra[0])/x_sinistra[1]).toFixed(2);
            let percentuale_verticale = ((y-y_alto[0])/y_basso[1]).toFixed(2);
            
            // sguardo alto destra
            if( (x >= x_destra[0] && x <= x_destra[1]) && (y >= y_alto[0] && y <= y_alto[1]) )
                await page.screenshot({ path: `${save_path}/${classes[0]}/${percentuale_orizzontale}_${percentuale_verticale}.png`});
            // sguardo alto centro 
            else if((x >= x_centro[0] && x <= x_centro[1]) && (y >= y_alto[0] && y <= y_alto[1]) )
                await page.screenshot({ path: `${save_path}/${classes[1]}/${percentuale_orizzontale}_${percentuale_verticale}.png`});
            // sguardo alto sinistra 
            else if( (x >= x_sinistra[0] && x <= x_sinistra[1]) && (y >= y_alto[0] && y <= y_alto[1]) )
                await page.screenshot({ path: `${save_path}/${classes[2]}/${percentuale_orizzontale}_${percentuale_verticale}.png`});
            //sguardo medio destra
            else if( (x >= x_destra[0] && x <= x_destra[1]) && (y >= y_medio[0] && y <= y_medio[1]) )
                await page.screenshot({ path: `${save_path}/${classes[3]}/${percentuale_orizzontale}_${percentuale_verticale}.png`});
            //sguardo medio centro
            else if( (x >= x_centro[0] && x <= x_centro[1]) && (y > y_medio[0] && y <= y_medio[1]) )
                await page.screenshot({ path: `${save_path}/${classes[4]}/${percentuale_orizzontale}_${percentuale_verticale}.png`});
            //sguardo medio sinistra
            else if( (x >= x_sinistra[0] && x <= x_sinistra[1]) && (y >= y_medio[0] && y <= y_medio[1]) )
                await page.screenshot({ path: `${save_path}/${classes[5]}/${percentuale_orizzontale}_${percentuale_verticale}.png`});
            //sguardo basso destra
            else if( (x >= x_destra[0] && x <= x_destra[1]) && (y >= y_basso[0] && y <= y_basso[1]) )
                await page.screenshot({ path: `${save_path}/${classes[6]}/${percentuale_orizzontale}_${percentuale_verticale}.png`});
            //sguardo basso centro
            else if( (x >= x_centro[0] && x <= x_centro[1]) && (y >= y_basso[0] && y <= y_basso[1]) )
                await page.screenshot({ path: `${save_path}/${classes[7]}/${percentuale_orizzontale}_${percentuale_verticale}.png`});
            //sguardo basso sinistra
            else if( (x >= x_sinistra[0] && x <= x_sinistra[1]) && (y >= y_basso[0] && y <= y_basso[1]) )
                await page.screenshot({ path: `${save_path}/${classes[8]}/${percentuale_orizzontale}_${percentuale_verticale}.png`});
            else
                console.log("not recognized");
        }
    }
    await browser.close();
    })();

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));