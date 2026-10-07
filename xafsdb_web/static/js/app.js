///
/// @author: Sebastian Paripsa
///


const date = document.querySelector("#date");
// set year (optional element: no template currently renders #date, and
// dereferencing null here threw before the rest of this file could run)
if (date) {
    date.innerHTML = new Date().getFullYear();
}

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
