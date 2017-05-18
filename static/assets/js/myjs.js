function updatePackage() {
    $('#package-{{ package_value }}').click(function () {
        alert('{{ package_value }}');
    });
}

function selectAllUser(src) {
    var checkboxes = document.getElementsByTagName('input');
    if (src.checked) {
        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].name == 'selectUserName') {
                checkboxes[i].checked = true;
            }
        }
    } else {
        for (var i = 0; i < checkboxes.length; i++) {
            console.log(i)
            if (checkboxes[i].name == 'selectUserName') {
                checkboxes[i].checked = false;
            }
        }
    }
}

function selectAllGroup(src) {
    var checkboxes = document.getElementsByTagName('input');
    if (src.checked) {
        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].name == 'selectGroupName') {
                checkboxes[i].checked = true;
            }
        }
    } else {
        for (var i = 0; i < checkboxes.length; i++) {
            console.log(i)
            if (checkboxes[i].name == 'selectGroupName') {
                checkboxes[i].checked = false;
            }
        }
    }
}

function deleteAllGroup() {
    var items = document.getElementById('selectAll');
    items.remove()
}
