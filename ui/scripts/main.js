function mapColor(colors, values, x) {
    m = (colors[1] - colors[0])/(values[1] - values[0]);
    return m * (x - values[1]) + colors[1];
}

function getColorFromHealth(health) {
    /*
     * Keypoints for colors
     * 100%: #A3FF2E
     * 50%: #FFFF2E
     * 0%: #FF332E
     */
    var r = 0;
    var g = 0;
    var b = 46;

    if(health >= 50) {
        g = 255;
        r = mapColor([255, 163], [50, 100], health)
    } else {
        r = 255;
        g = mapColor([255, 51], [50, 0], health);
    }

    return "rgb(" + r + "," + g + "," + b + ")";
}

var main = document.getElementById("container");

for(i=0; i<data['game_data'].length; i++) {
    var stage_data = data['game_data'][i];
    stage_data.health_color = getColorFromHealth(stage_data.health);

    main.innerHTML += Handlebars.templates.stage({data: stage_data});

    // add three empty boxes because Level 1 has 3 stages instead of 6
    if (stage_data.stage === '1-3' && data['game_data'].length > 3) {
        main.innerHTML += '<div></div>';
        main.innerHTML += '<div></div>';
        main.innerHTML += '<div></div>';
    }
}