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

function getChampionSize(i, champs, size_limits) {
    /*
     * i: index of champion in array
     * champs: champion array
     * size_limits: [min size, max size] 
     */
    if(champs.length == 1) {
        return size_limits[1];
    }

    // champs are sorted by health is descending order
    health_limits = [champs[champs.length - 1].damage, champs[0].damage];

    return (size_limits[1] - size_limits[0]) / (health_limits[1] - health_limits[0]) * 
        (champs[i].damage - health_limits[1]) + size_limits[1];
}

var border_colors = ["#A77044", "#D7D7D7", "#FFD700"];
var image_base_url = "../images/champions/";
var size_limits = [40, 90];

var main = document.getElementById("container");

for(i=0; i<data['game_data'].length; i++) {
    var stage_data = data['game_data'][i];
    stage_data.health_color = getColorFromHealth(stage_data.health);

    for(var j=0; j < stage_data.champions.length; j++) {
        var champion_data = stage_data.champions[j];

        // generate custom styles
        var border_color = border_colors[champion_data.level - 1];
        var size = getChampionSize(j, stage_data.champions, size_limits);
        var border_size = 5;
        var image_url =  image_base_url + champion_data.name + ".png";

        champion_data.styles = "--size: " + size + "px; --border-size: " + border_size + "px; " + 
            "--border-color: " + border_color + "; " +
            "--background: url('" + image_url + "');";
    }

    main.innerHTML += Handlebars.templates.stage({data: stage_data});  

    // add three empty boxes because Level 1 has 3 stages instead of 6
    if (stage_data.stage === '1-3' && data['game_data'].length > 3) {
        main.innerHTML += '<div></div>';
        main.innerHTML += '<div></div>';
        main.innerHTML += '<div></div>';
    }
}