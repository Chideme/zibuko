/*!
* Start Bootstrap - Simple Sidebar v6.0.1 (https://startbootstrap.com/template/simple-sidebar)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-simple-sidebar/blob/master/LICENSE)
*/
// 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }
    //DataTables function
        var p = document.getElementById('export');
        if(p){

        
        $('#export').DataTable( {
            dom: '<"pull-left"f><"pull-right"B>tip',
            
            "lengthMenu": [ 200, 150, 100, 75],
            buttons: [
                'pageLength',
                'copy',
                'excel',
                'csv',
                'pdf'
            ]
        } );}

        
          
// html2pdf

$('#download').on('click',function(){
    var element = document.getElementById('printTable');
    var opt = {
    margin:       [1,1,1,1],
    filename:     'statement'+'.pdf',
    html2canvas:  { scale: 2, bottom: 0 },
    jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' ,compressPDF: true},
    pagebreak: { before: "tr"}
    };

  
    // Old monolithic-style usage:
    html2pdf(element, opt);
    })

});