function dataTable_renderer(data){
    $('#user_dataTable').DataTable( {
        data: data,
       "columnDefs": [
           {
               "targets": 3,
               "render": (data, type, row) => {
                   return "<a href='/media/" + data + "'>Click here</a>"
               }

           },
           {
             "targets": 10,
               "render": (data, type, row) => {
                 if (data === 1){
                     return "Active";
                 }
                 return "Closed";
               }

           },
           {
               "targets": 12,
               "render": (data, type, row) => {
                   let string = "<a href='/dashboard/employment/update/" + row[0] + "'><i class='fas fa-edit' data-toggle='tooltip' title='Edit'></i></a> " +
                       "<a href='/dashboard/employment/delete/" + row[0] + "'><i class='fas fa-trash' title='Delete'></i></a>";
                   return string

               }
           }
        ],
        columns: [
            { title: "Job id" },
            { title: "Title" },
            { title: "Company" },
            { title: "Logo" },
            { title: "Description" },
            { title: "Email" },
            { title: "Pay Rate" },
            { title: "Availability" },
            { title: "Duration" },
            { title: "Employment Type" },
            { title: "Status"},
            { title: "Created at"},
            { title: "Action"}
        ],
        bDestroy: true
    } );
}


function handler(data){
    dataTable_renderer(data);
    $('#searchbar_button').on('click', function (e){
            let params = {};
            $.each($('#search_form').serializeArray(), function (index, value) {
                params[value.name] = params[value.name] ? params[value.name] || value.value : value.value;
            });
            let url = "/filter?"
            for(let key in params){
                url+=key+ "=" + params[key] +"&";
            }
            $.ajax({
                type: 'get',
                url: url,
                processData: false,
                contentType: false,
                cache: false,
                success: function (response) {
                    let datatable = $("#user_dataTable").DataTable();
                    let json_data = response["data"].replaceAll("&#34;", '"');
                    let real_data = $.parseJSON(json_data);
                    datatable.clear().rows.add(real_data).draw();
                }
            });
            e.preventDefault();
        });

}
