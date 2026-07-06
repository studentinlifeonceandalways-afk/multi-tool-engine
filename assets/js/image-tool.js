function loadImageTool() {
    const container = document.getElementById('tool-content');
    container.innerHTML = `
        <h3>Compress Your Image</h3>
        <input type="file" id="imageInput" accept="image/*" class="form-control mb-3">
        <button onclick="compressImage()" class="btn btn-primary">Compress Image</button>
        <div id="result" class="mt-3"></div>
        <div class="mt-3 text-muted">
            <small>Max file: 10MB | Supports: JPG, PNG, WebP</small>
        </div>
    `;
}

function compressImage() {
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];
    if (!file) { alert('Please select an image'); return; }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            let width = img.width, height = img.height;
            const maxSize = 800;
            if (width > height) {
                if (width > maxSize) { height *= maxSize / width; width = maxSize; }
            } else {
                if (height > maxSize) { width *= maxSize / height; height = maxSize; }
            }
            
            canvas.width = width; canvas.height = height;
            ctx.drawImage(img, 0, 0, width, height);
            const compressed = canvas.toDataURL('image/jpeg', 0.7);
            
            document.getElementById('result').innerHTML = `
                <div class="alert alert-success mt-3">
                    <p><strong>✅ Compressed Successfully!</strong></p>
                    <img src="${compressed}" class="img-fluid mb-2" style="max-height: 300px;">
                    <br><a href="${compressed}" download="compressed.jpg" class="btn btn-success">Download</a>
                </div>
            `;
        };
        img.src = e.target.result;
    };
    reader.readAsDataURL(file);
}
