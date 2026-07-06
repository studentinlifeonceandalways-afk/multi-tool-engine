function loadConverterTool() {
    const container = document.getElementById('tool-content');
    const fromUnit = "{{ from_unit }}";
    const toUnit = "{{ to_unit }}";
    const factor = parseFloat("{{ conversion_factor }}");
    
    container.innerHTML = `
        <h3>Convert ${fromUnit} to ${toUnit}</h3>
        <div class="row">
            <div class="col-md-6">
                <label class="form-label">${fromUnit}:</label>
                <input type="number" id="inputValue" class="form-control" placeholder="Enter value" oninput="convert(${factor}, '${fromUnit}', '${toUnit}')">
            </div>
            <div class="col-md-6">
                <label class="form-label">${toUnit}:</label>
                <input type="text" id="resultValue" class="form-control" readonly placeholder="Result">
            </div>
        </div>
        <div class="mt-3 text-muted">
            <small>1 ${fromUnit} = ${factor} ${toUnit}</small>
        </div>
    `;
}

function convert(factor, fromUnit, toUnit) {
    const input = document.getElementById('inputValue');
    const result = document.getElementById('resultValue');
    if (input.value === '') { result.value = ''; return; }
    const val = parseFloat(input.value);
    if (!isNaN(val)) { result.value = (val * factor).toFixed(4) + ' ' + toUnit; }
}
