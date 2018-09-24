import uuid
import secrets
import sys
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
import tornado.process
from tornado import template
import sqlite3
import math
from passlib.hash import pbkdf2_sha256
from expiringdict import ExpiringDict

SESSIONCONNECTION = "session.db"

if 'cache' not in globals():
	print("Creating in memory cache...")
	globals()["CACHE"] = ExpiringDict(max_len=100, max_age_seconds=86400)

FORM_TEMPLATE_STR = """
<!DOCTYPE html>
<html>
	<head>
			<meta charset="UTF-8">
			<meta name="viewport" content="width=device-width">
			<title>{{ title }}</title>
			<style>
				* {
					font-family: Consolas, Courier, Lucida Console, monospace;
					color: #fefefe;
				}
				* {
					margin: 0;
					padding: 0;
					text-rendering: optimizeLegibility;
				}
				@media (min-resolution: 2dppx) {
					* {
						text-rendering: geometricPrecision;
					}
				}

				body {
					width: 100%;
					height: 100%;
					padding: 0;
					margin: 0;
					font-size: 16px;
					background: #000;
					overflow: hidden;
				}
				#main_form {
					width: {{ width }}ch;
					height: {{ height }}rem;
					padding: 0;
					padding-bottom: 2px;
					position: relative;
					margin: 0 auto 0;
					border: 1px solid #000;
					overflow: hidden;
				}
				.unit {
					position: absolute;
					text-overflow: ellipsis;
					word-wrap: break-word;
					overflow: hidden;
					white-space: nowrap;
				}

				.spacer {
					position: absolute;
				}
				.spacer > * {
					padding-top:2px;
				}

				#submit_button {
					position: inherit;
					display: block;
					visibility: hidden;
					position: fixed;
					bottom: 20px;
					right: 0px;
					color: #000;
					padding: 10px;
					vertical-align: center;
				}
				input[type="text"], [type="password"] {
					caret-color: #fff;
					padding: 0;
					margin: 0;
					border: 0;
					outline: 0;
					font-size: 1rem;
					background: none;
					box-sizing: border-box;
					background-clip: border-box;
					/*padding-bottom: 2px;*/
					text-decoration: none;
					z-index: 99;
					border-bottom: 2px solid;
					/*position: relative;
					bottom: -3px;
					height: 1rem;*/
				}
				/* set on the component via after, this is a default */
				input[type="text"]:focus {
					background: #444;
				}
				input[type="password"]:focus {
					background: #444;
				}
			</style>
	<script>
/* MIT https://github.com/kenwheeler/cash */
(function(){
'use strict';var e=document,g=window,h=Array.prototype,l=h.filter,m=h.indexOf,aa=h.map,p=h.push,q=h.reverse,r=h.slice,ba=/^#[\w-]*$/,ca=/^\.[\w-]*$/,da=/<.+>/,ea=/^\w+$/;function t(a,b){void 0===b&&(b=e);return ca.test(a)?b.getElementsByClassName(a.slice(1)):ea.test(a)?b.getElementsByTagName(a):b.querySelectorAll(a)}
function u(a,b){if(a){if(a.__cash)return a;var c=a;if(v(a)){if(c=ba.test(a)?e.getElementById(a.slice(1)):da.test(a)?w(a):t(a,b),!c)return}else if(x(a))return this.ready(a);if(c.nodeType||c===g)c=[c];this.length=c.length;a=0;for(b=this.length;a<b;a++)this[a]=c[a]}}function y(a,b){return new u(a,b)}var z=y.fn=y.prototype=u.prototype={constructor:y,__cash:!0,length:0};z.get=function(a){return void 0===a?r.call(this):this[0>a?a+this.length:a]};z.eq=function(a){return y(this.get(a))};z.first=function(){return this.eq(0)};
z.last=function(){return this.eq(-1)};z.map=function(a){return y(aa.call(this,function(b,c){return a.call(b,c,b)}))};z.slice=function(){return y(r.apply(this,arguments))};var fa=/(?:^\w|[A-Z]|\b\w)/g,ha=/[\s-_]+/g;function A(a){return a.replace(fa,function(a,c){return a[c?"toUpperCase":"toLowerCase"]()}).replace(ha,"")}y.camelCase=A;function B(a,b){for(var c=0,d=a.length;c<d&&!1!==b.call(a[c],a[c],c,a);c++);}y.each=B;z.each=function(a){B(this,function(b,c){return a.call(b,c,b)});return this};
z.removeProp=function(a){return this.each(function(b,c){delete c[a]})};g.cash=g.$=y;y.extend=z.extend=function(a){void 0===a&&(a=this);for(var b=arguments,c=b.length,d=2>c?0:1;d<c;d++)for(var f in b[d])a[f]=b[d][f];return a};var C=1;y.guid=C;function D(a,b){var c=a&&(a.matches||a.webkitMatchesSelector||a.mozMatchesSelector||a.msMatchesSelector||a.oMatchesSelector);return!!c&&c.call(a,b)}y.matches=D;function x(a){return"function"===typeof a}y.isFunction=x;function v(a){return"string"===typeof a}
y.isString=v;function E(a){return!isNaN(parseFloat(a))&&isFinite(a)}y.isNumeric=E;var F=Array.isArray;y.isArray=F;z.prop=function(a,b){if(a){if(v(a))return 2>arguments.length?this[0]&&this[0][a]:this.each(function(c,f){f[a]=b});for(var c in a)this.prop(c,a[c]);return this}};function H(a){return v(a)?function(b,c){return D(c,a)}:a.__cash?function(b,c){return a.is(c)}:function(a,c,d){return c===d}}
z.filter=function(a){if(!a)return y();var b=x(a)?a:H(a);return y(l.call(this,function(c,d){return b.call(c,d,c,a)}))};var ia=/\S+/g;function I(a){return v(a)?a.match(ia)||[]:[]}z.hasClass=function(a){var b=I(a),c=!1;b.length&&this.each(function(a,f){c=f.classList.contains(b[0]);return!c});return c};z.removeAttr=function(a){var b=I(a);return b.length?this.each(function(a,d){B(b,function(a){d.removeAttribute(a)})}):this};
z.attr=function(a,b){if(a){if(v(a)){if(2>arguments.length){if(!this[0])return;var c=this[0].getAttribute(a);return null===c?void 0:c}return null===b?this.removeAttr(a):this.each(function(c,f){f.setAttribute(a,b)})}for(c in a)this.attr(c,a[c]);return this}};z.toggleClass=function(a,b){var c=I(a),d=void 0!==b;return c.length?this.each(function(a,k){B(c,function(a){d?b?k.classList.add(a):k.classList.remove(a):k.classList.toggle(a)})}):this};z.addClass=function(a){return this.toggleClass(a,!0)};
z.removeClass=function(a){return arguments.length?this.toggleClass(a,!1):this.attr("class","")};var J;function w(a){if(!J){J=e.implementation.createHTMLDocument("");var b=J.createElement("base");b.href=e.location.href;J.head.appendChild(b)}v(a)||(a="");J.body.innerHTML=a;return r.call(J.body.childNodes)}y.parseHTML=w;function K(a){return a.filter(function(a,c,d){return d.indexOf(a)===c})}y.unique=K;z.add=function(a,b){return y(K(this.get().concat(y(a,b).get())))};
function L(a,b,c){if(1===a.nodeType)return a=g.getComputedStyle(a,null),b?c?a.getPropertyValue(b):a[b]:a}function M(a,b){return parseInt(L(a,b),10)||0}var N=/^--/,O={},ja=e.createElement("div").style,ka=["webkit","moz","ms","o"];function P(a,b){void 0===b&&(b=N.test(a));if(b)return a;if(!O[a]){b=A(a);var c=""+b.charAt(0).toUpperCase()+b.slice(1);b=(b+" "+ka.join(c+" ")+c).split(" ");B(b,function(b){if(b in ja)return O[a]=b,!1})}return O[a]}y.prefixedProp=P;
var la={animationIterationCount:!0,columnCount:!0,flexGrow:!0,flexShrink:!0,fontWeight:!0,lineHeight:!0,opacity:!0,order:!0,orphans:!0,widows:!0,zIndex:!0};function Q(a,b,c){void 0===c&&(c=N.test(a));return c||la[a]||!E(b)?b:b+"px"}z.css=function(a,b){if(v(a)){var c=N.test(a);a=P(a,c);if(2>arguments.length)return this[0]&&L(this[0],a,c);if(!a)return this;b=Q(a,b,c);return this.each(function(d,k){1===k.nodeType&&(c?k.style.setProperty(a,b):k.style[a]=b)})}for(var d in a)this.css(d,a[d]);return this};
var ma=/^data-(.*)/;y.hasData=function(a){return"__cashData"in a};function R(a){return a.__cashData=a.__cashData||{}}function S(a,b){var c=R(a);if(b){if(!(b in c)&&(a=a.dataset?a.dataset[b]||a.dataset[A(b)]:y(a).attr("data-"+b),void 0!==a)){try{a=JSON.parse(a)}catch(d){}c[b]=a}return c[b]}return c}
z.data=function(a,b){var c=this;if(!a){if(!this[0])return;B(this[0].attributes,function(a){(a=a.name.match(ma))&&c.data(a[1])});return S(this[0])}if(v(a))return void 0===b?this[0]&&S(this[0],a):this.each(function(c,d){R(d)[a]=b});for(var d in a)this.data(d,a[d]);return this};z.removeData=function(a){return this.each(function(b,c){void 0===a?delete c.__cashData:delete R(c)[a]})};
function T(a,b){return M(a,"border"+(b?"Left":"Top")+"Width")+M(a,"padding"+(b?"Left":"Top"))+M(a,"padding"+(b?"Right":"Bottom"))+M(a,"border"+(b?"Right":"Bottom")+"Width")}B(["Width","Height"],function(a){z["inner"+a]=function(){return this[0]&&this[0]["client"+a]}});
B(["width","height"],function(a,b){z[a]=function(c){if(!this[0])return void 0===c?void 0:this;if(!arguments.length)return this[0].getBoundingClientRect()[a]-T(this[0],!b);c=parseInt(c,10);return this.each(function(d,f){1===f.nodeType&&(d=L(f,"boxSizing"),f.style[a]=Q(a,c+("border-box"===d?T(f,!b):0)))})}});B(["Width","Height"],function(a,b){z["outer"+a]=function(c){if(this[0])return this[0]["offset"+a]+(c?M(this[0],"margin"+(b?"Top":"Left"))+M(this[0],"margin"+(b?"Bottom":"Right")):0)}});
function U(a,b){for(var c=0,d=b.length;c<d;c++)if(0>a.indexOf(b[c]))return!1;return!0}function na(a,b,c){B(a[c],function(a){b.removeEventListener(c,a[1])});delete a[c]}function oa(a,b,c,d){d.guid=d.guid||C++;var f=a.__cashEvents=a.__cashEvents||{};f[b]=f[b]||[];f[b].push([c,d]);a.addEventListener(b,d)}function V(a){a=a.split(".");return[a[0],a.slice(1).sort()]}
function W(a,b,c,d){var f=a.__cashEvents=a.__cashEvents||{};if(b){var k=f[b];k&&(d&&(d.guid=d.guid||C++),f[b]=k.filter(function(f){var k=f[0];f=f[1];if(d&&f.guid!==d.guid||!U(k,c))return!0;a.removeEventListener(b,f)}))}else if(c&&c.length)for(b in f)W(a,b,c,d);else for(b in f)na(f,a,b)}z.off=function(a,b){var c=this;void 0===a?this.each(function(a,b){return W(b)}):B(I(a),function(a){a=V(a);var d=a[0],k=a[1];c.each(function(a,c){return W(c,d,k,b)})});return this};
z.on=function(a,b,c,d){var f=this;if(!v(a)){for(var k in a)this.on(k,b,a[k]);return this}x(b)&&(c=b,b=!1);B(I(a),function(a){a=V(a);var k=a[0],G=a[1];f.each(function(a,f){a=function pa(a){if(!a.namespace||U(G,a.namespace.split("."))){var n=f;if(b)for(n=a.target;!D(n,b);){if(n===f)return;n=n.parentNode;if(!n)return}a.namespace=a.namespace||"";n=c.call(n,a,a.data);d&&W(f,k,G,pa);!1===n&&(a.preventDefault(),a.stopPropagation())}};a.guid=c.guid=c.guid||C++;oa(f,k,G,a)})});return this};
z.one=function(a,b,c){return this.on(a,b,c,!0)};z.ready=function(a){function b(){return a(y)}"loading"!==e.readyState?setTimeout(b):e.addEventListener("DOMContentLoaded",b);return this};z.trigger=function(a,b){var c=a;if(v(a)){var d=V(a);a=d[0];d=d[1];c=e.createEvent("HTMLEvents");c.initEvent(a,!0,!0);c.namespace=d.join(".")}c.data=b;return this.each(function(a,b){b.dispatchEvent(c)})};
function qa(a){var b=[];B(a.options,function(a){!a.selected||a.disabled||a.parentNode.disabled||b.push(a.value)});return b}var ra=/select-one/i,sa=/select-multiple/i;function X(a){var b=a.type;return ra.test(b)?0>a.selectedIndex?null:a.options[a.selectedIndex].value:sa.test(b)?qa(a):a.value}var ta=/%20/g,ua=/file|reset|submit|button|image/i,va=/radio|checkbox/i;
z.serialize=function(){var a="";this.each(function(b,c){B(c.elements||[c],function(b){if(!b.disabled&&b.name&&"FIELDSET"!==b.tagName&&!ua.test(b.type)&&(!va.test(b.type)||b.checked)){var c=X(b);void 0!==c&&(c=F(c)?c:[c],B(c,function(c){var d=a;c="&"+encodeURIComponent(b.name)+"="+encodeURIComponent(c).replace(ta,"+");a=d+c}))}})});return a.substr(1)};z.val=function(a){return void 0===a?this[0]&&X(this[0]):this.each(function(b,c){c.value=a})};z.clone=function(){return this.map(function(a,b){return b.cloneNode(!0)})};
z.detach=function(){return this.each(function(a,b){b.parentNode&&b.parentNode.removeChild(b)})};function Y(a,b,c){var d=v(b);!d&&b.length?B(b,function(b){return Y(a,b,c)}):B(a,d?function(a){a.insertAdjacentHTML(c?"afterbegin":"beforeend",b)}:function(a,d){d=d?b.cloneNode(!0):b;c?a.insertBefore(d,a.childNodes[0]):a.appendChild(d)})}z.append=function(){var a=this;B(arguments,function(b){Y(a,b)});return this};z.appendTo=function(a){Y(y(a),this);return this};
z.html=function(a){if(void 0===a)return this[0]&&this[0].innerHTML;var b=a.nodeType?a[0].outerHTML:a;return this.each(function(a,d){d.innerHTML=b})};z.empty=function(){return this.html("")};z.insertAfter=function(a){var b=this;y(a).each(function(a,d){var c=d.parentNode;b.each(function(b,f){c.insertBefore(a?f.cloneNode(!0):f,d.nextSibling)})});return this};z.after=function(){var a=this;B(q.apply(arguments),function(b){q.apply(y(b).slice()).insertAfter(a)});return this};
z.insertBefore=function(a){var b=this;y(a).each(function(a,d){var c=d.parentNode;b.each(function(b,f){c.insertBefore(a?f.cloneNode(!0):f,d)})});return this};z.before=function(){var a=this;B(arguments,function(b){y(b).insertBefore(a)});return this};z.prepend=function(){var a=this;B(arguments,function(b){Y(a,b,!0)});return this};z.prependTo=function(a){Y(y(a),q.apply(this.slice()),!0);return this};z.remove=function(){return this.detach().off()};
z.replaceWith=function(a){var b=this;return this.each(function(c,d){if(c=d.parentNode){var f=y(a);if(!f[0])return b.remove(),!1;c.replaceChild(f[0],d);y(f[0]).after(f.slice(1))}})};z.replaceAll=function(a){y(a).replaceWith(this);return this};z.text=function(a){return void 0===a?this[0]?this[0].textContent:"":this.each(function(b,c){c.textContent=a})};var Z=e.documentElement;
z.offset=function(){var a=this[0];if(a)return a=a.getBoundingClientRect(),{top:a.top+g.pageYOffset-Z.clientTop,left:a.left+g.pageXOffset-Z.clientLeft}};z.offsetParent=function(){return y(this[0]&&this[0].offsetParent)};z.position=function(){var a=this[0];if(a)return{left:a.offsetLeft,top:a.offsetTop}};z.children=function(a){var b=[];this.each(function(a,d){p.apply(b,d.children)});b=y(K(b));return a?b.filter(function(b,d){return D(d,a)}):b};
z.find=function(a){for(var b=[],c=0,d=this.length;c<d;c++){var f=t(a,this[c]);f.length&&p.apply(b,f)}return y(b.length&&K(b))};z.has=function(a){var b=v(a)?function(b,d){return!!t(a,d).length}:function(b,d){return d.contains(a)};return this.filter(b)};z.is=function(a){if(!a||!this[0])return!1;var b=H(a),c=!1;this.each(function(d,f){c=b(d,f,a);return!c});return c};z.next=function(){return y(this[0]&&this[0].nextElementSibling)};
z.not=function(a){if(!a||!this[0])return this;var b=H(a);return this.filter(function(c,d){return!b(c,d,a)})};z.parent=function(){var a=[];this.each(function(b,c){c&&c.parentNode&&a.push(c.parentNode)});return y(K(a))};z.index=function(a){var b=a?y(a)[0]:this[0];a=a?this:y(b).parent().children();return m.call(a,b)};z.closest=function(a){return a&&this[0]?this.is(a)?this.filter(a):this.parent().closest(a):y()};
z.parents=function(a){var b=[],c;this.each(function(d,f){for(c=f;c&&c.parentNode&&c!==e.body.parentNode;)c=c.parentNode,(!a||a&&D(c,a))&&b.push(c)});return y(K(b))};z.prev=function(){return y(this[0]&&this[0].previousElementSibling)};z.siblings=function(){var a=this[0];return this.parent().children().filter(function(b,c){return c!==a})};
})();
	</script>
	</head>
	<body>
		<form id="main_form" method="post">
		{% autoescape None %}
		{% for field in fields %}
			{{ field.html() }}
		{% end %}
		<input type="hidden" id="submit_type" name="__submit_type" value="" />
		<input id="submit_button" type="submit" value="SUBMIT" />
		</form>
		<script>
window.mobileAndTabletcheck = function() {
	var check = false;
	(function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
	return check;
};

window.mobilecheck = function() {
	var check = false;
	(function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
	return check;
};

			if (window.mobilecheck()) {
				document.getElementById('submit_button').style.visibility = 'shown';
			}

			document.getElementById('main_form').action = window.location.href;
			
			if(document.addEventListener) {
				document.addEventListener("keypress", keyCapt, false);
			}

			function keyCapt(e){
				if(!e) {
					e=window.event;
				}
				if (e.keyCode === 114) {
					document.getElementById('submit_type').value = 'f3';
					e.preventDefault();
					document.getElementById('main_form').submit();
				}
				if (e.keyCode === 119) {
					document.getElementById('submit_type').value = 'f8';
					e.preventDefault();
					document.getElementById('main_form').submit();
				}
				if (e.keyCode === 120) {
					document.getElementById('submit_type').value = 'f9';
					e.preventDefault();
					document.getElementById('main_form').submit();
				}
			} 

			for (var i = 0; document.forms[0].elements[i].type == 'hidden'; i++);
			document.forms[0].elements[i].focus();
		</script>
		{% if is_scaled == True %}   
			<script>
			function fillDiv(div, proportional, cb) {
					console.log('filldiv', div);
					var currentWidth = div.outerWidth();
					var currentHeight = div.outerHeight();
					
					var availableHeight = window.innerHeight;
					var availableWidth = window.innerWidth;
					
					var scaleX = availableWidth / currentWidth;
					var scaleY = availableHeight / currentHeight;
					
					if (proportional) {
							scaleX = Math.min(scaleX, scaleY);
							scaleY = scaleX;
					}
					
					var translationX = Math.round((availableWidth - (currentWidth * scaleX)) / 2);
					var translationY = Math.round((availableHeight - (currentHeight * scaleY)) / 2);
					
					div.css({
							"position": "fixed",
							"left": "0",
							"top": "0",
							"transform": "translate(" + translationX + "px, "
									+ translationY + "px) scale3d("
									+ scaleX + ", " + scaleY + ", 1)",
							"transformOrigin": "0 0"
					});

					if (cb) {
						cb();
					}
			}
			function monitorScalingContent(elSel) {
					var div = $(elSel);
					fillDiv(div, true);
					window.onresize = function() {fillDiv(div, true);}
			}    
			
			window.onload = function() {monitorScalingContent("#main_form");}
			</script>
		{% end %}
	</body>
</html>
"""

