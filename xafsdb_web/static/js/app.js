const date = document.querySelector("#date");
// set year
date.innerHTML = new Date().getFullYear();

// show/hide tables
function showHideRow(row) {
    $("#" + row).toggle();
}

function toggleTable() {
    var lTable = document.getElementById("loginTable");
    lTable.style.display = (lTable.style.display == "table") ? "none" : "table";
}

function toggle(thisname) {
 tr=document.getElementsByTagName('tr')
 for (i=0;i<tr.length;i++){
  if (tr[i].getAttribute(thisname)){
   if ( tr[i].style.display=='none' ){
     tr[i].style.display = '';
   }
   else {
    tr[i].style.display = 'none';
   }
  }
 }
}
