!function(){var a=Handlebars.template;(Handlebars.templates=Handlebars.templates||{}).stage=a({1:function(a,n,l,e,r){return"win-bg"},3:function(a,n,l,e,r){return"lose-bg"},5:function(a,n,l,e,r){return'            <i class="fa fa-check" aria-hidden="true"></i>\n'},7:function(a,n,l,e,r){return'            <i class="fa fa-times" aria-hidden="true"></i>\n'},9:function(a,n,l,e,r){a.propertyIsEnumerable;var i=a.lambda,t=a.escapeExpression;return'        <div class="champion">\n            <img src="images/champions/'+t(i(null!=n?n.name:n,n))+'.png" />\n            <h4>'+t(i(null!=n?n.name:n,n))+" | Level: "+t(i(null!=n?n.level:n,n))+"</h4>\n            <p>Damage: "+t(i(null!=n?n.damage:n,n))+"</p>\n        </div>\n"},compiler:[8,">= 4.3.0"],main:function(a,n,l,e,r){a.propertyIsEnumerable;var i,t=null!=n?n:a.nullContext||{},s=a.lambda,u=a.escapeExpression;return'\n<div class="stage_box '+(null!=(i=l.if.call(t,null!=(i=null!=n?n.data:n)?i.win:i,{name:"if",hash:{},fn:a.program(1,r,0),inverse:a.program(3,r,0),data:r}))?i:"")+'">\n    <div class="header">\n        <div class="left">\n            <h2>Lvl'+u(s(null!=(i=null!=n?n.data:n)?i.stage:i,n))+'</h2>\n        </div>\n        <div class="result">\n'+(null!=(i=l.if.call(t,null!=(i=null!=n?n.data:n)?i.win:i,{name:"if",hash:{},fn:a.program(5,r,0),inverse:a.program(7,r,0),data:r}))?i:"")+"        </div>\n    </div>\n"+(null!=(i=l.each.call(t,null!=(i=null!=n?n.data:n)?i.champions:i,{name:"each",hash:{},fn:a.program(9,r,0),inverse:a.noop,data:r}))?i:"")+'    <div class="healthbar" style="width: '+u(s(null!=(i=null!=n?n.data:n)?i.health:i,n))+"%; background-color: "+u(s(null!=(i=null!=n?n.data:n)?i.health_color:i,n))+';">\n      '+u(s(null!=(i=null!=n?n.data:n)?i.health:i,n))+"\n    </div>\n</div>"},useData:!0})}();