FORM_TEMPLATE = template.Template(FORM_TEMPLATE_STR)

class Colors():
	RED = "#FF0000"
	TEAL = "#BCFEFD"
	GREEN = "#40F85A"
	PURPLE = "#7992F9"
	NORMAL = "#FEFEFE"
	YELLOW = "#FFFF00"
	BLUE = "#0000FD"

class SubmitTypes():
	F9 = "f9"
	F8 = "f8"
	F3 = "f3"
	NORMAL = None

class TextMultiLine():
	def __init__(self, text, color = "initial"):
		self.text = text.replace(" ", "&nbsp;").replace("\n", "<br />").strip()
		self.color = color

	def __str__(self):
		return "<p style=\"color: " + str(self.color) + ";\">" + str(self.text) + "</p>"

class TextColor():
	def __init__(self, text, color = "initial"):
		self.text = text.replace(" ", "&nbsp;")
		self.color = color

	def __str__(self):
		return "<span style=\"color: " + str(self.color) + ";\">" + str(self.text) + "</span>"

class TextBold():
	def __init__(self, text):
		self.text = text.replace(" ", "&nbsp;")

	def __str__(self):
		return "<b>" + str(self.text) + "</b>"

class Component():
	def __init__(self, name = None, x = 0, y = 0):
		self.x = x
		self.y = y
		self.name = name
		if name is None:
			self.name = "gen_" + str(uuid.uuid4())

	def compose(self, inner):
		return "<div class=\"unit\" style=\"" + "top:" + str(self.x) + "rem;left:" + str(self.y) + "ch;\">" + \
		inner + \
		"</div>"		
		# "<div class=\"spacer\">" + \

	def html(self):
		return self.compose("&nbsp;")

