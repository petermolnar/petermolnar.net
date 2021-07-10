var DEFAULT_THEME = 'dark';
var ALT_THEME = 'light';
var STORAGE_KEY = 'theme';
var colorscheme = [];

function indicateTheme(mode) {
    for(var i = colorscheme.length; i--; ) {
        if(colorscheme[i].value == mode) {
            colorscheme[i].checked = true;
        }
    }
}

function applyTheme(mode) {
    var st = document.getElementById('css_' + ALT_THEME);
    if (mode == ALT_THEME) {
        st.setAttribute('media', 'all');
    }
    else {
        st.setAttribute('media', 'not all');
    }
}

function setTheme(e) {
    var mode = e.target.value;
    if (mode != DEFAULT_THEME) {
        document.cookie = STORAGE_KEY+'='+mode+'; path=/; SameSite=Strict;';
    }
    else {
        document.cookie = STORAGE_KEY+'='+mode+'; path=/; SameSite=Strict; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    }
    applyTheme(mode);
    indicateTheme(mode);
}

function getCurrentTheme() {
    var cookies = "; " + document.cookie;
    var is_theme_set = cookies.split("; "+STORAGE_KEY+"=");
    if (is_theme_set.length == 2) {
        return is_theme_set.pop().split(";").shift();
    }
    else {
        return DEFAULT_THEME;
    }
}

function setupTheme() {
    var themeform = document.createElement('form');
    themeform.id = "theme";
    document.getElementById("header-forms").insertBefore(themeform, document.getElementById("search"));
    var schemes = ["dark", "light"];
    for (var i = 0; i < schemes.length; i++) {
        var input = document.createElement('input');
        input.name = 'colorscheme';
        input.type = 'radio';
        input.id = schemes[i] + input.name;
        input.value = schemes[i];
        themeform.appendChild(input);

        var label = document.createElement('label');
        label.htmlFor = input.id;
        label.innerHTML='<svg width="16" height="16"><use xlink:href="#icon-' + schemes[i] + '"></use></svg>';
        label.title='set site to ' + schemes[i] + ' theme';
        themeform.appendChild(label);
    }

    colorscheme = document.getElementsByName('colorscheme');
    for(var i = colorscheme.length; i--; ) {
        colorscheme[i].onclick = setTheme;
    }

    current_theme = getCurrentTheme();
    if (DEFAULT_THEME == current_theme) {
        indicateTheme(current_theme);
    }
    else {
        applyTheme(current_theme);
        indicateTheme(current_theme);
    }
}

setupTheme();
