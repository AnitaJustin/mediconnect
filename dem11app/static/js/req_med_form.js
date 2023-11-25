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
$(document).ready(function () {
    updateMedicineDropdown('#id_disease', '#id_medicine');

    // Set up an event listener for the disease dropdown change
    $('#id_disease').change(function () {
        updateMedicineDropdown('#id_disease', '#id_medicine');
    });
});