class TextBar(Component):
	def __init__(self, text, width, name = None, x = 0, y = 0):
		Component.__init__(self, name = name, x = x, y = y)
		self.text = text
		self.width = width

	def html(self):
		left_off = math.floor(len(self.text) / 2) + 1
		right_off = math.ceil(len(self.text) / 2) + 1

		padding_size = int(round((self.width / 2)))
		padding_rem = int(round(self.width % 2))

		contents = "|" + ("-" * (padding_size - left_off))
		contents = contents + self.text
		contents = contents + ("-" * ((padding_size + padding_rem) - right_off)) + "|"
		return self.compose(contents)

class Text(Component):
	def __init__(self, text, name = None, x = 0, y = 0):
		Component.__init__(self, name = name, x = x, y = y)
		self._text = str(text)

	def get_text(self):
		return str(self._text)

	def set_text(self, val):
		self._text = str(val)

	text = property(get_text, set_text)

	def html(self):
		return self.compose("<span>" + self._text + "</span>")

class TextField(Component):
	def __init__(self, label, color=None, value="", field_length=10, placeholder="", is_password=False, name = None, x = 0, y = 0):
		Component.__init__(self, name = name, x = x, y = y)
		if label is None:
			self.label = "&nbsp;"
		else:
			self.label = str(label)
		self.field_length = field_length
		self.placeholder = placeholder
		self._value = str(value)
		if color is None:
			self.color = Colors().NORMAL
		else:
			self.color = color
		if is_password == False:
			self.type = "text"
		else:
			self.type = "password"

	def clear(self):
		self._value = ""
	
	def get_value(self):
		if self._value is None:
			return ""
		else:
			return self._value.strip()

	def set_value(self, val):
		self._value = str(val).strip()

	value = property(get_value, set_value)

	def html(self):
		# <span class=\"input-underline\" style=\"width:" + str(self.field_length) + "ch;background:" + str(self.color) + ";\"></span>"
		return self.compose(
		"<label for=\"" + self.name + "\">" + self.label + "</label>" \
		"<input style=\"color:" + str(self.color) + ";\" placeholder=\"" + self.placeholder + "\" size=\"" + str(self.field_length) + "\" name=\"" + self.name + "\" " \
		"type=\"" + self.type + "\" value=\"" + self._value + "\" maxlength=\"" + str(self.field_length) + "\" autocomplete=\"off\"></input>"
		)

