function dataTable_renderer(data){
    $('#user_dataTable').DataTable( {
        data: data,
       "columnDefs": [
            {
                "targets": 10,
                "visible": false,
                "searchable": false
            },
           {
               "targets": 3,
               "render": (data, type, row) => {
                   return "<a href='/media/" + data + "'>Click here</a>"
               }

           },
           {
               "targets": 11,
               "render": (data, type, row) => {
                   let string = "<a href='#'><i class='fas fa-edit' data-toggle='tooltip' title='Edit'></i></a> " +
                       "<a href='#'><i class='fas fa-trash' title='Delete'></i></a>";
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
            { title: "Created at"},
            { title: "Action"}
        ],
        bDestroy: true
    } );
}


function handler(data){
    dataTable_renderer(data);
    $('#addUserModal').on('show.bs.modal', function (event) {
            $('#cancel_button').on('click', function (e) {
                $('#addUserModal').modal('toggle');
                return false;
            });
            $('#addRegister_button').on('click', function (e){
                // Create Applicant
                let params = {};
                $.each($('#register_employee').serializeArray(), function (index, value) {
                    params[value.name] = params[value.name] ? params[value.name] || value.value : value.value;
                });
                let form_data = new FormData();
                for(let key in params){
                    form_data.append(key, params[key]);
                }
                form_data.append('resume', $("#resume")[0].files[0]);
                console.log(form_data)
                $.ajax({
                    type: 'post',
                    url: "create",
                    data: form_data,
                    processData: false,
                    contentType: false,
                    cache: false,
                    success: function (response) {
                        console.log(response);
                        if(response.status_code){
                            window.location.href = response.url;
                        }
                    }
                });
                e.preventDefault();
            });

        });
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
