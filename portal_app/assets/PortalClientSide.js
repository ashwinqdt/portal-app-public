
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {

        table_style: function(theme) {
            if (theme === 'light') {
                return 'ag-theme-alpine';
            } else {
                return 'ag-theme-alpine-dark';
            }

        },



    }
});



