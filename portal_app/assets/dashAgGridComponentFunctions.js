var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};
var dagfuncs = window.dashAgGridFunctions = window.dashAgGridFunctions || {};


dagcomponentfuncs.urlCellRenderer = function (params) {
  console.log(params);
  var app_url = params.value;

  if (app_url === undefined || !app_url || app_url == '') {
    return React.createElement('div');
  }
  else{
    var app_external_link = React.createElement(
      window.dash_mantine_components.Anchor,
      {
          href: app_url,
          color: '#00B0F0',
          underline: true,
          target: '_blank',
          size: 16,
          style: {display: 'flex', flexWrap: 'nowrap', overflowX: 'hidden', whiteSpace: 'nowrap'},
      },
      app_url
  );
  }
  return app_external_link;
}







function create_badge(badge_variant, badge_class, badge_value, badge_style={width: '100%'}) {
    var badge = React.createElement(
      window.dash_mantine_components.Badge,
      {
          variant: badge_variant,
          radius: 'sm',
          className: badge_class,
          style: badge_style,
      },
      badge_value
  );
    return badge;
}


function create_tooltip(label, component){
  var tooltip = React.createElement(
    window.dash_mantine_components.FloatingTooltip,
    {
        label: label,
        style: {fontSize: '0.75rem'

        },
    },
    component
);
  return tooltip;

}

function formatLongText(text_value, limit) {
  if (text_value.length <= limit) {
      return text_value; // If length is limit or less, return the original text
  } else {
      return text_value.slice(0, limit - 2) + '..'; // Otherwise, truncate and add '..'
  }
}


function getKey(object, key, default_value) {
  var result = object[key];
  return (typeof result !== "undefined") ? result : default_value;
}