class PasswordField(TextField):
	def __init__(self, label, value="", field_length=10, placeholder="", name = None, x = 0, y = 0):
		TextField.__init__(self, label, value = value, field_length = field_length, placeholder = placeholder, is_password = True, name = name, x = x, y = y)

class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
	def set_extra_headers(self, path):
		# Disable cache
		self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

class Form():
	def __init__(self):
		self.title = ""
		self.fields = []
		self.width = 80
		self.height = 32
		self.is_scaled = True
		self.request = None
		self.session = None

	def persist_field_values(self):
		for key, value in self.request.arguments.items():
			for x in self.fields:
				if x.name.startswith("__"):
					pass
				if x.name == key:
					try:
						x.value = (value[0].decode("utf-8"))
					except:
						pass

	def clear_field_values(self):		
		for key, value in self.request.arguments.items():
			for x in self.fields:
				if x.name == key:
					try:
						x.clear()
					except:
						pass

	def __getitem__(self, key):
		for x in self.fields:
			if x.name == key:
				try:
					return x
				except:
					pass
		return None

	def get_field_value(self, name):
		for key, value in self.request.arguments.items():
			for x in self.fields:
				if x.name == key and key == name:
					return value[0].decode("utf-8")

	def get_submit_type(self):
		for key, value in self.request.arguments.items():
			if key == "__submit_type":
				return value[0].decode("utf-8")
		return None

	# subclasses need to override this
	def on_submit(self):
		pass

