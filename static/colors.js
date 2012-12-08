var CurrentColor = new Array();
function hsv2rgb (h, s, v){h /= 360;s /= 100;v /= 100;var m2 = v <= 0.5 ? v * (s + 1) : v + s - v * s;var m1 = v * 2 - m2;var r = norm2hex (hue2rgb (m1, m2, h + 1/3));var g = norm2hex (hue2rgb (m1, m2, h));var b = norm2hex (hue2rgb (m1, m2, h - 1/3));return r + '' + g + '' + b;}
function norm2hex (value){return dec2hex (Math.floor (255 * value));}
function hue2rgb (m1, m2, h) {if (h < 0) h = h + 1;if (h > 1) h = h - 1;if (h * 6 < 1) return m1 + (m2 - m1) * h * 6;if (h * 2 < 1) return m2;if (h * 3 < 2) return m1 + (m2 - m1) * (2/3 - h) * 6;return m1;}
function dec2hex (dec) {var hexChars = "0123456789ABCDEF";var a = dec % 16;var b = (dec - a) / 16;hex = '' + hexChars.charAt (b) + hexChars.charAt (a);return hex;}
function AlterColor() {	CurrentColor.h = Math.floor (360 * Math.random());CurrentColor.s = 30 + Math.floor (70 * Math.random());CurrentColor.v = 30 + Math.floor (50 * Math.random());SetLogoColor (CurrentColor.h, CurrentColor.s, CurrentColor.v);}
function SetLogoColor (h, s, v) {var logodiv = document.getElementById ('hover-color');if (logodiv) logodiv.style.color = '#' + hsv2rgb (h, s, v);}
