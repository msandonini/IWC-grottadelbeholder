document.addEventListener('DOMContentLoaded', function() {
    let categorySelect = document.getElementById("id_category");

    categorySelect.onchange = function () {showSelectedForm()};

    let classForm = document.getElementById("classForm");
    let raceForm = document.getElementById("raceForm");
    let monsterForm = document.getElementById("monsterForm");
    let spellForm = document.getElementById("spellForm");

    classForm.style.display = "block";
    raceForm.style.display = "none";
    monsterForm.style.display = "none";
    spellForm.style.display = "none";
}, false);

function showSelectedForm() {
    let categorySelect = document.getElementById("id_category");

    let classForm = document.getElementById("classForm");
    let raceForm = document.getElementById("raceForm");
    let monsterForm = document.getElementById("monsterForm");
    let spellForm = document.getElementById("spellForm");

    switch (categorySelect.value) {
        case 'CL': {
            classForm.style.display = "block";
            raceForm.style.display = "none";
            monsterForm.style.display = "none";
            spellForm.style.display = "none";

            break;
        }
        case 'RA': {
            classForm.style.display = "none";
            raceForm.style.display = "block";
            monsterForm.style.display = "none";
            spellForm.style.display = "none";

            break;
        }
        case 'MO': {
            classForm.style.display = "none";
            raceForm.style.display = "none";
            monsterForm.style.display = "block";
            spellForm.style.display = "none";

            break;
        }
        case 'SP': {
            classForm.style.display = "none";
            raceForm.style.display = "none";
            monsterForm.style.display = "none";
            spellForm.style.display = "block";

            break;
        }
    }
}

function submitForm() {
    document.getElementById("contentForm").submit();
}