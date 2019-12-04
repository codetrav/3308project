(function () {
  var commandErrors = [40];
  if (commandErrors >= 70) {
  document.getElementById("centerbox1").style.color = 'red';
  }
  else
  if (commandErrors >= 51 && udata <70)  
  {
  document.getElementById("centerbox1").style.color = 'yellow';
  }
  else
  if (commandErrors <=50)
  {
  document.getElementById("centerbox1").style.color = 'green';
  }
})();
