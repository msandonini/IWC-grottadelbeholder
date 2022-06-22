function createContentForm(selector) {
    let form = document.getElementById("contentForm");

    let formChildren = form.children;

    for (let i = 0; i < formChildren.length; i ++) {
        if (formChildren[i].getAttribute('name') !== 'csrfmiddlewaretoken' &&
            formChildren[i].getAttribute('name') !== 'typeSelector' &&
            formChildren[i].id !== 'typeSelectorLabel') {
            formChildren[i].remove();
            i --;
        }
    }

    let br = document.createElement("br");

    form.appendChild(br);
    form.appendChild(br.cloneNode())

    let nameLabel = document.createElement("label");
    nameLabel.htmlFor = "contentName";
    nameLabel.textContent = "Nome: ";

    let name = document.createElement("input");
    name.type = "text";
    name.id = "contentName";
    name.name = "name";

    form.appendChild(nameLabel);
    form.appendChild(name);

    form.appendChild(br.cloneNode());
    form.appendChild(br.cloneNode());

    let descriptionLabel = document.createElement("label");
    descriptionLabel.htmlFor = "contentDescription";
    descriptionLabel.textContent = "Descrizione: "

    let description = document.createElement("textarea");
    description.name = "description";
    description.id = "contentDescription"
    description.rows = 10;

    form.appendChild(descriptionLabel);
    form.appendChild(br.cloneNode());
    form.appendChild(description);
    form.appendChild(br.cloneNode());
    form.appendChild(br.cloneNode());

    // TODO inserire form varianti al contenuto
    switch (selector.value) {
        case 'CL': {
// -------- HP

            let hpTable = document.createElement("table");
            hpTable.id = "hpTable";
            form.appendChild(hpTable)

            let hpTable_caption = document.createElement("caption");
            hpTable_caption.textContent = "Punti Vita";
            hpTable.appendChild(hpTable_caption);

            let tr = document.createElement("tr");

            hpTable.appendChild(tr);

            let td = document.createElement("td");
            tr.appendChild(td);

            let hpl1_label = document.createElement("label");
            hpl1_label.htmlFor = "hitPointsLevel1";
            hpl1_label.textContent = "Punti Vita al livello 1:";

            td.appendChild(hpl1_label);

            let hpl1 = document.createElement("input")  // TODO controllare all'invio che non sia maggiore di 20
            hpl1.type = "number";
            hpl1.min = "1";
            hpl1.max = "20";
            hpl1.id = "hitPointsLevel1";
            hpl1.className = "td";
            hpl1.name = "hitPointsLevel1";
            hpl1.maxLength = 2;

            td = td.cloneNode();
            td.appendChild(hpl1);

            tr.appendChild(td);

            let hpAbove1_label = document.createElement("label");
            hpAbove1_label.htmlFor = "hitPointsAboveLv1";
            hpAbove1_label.textContent = "Punti vita oltre il livello 1:";

            td = td.cloneNode();
            td.appendChild(hpAbove1_label);
            tr.appendChild(td);

            let hpAbove1 = document.createElement("input"); // TODO controllare all'invio che non sia più lungo di 25 caratteri
            hpAbove1.type = "text";
            hpAbove1.id = "hitPointsAboveLv1";
            hpAbove1.name = "hitPointsAboveLevel1"
            hpAbove1.maxLength = 25;

            td = td.cloneNode();
            td.appendChild(hpAbove1);

            tr.appendChild(td);

            tr = tr.cloneNode();
            hpTable.appendChild(tr)

            let hitDiceType_label = document.createElement("label");
            hitDiceType_label.htmlFor = "hitDiceType";
            hitDiceType_label.textContent = "Tipo di dado vita: ";

            td = td.cloneNode();
            tr.appendChild(td);
            td.appendChild(hitDiceType_label);

            let hitDiceType = document.createElement("select"); // TODO controllare all'invio che non sia più lungo di 5 caratteri
            hitDiceType.name = "hitDiceType";

            td = td.cloneNode();
            tr.appendChild(td);
            td.appendChild(hitDiceType);

            let option = document.createElement("option");
            option.value = "1d4";
            option.textContent = "1d4";
            hitDiceType.appendChild(option);

            option = option.cloneNode();

            option.value = "1d6";
            option.textContent = "1d6";
            hitDiceType.appendChild(option);

            option = option.cloneNode();

            option.value = "1d8";
            option.textContent = "1d8";
            hitDiceType.appendChild(option);

            option = option.cloneNode();

            option.value = "1d10";
            option.textContent = "1d10";
            hitDiceType.appendChild(option);

            option = option.cloneNode();

            option.value = "1d12";
            option.textContent = "1d12";
            hitDiceType.appendChild(option);

            option = option.cloneNode();

            option.value = "1d20";
            option.textContent = "1d20";
            hitDiceType.appendChild(option);

// -------- PROFICIENCIES

            let profTable = document.createElement("table");
            profTable.id = "profTable";
            form.appendChild(profTable);

            let profTable_caption = document.createElement("caption");
            profTable_caption.textContent = "Competenze";
            profTable.appendChild(profTable_caption);

            tr = document.createElement("tr");
            profTable.appendChild(tr);
            td = document.createElement("td");


            let armorProficiency_label = document.createElement("label");
            armorProficiency_label.htmlFor = "armorProficiency"
            armorProficiency_label.textContent = "Armature:"

            td.appendChild(armorProficiency_label);
            tr.appendChild(td);

            let armorProficiency = document.createElement("select");
            armorProficiency.name = "armorProficiency";

            td = td.cloneNode();
            td.appendChild(armorProficiency);
            tr.appendChild(td);

            option = document.createElement("option");
            option.value = "N";
            option.textContent = "Nessuna";

            armorProficiency.appendChild(option);

            option = option.cloneNode();
            option.textContent = "Armature leggere";
            option.value = "L";

            armorProficiency.appendChild(option);

            option = option.cloneNode();
            option.textContent = "Armature medie";
            option.value = "M";

            armorProficiency.appendChild(option);

            option = option.cloneNode();
            option.textContent = "Tutte le armature";
            option.value = "A";

            armorProficiency.appendChild(option);

            let shieldProficiency_label = document.createElement("label");
            shieldProficiency_label.htmlFor = "shieldProficiency";
            shieldProficiency_label.textContent = "Scudo? ";

            let shieldProficiency = document.createElement("input");
            shieldProficiency.type = "checkbox";
            shieldProficiency.name = "shieldProficiency";
            shieldProficiency.value = "shieldProficiency";

            td = td.cloneNode();
            td.appendChild(shieldProficiency);
            tr.appendChild(td);

            td.appendChild(shieldProficiency_label);

            td = td.cloneNode();
            tr.appendChild(td);

            tr = tr.cloneNode();
            profTable.appendChild(tr);

            let weaponProficiency_label = document.createElement("label");
            weaponProficiency_label.htmlFor = "weaponProficiency";
            weaponProficiency_label.textContent = "Armi:";

            let weaponProficiency = document.createElement("textarea");
            weaponProficiency.name = "weaponProficiency";
            weaponProficiency.id = "weaponProficiency";

            td = td.cloneNode();
            td.appendChild(weaponProficiency_label);
            td.appendChild(weaponProficiency);
            td.colSpan = 4;
            tr.appendChild(td);

            td = td.cloneNode();
            tr.appendChild(td);
            td = td.cloneNode();
            tr.appendChild(td);
            td = td.cloneNode();
            tr.appendChild(td);

            /*

            armorProficiency =              // Selezione tipi di armature
            shieldProficiency =             // Checkbox per competenza con lo scudo
            weaponProficiency =             // Testo
                                            // TODO controllare all'invio che sia al massimo di 100 caratteri
            toolProficiency =               // Testo
                                            // TODO Controllare all'invio che sia al massimo di 100 caratteri

            savingThrows =                  // Testo
                                            // TODO Controllare all'invio che sia al massimo di 100 caratteri
            Skills =                        // Testo
                                            // TODO Controllare all'invio che sia al massimo di 200 caratteri

            abilities =                     // Textarea

            archetypes =                    // Textarea
*/
            break;
        }
        case 'RA': {
            break;
        }
        case 'MO': {
            break;
        }
        case 'SP': {
            break;
        }
    }
}