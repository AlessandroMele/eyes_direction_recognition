/***********************************/

//node dependency
const puppeteer = require('puppeteer');

//importing consts from config.js
const config = require('./config.js');

/***********************************/

//start program
(async () => {

    //OS default browser launch
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    //setting window size
    await page.setViewport({width: config.window_size[0], height: config.window_size[1]});
    await page.goto(web_page);
    await delay(60000);
    try{
        //hiding blinking clicking button
        await page.mouse.click(config.button_hide_blinking[0], config.button_hide_blinking[1]);
        await delay(5000);
        
        //hiding text clicking button
        await page.mouse.click(config.button_hide_text[0], config.button_hide_text[1]);
        await delay(5000);
    }
    catch(exception){
        console.log("No button to click");
    }
    //filtering and saving images
    try{
        for (let x = config.coords.x_right[0]; x < config.coords.x_rightx_left[1]; x += config.x_delta){
            for (let y = config.coords.y_high[0]; y < config.coords.y_low[1]; y += config.y_delta){
                await delay(2000);
                await page.mouse.move(x, y);
                
                //normalization of perc
                let hor_perc = ((x-config.coords.x_right[0])/(config.coords.x_left[1]-config.coords.x_right[0])).toFixed(2);
                let ver_perc = ((y-config.coords.y_high[0])/(config.coords.y_low[1]-config.coords.y_high[0])).toFixed(2);
                
                // high right
                if( (x >= config.coords.x_right[0] && x <= config.coords.x_right[1]) && (y >= config.coords.y_high[0] && y <= config.coords.y_high[1]) )
                    await page.screenshot({ path: `${config.save_path}/${config.classes[0]}/${hor_perc}_${ver_perc}.png`});
                // high center
                else if((x >= config.coords.x_center[0] && x <= config.coords.x_center[1]) && (y >= config.coords.y_high[0] && y <= config.coords.y_high[1]) )
                    await page.screenshot({ path: `${config.save_path}/${config.classes[1]}/${hor_perc}_${ver_perc}.png`});
                // high left 
                else if( (x >= config.coords.x_left[0] && x <= config.coords.x_left[1]) && (y >= config.coords.y_high[0] && y <= config.coords.y_high[1]) )
                    await page.screenshot({ path: `${config.save_path}/${config.classes[2]}/${hor_perc}_${ver_perc}.png`});
                // middle right 
                else if( (x >= config.coords.x_right[0] && x <= config.coords.x_right[1]) && (y >= config.coords.y_middle[0] && y <= config.coords.y_middle[1]) )
                    await page.screenshot({ path: `${config.save_path}/${config.classes[3]}/${hor_perc}_${ver_perc}.png`});
                // middle center 
                else if( (x >= config.coords.x_center[0] && x <= config.coords.x_center[1]) && (y > config.coords.y_middle[0] && y <= config.coords.y_middle[1]) )
                    await page.screenshot({ path: `${config.save_path}/${config.classes[4]}/${hor_perc}_${ver_perc}.png`});
                // middle left 
                else if( (x >= config.coords.x_left[0] && x <= config.coords.x_left[1]) && (y >= config.coords.y_middle[0] && y <= config.coords.y_middle[1]) )
                    await page.screenshot({ path: `${config.save_path}/${config.classes[5]}/${hor_perc}_${ver_perc}.png`});
                // low right 
                else if( (x >= config.coords.x_right[0] && x <= config.coords.x_right[1]) && (y >= config.coords.y_low[0] && y <= config.coords.y_low[1]) )
                    await page.screenshot({ path: `${config.save_path}/${config.classes[6]}/${hor_perc}_${ver_perc}.png`});
                // low center 
                else if( (x >= config.coords.x_center[0] && x <= config.coords.x_center[1]) && (y >= config.coords.y_low[0] && y <= config.coords.y_low[1]) )
                    await page.screenshot({ path: `${config.save_path}/${config.classes[7]}/${hor_perc}_${ver_perc}.png`});
                // low left 
                else if( (x >= config.coords.x_left[0] && x <= config.coords.x_left[1]) && (y >= config.coords.y_low[0] && y <= config.coords.y_low[1]) )
                    await page.screenshot({ path: `${config.save_path}/${config.classes[8]}/${hor_perc}_${ver_perc}.png`});
                else
                    console.log(`!!! Warning: position (${x},${y}) not filtered !!!`);
            }
        }
    }
    catch(exception){
        console.log("Error(s) with class!");
    }
    await browser.close();
    })();
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));