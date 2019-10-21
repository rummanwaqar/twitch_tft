var main = document.getElementById("container");

for(i=0; i<data['game_data'].length; i++) {
    var stage_data = data['game_data'][i];
    main.innerHTML += Handlebars.templates.stage({data: stage_data});

    // add three empty boxes because Level 1 has 3 stages instead of 6
    if (stage_data.stage === '1-3' && data['game_data'].length > 3) {
        main.innerHTML += '<div></div>';
        main.innerHTML += '<div></div>';
        main.innerHTML += '<div></div>';
    }
}