const is_login = () => {
  let returnValue = false;
  let idToken = localStorage.getItem('idToken');
  if('idToken' in localStorage) {
    $.ajax({
      url: '/idTokenCheck/',
      type: 'GET',
      async: false,
      data: {'token': idToken},
      success: function(data) {
          if(data === 'exist') {
              returnValue = true;
          } else {
              returnValue = false;
          }
      }
    });
  }
  return returnValue;
}

const validation_main = () => {
  if (is_login() === false) {
    location.href = "/";
  }
}

const validation_login = () => {
  if (is_login() === false) {
    location.href = "/main";
  }
}