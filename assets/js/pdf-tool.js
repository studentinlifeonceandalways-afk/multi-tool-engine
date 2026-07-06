function loadPDFTool() {
    const container = document.getElementById('tool-content');
    container.innerHTML = `
        <h3>Merge PDF Files</h3>
        <input type="file" id="pdfInput" multiple accept=".pdf" class="form-control mb-3" onchange="addPDFs(this)">
        <button onclick="mergePDFs()" class="btn btn-primary">Merge PDFs</button>
        <div id="pdfList" class="mt-3"></div>
        <div id="result" class="mt-3"></div>
    `;
}

let pdfFiles = [];

function addPDFs(input) {
    pdfFiles = Array.from(input.files);
    const list = document.getElementById('pdfList');
    if (pdfFiles.length === 0) { list.innerHTML = ''; return; }
    list.innerHTML = `<h5>Selected PDFs (${pdfFiles.length})</h5><ul class="list-unstyled">`;
    pdfFiles.forEach((f, i) => list.innerHTML += `<li>${i+1}. ${f.name}</li>`);
    list.innerHTML += '</ul>';
}

async function mergePDFs() {
    if (pdfFiles.length < 2) { alert('Select at least 2 PDFs'); return; }
    document.getElementById('result').innerHTML = '<div class="alert alert-info">Merging...</div>';
    
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf-lib/1.17.1/pdf-lib.min.js';
    script.onload = async function() {
        try {
            const { PDFDocument } = PDFLib;
            const merged = await PDFDocument.create();
            for (const file of pdfFiles) {
                const reader = new FileReader();
                const bytes = await new Promise(resolve => {
                    reader.onload = e => resolve(new Uint8Array(e.target.result));
                    reader.readAsArrayBuffer(file);
                });
                const pdf = await PDFDocument.load(bytes);
                const pages = await merged.copyPages(pdf, pdf.getPageIndices());
                pages.forEach(p => merged.addPage(p));
            }
            const mergedBytes = await merged.save();
            const blob = new Blob([mergedBytes], { type: 'application/pdf' });
            const url = URL.createObjectURL(blob);
            document.getElementById('result').innerHTML = `
                <div class="alert alert-success">
                    <p><strong>✅ Merged Successfully!</strong></p>
                    <a href="${url}" download="merged.pdf" class="btn btn-success">Download</a>
                </div>
            `;
            pdfFiles = [];
            document.getElementById('pdfList').innerHTML = '';
        } catch(e) {
            document.getElementById('result').innerHTML = '<div class="alert alert-danger">Error merging. Try again.</div>';
        }
    };
    document.head.appendChild(script);
}