class FormsServerHandler(tornado.web.RequestHandler):
	def initialize(self, forms_path):
		form_name = self.request.path.split("/")[-1]
		if form_name == "":
			form_name = "Index"
		try:
			exec(open("./" + forms_path + "/" + form_name + "Form.py").read(), globals())
		except:
			form_name = "Error"
			exec(open("./" + forms_path + "/" + form_name + "Form.py").read(), globals())
		self.form = globals()[form_name + "Form"]()
		self.form.fields = []
		self.form.title = "NO TITLE"
		self.form.request = self.request
		self.form.is_scaled = True
		self.form.width = 80
		self.form.height = 32
		self.form.session = Session(self)

	def prepare(self):
		# https://stackoverflow.com/questions/29794641/tornado-redirect-to-a-different-domain
		self._init_ret = self.form.init()
		if self._init_ret is not None:
			self.redirect(str(self._init_ret))		

	def get(self):
		invert_op = getattr(self.form, "setup", None)
		if callable(invert_op):
			ret = self.form.setup()
		invert_op = getattr(self.form, "on_get", None)
		if callable(invert_op):
			ret = self.form.on_get()
		self.write(FORM_TEMPLATE.generate(
			title=self.form.title, 
			is_scaled=self.form.is_scaled, 
			fields=self.form.fields,
			width=self.form.width,
			height=self.form.height))

	def post(self):
		invert_op = getattr(self.form, "setup", None)
		if callable(invert_op):
			ret = self.form.setup()		
		invert_op = getattr(self.form, "on_post", None)
		if callable(invert_op):
			ret = self.form.on_post()	
		invert_op = getattr(self.form, "on_submit", None)
		ret = None
		if callable(invert_op):
			ret = self.form.on_submit()
		if ret is None:
			self.postback()
		else:
			self.navigate_to_form(str(ret))

	def postback(self):
		self.write(FORM_TEMPLATE.generate(
			title=self.form.title, 
			is_scaled=self.form.is_scaled, 
			fields=self.form.fields,
			width=self.form.width,
			height=self.form.height))

	def navigate_to_form(self, name):
		self.redirect(name)

