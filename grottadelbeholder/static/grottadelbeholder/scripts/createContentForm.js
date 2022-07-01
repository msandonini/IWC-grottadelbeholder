document.addEventListener('DOMContentLoaded', function() {
    let categorySelect = document.getElementById("id_category");

    categorySelect.onchange = function () {showSelectedForm()};

    showSelectedForm()
}, false);

function showSelectedForm() {
    let categorySelect = document.getElementById("id_category");
    let detailForm = document.getElementById("detailForm");

    let categoryFormsDiv = document.getElementById("categoryForms");
    categoryFormsDiv.innerHTML += detailForm.innerHTML;

    detailForm.innerHTML = "";

    switch (categorySelect.value) {
        case 'CL': {
            let classForm = document.getElementById("classForm");

            detailForm.appendChild(classForm);

            break;
        }
        case 'RA': {
            let raceForm = document.getElementById("raceForm");

            detailForm.appendChild(raceForm);

            break;
        }
        case 'MO': {
            let monsterForm = document.getElementById("monsterForm");

            detailForm.appendChild(monsterForm);

            break;
        }
        case 'SP': {
            let spellForm = document.getElementById("spellForm");

            detailForm.appendChild(spellForm);

            break;
        }
    }
}

function submitForm() {
    document.getElementById("contentForm").submit();
}