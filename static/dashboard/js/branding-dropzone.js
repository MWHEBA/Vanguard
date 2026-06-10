document.addEventListener("DOMContentLoaded", () => {
    const logoDropzone = document.querySelector("[data-logo-branding-dropzone]");
    const faviconDropzone = document.querySelector("[data-favicon-branding-dropzone]");
    
    if (!logoDropzone && !faviconDropzone) {
        return;
    }

    const logoInput = document.querySelector("[data-logo-branding-input]");
    const faviconInput = document.querySelector("[data-favicon-branding-input]");
    const logoPreview = document.querySelector("[data-logo-branding-preview]");
    const faviconPreview = document.querySelector("[data-favicon-branding-preview]");

    // الدالة دي بتتحقق إذا كان الملف أو الرابط لملف svg
    const isSvg = (fileOrUrl) => {
        if (!fileOrUrl) return false;
        if (typeof fileOrUrl === "string") {
            return fileOrUrl.split('?')[0].split('#')[0].toLowerCase().endsWith(".svg");
        }
        if (fileOrUrl instanceof File) {
            return fileOrUrl.name.toLowerCase().endsWith(".svg");
        }
        return false;
    };

    // الدالة دي بتجيب كود الـ HTML المناسب لعرض المعاينة للملف أو الرابط
    const getPreviewHtml = (fileOrUrl) => {
        if (!fileOrUrl) {
            return "<span>Drop here</span>";
        }
        if (isSvg(fileOrUrl)) {
            return `<div class="svg-preview-placeholder"><span class="svg-icon">SVG</span></div>`;
        }
        const src = typeof fileOrUrl === "string" ? escapeHtml(fileOrUrl) : "";
        if (src) {
            return `<img src="${src}" alt="">`;
        }
        return "";
    };

    const setLogoPreview = (fileOrUrl) => {
        if (!logoPreview) {
            return;
        }
        if (isSvg(fileOrUrl)) {
            logoPreview.innerHTML = getPreviewHtml(fileOrUrl);
            return;
        }
        if (typeof fileOrUrl === "string") {
            logoPreview.innerHTML = getPreviewHtml(fileOrUrl);
            return;
        }
        const reader = new FileReader();
        reader.onload = () => {
            logoPreview.innerHTML = `<img src="${escapeHtml(reader.result)}" alt="">`;
        };
        reader.readAsDataURL(fileOrUrl);
    };

    const setFaviconPreview = (fileOrUrl) => {
        if (!faviconPreview) {
            return;
        }
        if (isSvg(fileOrUrl)) {
            faviconPreview.innerHTML = getPreviewHtml(fileOrUrl);
            return;
        }
        if (typeof fileOrUrl === "string") {
            faviconPreview.innerHTML = getPreviewHtml(fileOrUrl);
            return;
        }
        const reader = new FileReader();
        reader.onload = () => {
            faviconPreview.innerHTML = `<img src="${escapeHtml(reader.result)}" alt="" style="width: 32px; height: 32px;">`;
        };
        reader.readAsDataURL(fileOrUrl);
    };

    // Logo dropzone
    if (logoDropzone && logoInput) {
        logoDropzone.addEventListener("dragover", (event) => {
            event.preventDefault();
            logoDropzone.classList.add("is-dragover");
        });

        logoDropzone.addEventListener("dragleave", () => {
            logoDropzone.classList.remove("is-dragover");
        });

        logoDropzone.addEventListener("drop", (event) => {
            event.preventDefault();
            logoDropzone.classList.remove("is-dragover");
            const file = event.dataTransfer.files[0];
            if (!file) return;
            const ext = file.name.split('.').pop().toLowerCase();
            
            // هنتأكد إن ملف اللوجو اللي اتسحب امتداده صح (webp, png, ico, svg)
            if (!['webp', 'png', 'ico', 'svg'].includes(ext)) {
                alert(`Warning: The file "${file.name}" is not supported. Only webp, png, ico, and svg are supported for logo.`);
                return;
            }

            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            logoInput.files = dataTransfer.files;
            setLogoPreview(file);
        });

        logoInput.addEventListener("change", () => {
            const file = logoInput.files[0];
            if (file) {
                const ext = file.name.split('.').pop().toLowerCase();
                // هنتأكد إن ملف اللوجو المختار امتداده صح
                if (!['webp', 'png', 'ico', 'svg'].includes(ext)) {
                    alert(`Warning: The file "${file.name}" is not supported. Only webp, png, ico, and svg are supported for logo.`);
                    logoInput.value = "";
                    return;
                }
                setLogoPreview(file);
            }
        });
    }

    // Favicon dropzone
    if (faviconDropzone && faviconInput) {
        faviconDropzone.addEventListener("dragover", (event) => {
            event.preventDefault();
            faviconDropzone.classList.add("is-dragover");
        });

        faviconDropzone.addEventListener("dragleave", () => {
            faviconDropzone.classList.remove("is-dragover");
        });

        faviconDropzone.addEventListener("drop", (event) => {
            event.preventDefault();
            faviconDropzone.classList.remove("is-dragover");
            const file = event.dataTransfer.files[0];
            if (!file) return;
            const ext = file.name.split('.').pop().toLowerCase();
            
            // هنتأكد إن ملف الـ Favicon اللي اتسحب امتداده صح (ico, png, svg)
            if (!['ico', 'png', 'svg'].includes(ext)) {
                alert(`Warning: The file "${file.name}" is not supported. Only ico, png, and svg are supported for favicon.`);
                return;
            }

            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            faviconInput.files = dataTransfer.files;
            setFaviconPreview(file);
        });

        faviconInput.addEventListener("change", () => {
            const file = faviconInput.files[0];
            if (file) {
                const ext = file.name.split('.').pop().toLowerCase();
                // هنتأكد إن ملف الـ Favicon المختار امتداده صح
                if (!['ico', 'png', 'svg'].includes(ext)) {
                    alert(`Warning: The file "${file.name}" is not supported. Only ico, png, and svg are supported for favicon.`);
                    faviconInput.value = "";
                    return;
                }
                setFaviconPreview(file);
            }
        });
    }
});

function escapeHtml(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