class SessionCacheKeyValue():
	def __init__(self, session_id):
		self.session_id = session_id

	def __getitem__(self, key):
		conn = sqlite3.connect(SESSIONCONNECTION)
		c = conn.cursor()
		c.execute('SELECT value FROM kv WHERE sessionid = ? and key = ?', (self.session_id, key,))
		item = c.fetchone()
		conn.close()
		if item is None:
			return None
		return item[0]

	def __setitem__(self, key, value):
		conn = sqlite3.connect(SESSIONCONNECTION)
		c = conn.cursor()
		c.execute('REPLACE INTO kv (sessionid, key, value) VALUES (?,?,?)', (self.session_id, key, value))
		conn.commit()
		conn.close()

class SessionCache():
	def __init__(self):
		conn = sqlite3.connect(SESSIONCONNECTION)
		c = conn.cursor()
		c.execute("CREATE TABLE IF NOT EXISTS kv (sessionid text, key text, value text, UNIQUE(sessionid, key))")
		conn.commit()
		conn.close()

	def __getitem__(self, session_id):
		return SessionCacheKeyValue(session_id)

	def __delitem__(self, session_id):
		if key not in self:
			raise KeyError(key)
		conn = sqlite3.connect(SESSIONCONNECTION)
		c = self.conn.cursor()
		c.execute('DELETE FROM kv WHERE sessionid = ?', (session_id,))
		conn.commit()
		conn.close()

