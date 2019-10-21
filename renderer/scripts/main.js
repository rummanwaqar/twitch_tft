var main = document.getElementById("container");

for(i=0; i<data['game_data'].length; i++) {
    var stage_data = data['game_data'][i];
    main.innerHTML += Handlebars.templates.stage({data: stage_data});
}