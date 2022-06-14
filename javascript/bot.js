//importing modules
const puppeteer = require('puppeteer');
const path = require('./config.js');

//importing consts from config.js
save_path = path.save_path;
classes = path.classes;

const x_right = path.coords.x_right;
const x_center = path.coords.x_center;
const x_left = path.coords.x_left;

const y_high = path.coords.y_high;
const y_middle = path.coords.y_middle;
const y_low = path.coords.y_low;

//start program
(async () => {
    //browser launch
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    //setting window size
    await page.setViewport({width: 1511, height: 792});
    await page.goto('https://edtech.westernu.edu/3D-eye-movement-simulator/');
    await delay(60000);
    
    //hiding blinking clicking button
    await page.mouse.click(629, 674);
    await delay(5000);
    
    //hiding text clicking button
    await page.mouse.click(754, 674);
    await delay(5000);
    
    //filtering and saving images
    for (let x = x_right[0]; x < x_left[1]; x += 25){
        for (let y = y_high[0]; y < y_low[1]; y += 20){
            await delay(2000);
            await page.mouse.move(x, y);
            
            //normalization of perc
            let hor_perc = ((x-x_right[0])/(x_left[1]-x_right[0])).toFixed(2);
            let ver_perc = ((y-y_high[0])/(y_low[1]-y_high[0])).toFixed(2);
            
            // high right
            if( (x >= x_right[0] && x <= x_right[1]) && (y >= y_high[0] && y <= y_high[1]) )
                await page.screenshot({ path: `${save_path}/${classes[0]}/${hor_perc}_${ver_perc}.png`});
            // high center
            else if((x >= x_center[0] && x <= x_center[1]) && (y >= y_high[0] && y <= y_high[1]) )
                await page.screenshot({ path: `${save_path}/${classes[1]}/${hor_perc}_${ver_perc}.png`});
            // high left 
            else if( (x >= x_left[0] && x <= x_left[1]) && (y >= y_high[0] && y <= y_high[1]) )
                await page.screenshot({ path: `${save_path}/${classes[2]}/${hor_perc}_${ver_perc}.png`});
            // middle right 
            else if( (x >= x_right[0] && x <= x_right[1]) && (y >= y_middle[0] && y <= y_middle[1]) )
                await page.screenshot({ path: `${save_path}/${classes[3]}/${hor_perc}_${ver_perc}.png`});
            // middle center 
            else if( (x >= x_center[0] && x <= x_center[1]) && (y > y_middle[0] && y <= y_middle[1]) )
                await page.screenshot({ path: `${save_path}/${classes[4]}/${hor_perc}_${ver_perc}.png`});
            // middle left 
            else if( (x >= x_left[0] && x <= x_left[1]) && (y >= y_middle[0] && y <= y_middle[1]) )
                await page.screenshot({ path: `${save_path}/${classes[5]}/${hor_perc}_${ver_perc}.png`});
            // low right 
            else if( (x >= x_right[0] && x <= x_right[1]) && (y >= y_low[0] && y <= y_low[1]) )
                await page.screenshot({ path: `${save_path}/${classes[6]}/${hor_perc}_${ver_perc}.png`});
            // low center 
            else if( (x >= x_center[0] && x <= x_center[1]) && (y >= y_low[0] && y <= y_low[1]) )
                await page.screenshot({ path: `${save_path}/${classes[7]}/${hor_perc}_${ver_perc}.png`});
            // low left 
            else if( (x >= x_left[0] && x <= x_left[1]) && (y >= y_low[0] && y <= y_low[1]) )
                await page.screenshot({ path: `${save_path}/${classes[8]}/${hor_perc}_${ver_perc}.png`});
            else
                console.log("not recognized");
        }
    }
    await browser.close();
    })();

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));