class Session():
	def __init__(self, handler):
		self.handler = handler
		self.session_id = None
		self.session_cache = SessionCache()
		self.session_cookie_name = "FromServerSession"

	def _get_session_id(self):
		if self.session_id is None:
			cookie = self.handler.get_secure_cookie(self.session_cookie_name)
			if cookie is None:
				self.session_id = None
			else:
				self.session_id = cookie.decode("utf-8")

	def create(self):
		self.session_id = str(secrets.token_urlsafe(64))
		self.handler.set_secure_cookie(self.session_cookie_name, self.session_id)
		# no need to create if never used?
		self.session_cache[self.session_id]["_created"] = True 

	def remove(self):
		self._get_session_id()
		if self.session_id is None:
			pass
		else:
			try:
				del self.session_cache[self.session_id]
			except:
				pass
			self.handler.clear_cookie(self.session_cookie_name)

	def is_valid(self):
		id = ""
		self._get_session_id()
		if self.session_id is None:
			return False
		else:
			try:
				id = self.session_cache[self.session_id]
			except:
				return False
		return True

	def __getitem__(self, key):
		self._get_session_id()
		if self.session_id is None:
			return None
		else:
			if self.session_cache[self.session_id] is None:
				return None
			return self.session_cache[self.session_id][key]

	def __setitem__(self, key, value):
		self._get_session_id()
		if self.session_id is None:
			self.create() # will assign self.session_id a value
		self.session_cache[self.session_id][key] = value

