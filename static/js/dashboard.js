let list_button = document.getElementById("list-btn")
let map_button = document.getElementById("map-btn")
let list_view = document.getElementById("list-view")
let map_view = document.getElementById("map-view")
let all_list_view = document.getElementById("all-list-btn")
let today_list_view = document.getElementById("today-list-btn")
let all_table_view = document.getElementById("all-table-view")
let today_table_view = document.getElementById("today-table-view")


all_list_view.addEventListener('click', onClickAllListButton)
today_list_view.addEventListener('click', onClickTodayListButton)
list_button.addEventListener('click', onClickListButton)
map_button.addEventListener('click', onClickMapButton)

function onClickListButton() {
    map_view.hidden = true
    list_view.hidden = false
}

function onClickMapButton() {
    map_view.hidden = false
    list_view.hidden = true
}

function onClickAllListButton() {
    today_table_view.hidden = true
    all_table_view.hidden = false
}

function onClickTodayListButton() {
    today_table_view.hidden = false
    all_table_view.hidden = true
}

$(document).ready( function () {
            $('#allTable').DataTable();
        } );

$(document).ready( function () {
            $('#todayTable').DataTable(
                {
    layout: {
        topStart: {
            buttons: [
                {
                    extend: 'pdfHtml5',
                    download: 'open'
                }
            ]
        }
    },
                    columnDefs: [
        {
            targets: 5,
            render: DataTable.render.datetime()
        }
    ]
}
            );
        } );