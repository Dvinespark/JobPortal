function dataTable_renderer(data){
    $('#user_dataTable').DataTable( {
        data: data,
        "columnDefs": [
            {
                "targets": 0,
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
                    let string = "<a class='btn-github apply-btn' href='#applyJob' data-toggle='modal' data-jobid=" + row[0] +
                        "><i class='fas fa-briefcase' data-toggle='tooltip' title='Apply'></i></a>";
                    return string;

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
    $('#applyJob').on('show.bs.modal', function (event) {
            $('#cancel_button').on('click', function (e) {
                $('#applyJob').modal('toggle');
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
            if(params.length > 0)
            {
                $.ajax({
                type: 'get',
                url: url,
                processData: false,
                contentType: false,
                cache: false,
                success: function (response) {
                    let datatable = $("#user_dataTable").DataTable();
                    let response_data = $.parseJSON(response['data']);
                    datatable.clear().rows.add(response_data).draw();
                }
            });
            e.preventDefault();
            }

        });

}
