const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('https://edtech.westernu.edu/3D-eye-movement-simulator/');
    await delay(15000);

    await page.mouse.move(386,589);
    await delay(1000);
    await page.mouse.click(386,589);

    const path = "/Users/alessandro/Desktop/vscode/deep_eyes_recognition/dataset/images_js/";

    const x_min = 0; 
    const x_max_dx = 273;
    const x_destra = (x_min, x_max_dx);
    const x_max_cx = 325;
    const x_centro = (x_max_dx, x_max_cx);
    const x_max = 781;
    const x_max_sx = (x_max_cx, x_max);

    const y_min = 0;
    const y_max_dx = 217;
    const y_destra = (y_min, y_max_dx);
    const y_max_cx = 317;
    const y_centro = (y_max_dx, y_max_cx);
    const y_max = 677;
    const y_sinistra = (y_max_cx, y_max);

    for(let x = 0; x < sinistra; x += 15){
        for(let y = 0; y < basso; y += 15){
            await page.mouse.move(x, y);
            let percentuale_orizzontale = (x/sinistra).toFixed(2);
            let percentuale_verticale = (y/basso).toFixed(2);
            switch (x, y){
                // sguardo alto destra 
                case( (x > [0] && x < [1]) && (y > [0] && y < [1]) ): {
                    await page.screenshot({ path: `${path}alto_destra/(${percentuale_orizzontale}_${percentuale_verticale}).png`});
                    break;
                }
                //sguardo alto centro
                case( (x > [0] && x < [1]) && (y > [0] && y < [1]) ): {
                    await page.screenshot({ path: `${path}/alto_centro/(${percentuale_orizzontale}_${percentuale_verticale}).png`});
                    break;
                }
                //sguardo alto sinistra
                case( (x > [0] && x < [1]) && (y > [0] && y < [1]) ): {
                    await page.screenshot({ path: `${path}/alto_sinistra/(${percentuale_orizzontale}_${percentuale_verticale}).png`});
                    break;
                }
                //sguardo medio destra
                case( (x > [0] && x < [1]) && (y > [0] && y < [1]) ): {
                    await page.screenshot({ path: `${path}/(${percentuale_orizzontale}_${percentuale_verticale}).png`});
                    break;
                }
                //sguardo medio centro
                case( (x > [0] && x < [1]) && (y > [0] && y < [1]) ): {
                    await page.screenshot({ path: `${path}/medio_centro/(${percentuale_orizzontale}_${percentuale_verticale}).png`});
                    break;
                }
                //sguardo medio sinistra
                case( (x > [0] && x < [1]) && (y > [0] && y < [1]) ): {
                    await page.screenshot({ path: `${path}/medio_sinistra/(${percentuale_orizzontale}_${percentuale_verticale}).png`});
                    break;
                }
                //sguardo basso destra
                case( (x > [0] && x < [1]) && (y > [0] && y < [1]) ): {
                    await page.screenshot({ path: `${path}/basso_destra/(${percentuale_orizzontale}_${percentuale_verticale}).png`});
                    break;
                }
                //sguardo basso centro
                case( (x > [0] && x < [1]) && (y > [0] && y < [1]) ): {
                    await page.screenshot({ path: `${path}/basso_centro/(${percentuale_orizzontale}_${percentuale_verticale}).png`});
                    break;
                }

                //sguardo basso sinistra
                case( (x > [0] && x < [1]) && (y > [0] && y < [1]) ): {
                    await page.screenshot({ path: `${path}/basso_sinistra/(${percentuale_orizzontale}_${percentuale_verticale}).png`});
                    break;
                }
                //else
                default: {
                    break;
                }
            }
        }
    }
    await browser.close();
})();

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));