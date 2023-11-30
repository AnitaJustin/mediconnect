function updateMedicineDropdown(diseaseDropdownId, medicineDropdownId) {
    var selectedDisease = $(diseaseDropdownId).val();
    if (selectedDisease) {
        $.ajax({
            url: `/get_medicines/${selectedDisease}/`,
            type: 'GET',
            success: function (data) {
                var medicinesDropdown = $(medicineDropdownId);
                medicinesDropdown.empty();

                // Assuming data is an array of medicine names
                data.forEach(function (medicine) {
                    medicinesDropdown.append('<option value="' + medicine.name + '">' + medicine.name + '</option>');
                });
            },
            error: function (error) {
                console.log(error);
            }
        });
  
    } else {
        // If no disease is selected, clear the medicine dropdown
        $(medicineDropdownId).empty();
    }
}
function updateMedicineCount(diseaseDropdownId, medicineDropdownId,quantityFieldId) {
    var selectedDisease = $(diseaseDropdownId).val();
    var selectedMedicine=$(medicineDropdownId).val();

    if (selectedDisease && selectedMedicine) {
        $.ajax({
            url: `/get_number/${selectedDisease}/${selectedMedicine}/`,
            type: 'GET',
            success: function (data) {
                console.log(data);
                // Assuming data is the number of corresponding medicines
                var quantityField = $(quantityFieldId);
                quantityField.attr('placeholder', 'Enter quantity (Max: ' + data.count + ')');
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
}


$(document).ready(function () {
    updateMedicineDropdown('#id_disease', '#id_medicine');

    // Set up an event listener for the disease dropdown change
    $('#id_disease').change(function () {
        updateMedicineDropdown('#id_disease', '#id_medicine');
    });
});