# just as a shorthand to wrap tornado
class TornadoServer():
	def __init__(self, handlers, cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__", port=8090, autoreload=False):
		self.handlers = handlers
		self.autoreload = autoreload
		self.handlers.append((r"/static/(.*)", NoCacheStaticFileHandler, {"path": "static"}))
		self.cookie_secret = cookie_secret
		self.port = port

		self.app = tornado.web.Application(
			self.handlers, autoreload=self.autoreload,
			cookie_secret=self.cookie_secret)

	def start(self):
		self.app.listen(self.port)
		tornado.ioloop.IOLoop.instance().start()

class DB():
	def __init__(self, dbname):
		self.filename = dbname + ".db"
		conn = sqlite3.connect(self.filename)
		conn.commit()
		conn.close()

	def execute(self, cmd, params = None):
		conn = sqlite3.connect(self.filename)
		c = conn.cursor()
		if params is None:
			c.execute(cmd)
		else:
			c.execute(cmd, params)
		conn.commit()
		conn.close()

	def select_one(self, cmd, params = None):
		conn = sqlite3.connect(self.filename)
		c = conn.cursor()
		if params is None:
			c.execute(cmd)
		else:
			c.execute(cmd, params)
		items = c.fetchone()
		conn.commit()
		conn.close()
		return items

	def select(self, cmd, params = None):
		conn = sqlite3.connect(self.filename)
		c = conn.cursor()
		if params is None:
			c.execute(cmd)
		else:
			c.execute(cmd, params)
		items = c.fetchall()
		conn.commit()
		conn.close()
		return items

class Users():
	def __init__(self, max_attempts = 4):
		self.users_db = DB("users")
		self.max_attempts = max_attempts
		self.users_db.execute("""
			CREATE TABLE IF NOT EXISTS users (
				name text,
				hash text,
				attempts integer
			)
		""")

	def assert_default_admin_user(self, password="password"):
		user = self.users_db.select("select name from users where name = ?", ("admin",))
		if len(user) == 0:
			hashed = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
			self.users_db.execute("insert into users (name, hash, attempts) values (?, ?, 0)", ("admin", hashed,))

	def change_user_password(self, username, password):
		hashed = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
		self.users_db.execute("update users set hash = ? where name = ?", (hashed, username,))		

	def check_password(self, username, password):
		matching_users = self.users_db.select_one(
			"select name, hash, attempts from users where name = ?", 
			(username,))
		if matching_users is None:
			return False
		else:
			if matching_users[2] > self.max_attempts:
				return False

			res = pbkdf2_sha256.verify(password, matching_users[1])
			if res == False:
				self.users_db.execute("update users set attempts = attempts + 1 where name = ?", (username,))
			else:
				self.users_db.execute("update users set attempts = 0 where name = ?", (username,))
			return res

USERS = Users()