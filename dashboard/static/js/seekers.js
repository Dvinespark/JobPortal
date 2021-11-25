function dataTable_renderer(data) {
    $('#job_seekers_dataTable').DataTable({
        data: data,
        "columnDefs": [
            {
                "targets": 0,
                "visible": false,
                "searchable": false
            },
            {
                "targets": 10,
                "visible": false,
                "searchable": false
            },
            {
                "targets": 9,
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
            {title: "Id"},
            {title: "Firstname"},
            {title: "Lastname"},
            {title: "Email"},
            {title: "Skill 1"},
            {title: "Experience Year"},
            {title: "Phone Number"},
            {title: "Status"},
            {title: "Availability"},
            {title: "Resume"},
            {title: "Job Id"},
            {title: "Action"}
        ],
        bDestroy: true
    });
}

function handler(data) {
    dataTable_renderer(data);
}

$('#seeker_search_button').on('click', function (e) {
    let params = {};
    let form_data = $('#search_form').serializeArray();
    $.each(form_data, function (index, value) {
        params[value.name] = params[value.name] ? params[value.name] || value.value : value.value;
    });
    let url = "jobseeker/filter?"
    for (let key in params) {
        if (params[key]){
            url += key + "=" + params[key] + "&";
        }
    }
    $.ajax({
        type: 'get',
        url: url,
        success: function (response) {
            console.log(response.data);
            let response_data = $.parseJSON(response.data);
            let datatable = $("#job_seekers_dataTable").DataTable();
            datatable.clear().rows.add(response_data).draw();
        }
    });
    e.preventDefault();
    e.stopImmediatePropagation();
});
