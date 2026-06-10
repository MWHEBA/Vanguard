document.addEventListener("DOMContentLoaded", () => {
    const dropzone = document.querySelector("[data-gallery-dropzone]");
    const galleryList = document.querySelector("[data-gallery-list]");
    if (!dropzone || !galleryList) {
        return;
    }

    const input = dropzone.querySelector("[data-gallery-input]");
    const status = document.querySelector("[data-gallery-status]");
    const uploadUrl = dropzone.dataset.uploadUrl;
    const reorderUrl = dropzone.dataset.reorderUrl;
    const replaceUrlTemplate = dropzone.dataset.replaceUrlTemplate;
    const titleUrlTemplate = dropzone.dataset.titleUrlTemplate;
    const deleteUrlTemplate = dropzone.dataset.deleteUrlTemplate;

    const primaryDropzone = document.querySelector("[data-primary-image-dropzone]");
    const primaryInput = document.querySelector("[data-primary-image-input]");
    const primaryPreview = document.querySelector("[data-primary-image-preview]");

    const logoDropzone = document.querySelector("[data-logo-image-dropzone]");
    const logoInput = document.querySelector("[data-logo-image-input]");
    const logoPreview = document.querySelector("[data-logo-image-preview]");

    const csrfToken = getCsrfToken();
    let draggedCard = null;

    // الدالة دي بتتحقق إذا كان الملف أو الرابط لملف glb
    const isGlb = (fileOrUrl) => {
        if (!fileOrUrl) return false;
        if (typeof fileOrUrl === "string") {
            return fileOrUrl.split('?')[0].split('#')[0].toLowerCase().endsWith(".glb");
        }
        if (fileOrUrl instanceof File) {
            return fileOrUrl.name.toLowerCase().endsWith(".glb");
        }
        return false;
    };

    // الدالة دي بتجيب كود الـ HTML المناسب لعرض المعاينة للملف أو الرابط
    const getPreviewHtml = (fileOrUrl) => {
        if (!fileOrUrl) {
            return "<span>No image</span>";
        }
        if (isGlb(fileOrUrl)) {
            return `<div class="glb-preview-placeholder"><span class="glb-icon">3D</span><span class="glb-label">.GLB Model</span></div>`;
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
        if (isGlb(fileOrUrl)) {
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

    const setLogoInputFile = (file) => {
        if (!logoInput || !file) {
            return;
        }
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        logoInput.files = dataTransfer.files;
        setLogoPreview(file);
        setStatus("Logo ready to save.", "success");
    };

    const setPrimaryPreview = (fileOrUrl) => {
        if (!primaryPreview) {
            return;
        }
        if (isGlb(fileOrUrl)) {
            primaryPreview.innerHTML = getPreviewHtml(fileOrUrl);
            return;
        }
        if (typeof fileOrUrl === "string") {
            primaryPreview.innerHTML = getPreviewHtml(fileOrUrl);
            return;
        }
        const reader = new FileReader();
        reader.onload = () => {
            primaryPreview.innerHTML = `<img src="${escapeHtml(reader.result)}" alt="">`;
        };
        reader.readAsDataURL(fileOrUrl);
    };

    const setPrimaryInputFile = (file) => {
        if (!primaryInput || !file) {
            return;
        }
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        primaryInput.files = dataTransfer.files;
        setPrimaryPreview(file);
        setStatus("Primary image ready to save.", "success");
    };

    const setStatus = (message, tone = "") => {
        if (!status) {
            return;
        }
        status.textContent = message;
        status.dataset.tone = tone;
    };

    const endpointFor = (template, id) => template.replace("/0/", `/${id}/`);

    const request = async (url, options = {}) => {
        const response = await fetch(url, {
            credentials: "same-origin",
            headers: {
                "Accept": "application/json",
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": csrfToken,
                ...(options.headers || {}),
            },
            ...options,
        });
        const contentType = response.headers.get("content-type") || "";
        if (!contentType.includes("application/json")) {
            throw new Error("Dashboard session or CSRF token expired. Refresh the page and try again.");
        }
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Gallery request failed.");
        }
        return data;
    };

    const uploadFiles = async (files) => {
        const allowedExtensions = ["webp", "png", "glb"];
        const filesArray = Array.from(files || []);
        
        // هنتأكد إن كل الملفات المحددة ليها امتداد مسموح بيه (webp, png, glb)
        const invalidFiles = filesArray.filter(file => {
            const ext = file.name.split('.').pop().toLowerCase();
            return !allowedExtensions.includes(ext);
        });

        if (invalidFiles.length > 0) {
            const invalidNames = invalidFiles.map(f => f.name).join(", ");
            alert(`Warning: The following files are not supported: ${invalidNames}. Only webp, png, and glb are supported.`);
            setStatus(`Unsupported file formats selected: ${invalidNames}`, "error");
            if (input) {
                input.value = "";
            }
            return;
        }

        if (!filesArray.length) {
            setStatus("Select one or more files.", "error");
            return;
        }

        const payload = new FormData();
        filesArray.forEach((file) => payload.append("images", file));

        dropzone.classList.add("is-uploading");
        setStatus("Uploading gallery files...");

        try {
            const data = await request(uploadUrl, {
                method: "POST",
                body: payload,
            });
            data.items.forEach((item) => galleryList.appendChild(createUploadedCard(item)));
            bindGalleryCards();
            await saveOrder();
            const errorText = data.errors && data.errors.length ? ` ${data.errors.join(" ")}` : "";
            setStatus(`${data.items.length} file(s) uploaded.${errorText}`, data.errors && data.errors.length ? "warning" : "success");
        } catch (error) {
            setStatus(error.message, "error");
        } finally {
            dropzone.classList.remove("is-uploading");
            if (input) {
                input.value = "";
            }
        }
    };

    const createUploadedCard = (item) => {
        const card = document.createElement("article");
        card.className = "gallery-card is-new";
        card.draggable = true;
        card.dataset.galleryCard = "";
        card.dataset.visualId = item.id;
        card.innerHTML = `
            <button class="drag-handle" type="button" data-drag-handle aria-label="Drag to reorder">::</button>
            <div class="gallery-preview">
                ${getPreviewHtml(item.imageUrl || item.imagePath)}
            </div>
            <div class="gallery-change">
                <input id="gallery-replace-${item.id}" type="file" accept=".webp,.png,.glb,image/webp,image/png" data-gallery-replace-input>
                <label class="icon-action" for="gallery-replace-${item.id}" aria-label="Change image">
                    <span aria-hidden="true">↻</span>
                </label>
            </div>
            <div class="gallery-card-body">
                <div class="gallery-fields">
                    <label>
                        <span>Title</span>
                        <input class="dashboard-input" type="text" value="${escapeHtml(item.title || "")}" data-gallery-title-input>
                    </label>
                </div>
            </div>
            <button class="gallery-delete-button" type="button" data-gallery-delete aria-label="Delete ${escapeHtml(item.title || "gallery image")}">x</button>
        `;
        return card;
    };

    const bindGalleryCards = () => {
        galleryList.querySelectorAll("[data-gallery-card]").forEach((card) => {
            card.removeEventListener("dragstart", onDragStart);
            card.removeEventListener("dragend", onDragEnd);
            card.addEventListener("dragstart", onDragStart);
            card.addEventListener("dragend", onDragEnd);

            const deleteButton = card.querySelector("[data-gallery-delete]");
            const replaceInput = card.querySelector("[data-gallery-replace-input]");
            const titleInput = card.querySelector("[data-gallery-title-input]");
            if (replaceInput) {
                replaceInput.onchange = () => replaceImage(card, replaceInput.files[0], replaceInput);
            }
            if (titleInput) {
                titleInput.onchange = () => updateTitle(card, titleInput);
            }
            if (deleteButton) {
                deleteButton.onclick = () => deleteCard(card);
            }
        });
    };

    const onDragStart = (event) => {
        draggedCard = event.currentTarget;
        draggedCard.classList.add("is-dragging");
        event.dataTransfer.effectAllowed = "move";
        event.dataTransfer.setData("text/plain", draggedCard.dataset.visualId || "");
    };

    const onDragEnd = async () => {
        if (draggedCard) {
            draggedCard.classList.remove("is-dragging");
        }
        draggedCard = null;
        await saveOrder();
    };

    galleryList.addEventListener("dragover", (event) => {
        event.preventDefault();
        const afterElement = getDragAfterElement(galleryList, event.clientY);
        if (!draggedCard) {
            return;
        }
        if (afterElement == null) {
            galleryList.appendChild(draggedCard);
        } else {
            galleryList.insertBefore(draggedCard, afterElement);
        }
    });

    const getDragAfterElement = (container, y) => {
        const cards = [...container.querySelectorAll("[data-gallery-card]:not(.is-dragging)")];
        return cards.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;
            if (offset < 0 && offset > closest.offset) {
                return { offset, element: child };
            }
            return closest;
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    };

    const saveOrder = async () => {
        const form = new URLSearchParams();
        galleryList.querySelectorAll("[data-gallery-card]").forEach((card) => {
            form.append("visual_ids[]", card.dataset.visualId);
        });
        try {
            await request(reorderUrl, {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: form.toString(),
            });
            setStatus("Gallery order saved.", "success");
        } catch (error) {
            setStatus(error.message, "error");
        }
    };

    const deleteCard = async (card) => {
        if (!window.confirm("Delete this gallery item?")) {
            return;
        }
        try {
            await request(endpointFor(deleteUrlTemplate, card.dataset.visualId), { method: "POST" });
            card.remove();
            await saveOrder();
            setStatus("Gallery item deleted.", "success");
        } catch (error) {
            setStatus(error.message, "error");
        }
    };

    const replaceImage = async (card, file, inputElement) => {
        if (!file) {
            return;
        }

        const ext = file.name.split('.').pop().toLowerCase();
        // هنتحقق إن امتداد الملف مسموح بيه للاستبدال
        if (!['webp', 'png', 'glb'].includes(ext)) {
            alert(`Warning: The file "${file.name}" is not supported. Only webp, png, and glb are supported.`);
            setStatus(`Replacement file must be webp, png, or glb.`, "error");
            if (inputElement) {
                inputElement.value = "";
            }
            return;
        }

        const payload = new FormData();
        payload.append("image", file);
        setStatus("Replacing image...");

        try {
            const item = await request(endpointFor(replaceUrlTemplate, card.dataset.visualId), {
                method: "POST",
                body: payload,
            });
            const preview = card.querySelector(".gallery-preview");
            if (preview) {
                preview.innerHTML = getPreviewHtml(item.imageUrl || item.imagePath);
            }
            setStatus("Image replaced.", "success");
        } catch (error) {
            setStatus(error.message, "error");
        } finally {
            if (inputElement) {
                inputElement.value = "";
            }
        }
    };

    const updateTitle = async (card, inputElement) => {
        const title = inputElement.value.trim();
        if (!title) {
            setStatus("Title is required.", "error");
            return;
        }

        const payload = new URLSearchParams();
        payload.append("title", title);

        try {
            await request(endpointFor(titleUrlTemplate, card.dataset.visualId), {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: payload.toString(),
            });
            setStatus("Gallery title saved.", "success");
        } catch (error) {
            setStatus(error.message, "error");
        }
    };

    dropzone.addEventListener("dragover", (event) => {
        event.preventDefault();
        dropzone.classList.add("is-dragover");
    });

    dropzone.addEventListener("dragleave", () => {
        dropzone.classList.remove("is-dragover");
    });

    dropzone.addEventListener("drop", (event) => {
        event.preventDefault();
        dropzone.classList.remove("is-dragover");
        uploadFiles(event.dataTransfer.files);
    });

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
            // هنتأكد إن ملف اللوجو اللي اتسحب امتداده صح
            if (!['webp', 'png', 'glb'].includes(ext)) {
                alert(`Warning: The file "${file.name}" is not supported. Only webp, png, and glb are supported.`);
                setStatus("Logo file must be webp, png, or glb.", "error");
                return;
            }
            setLogoInputFile(file);
        });

        logoInput.addEventListener("change", () => {
            const file = logoInput.files[0];
            if (file) {
                const ext = file.name.split('.').pop().toLowerCase();
                // هنتأكد إن ملف اللوجو المختار امتداده صح
                if (!['webp', 'png', 'glb'].includes(ext)) {
                    alert(`Warning: The file "${file.name}" is not supported. Only webp, png, and glb are supported.`);
                    setStatus("Logo file must be webp, png, or glb.", "error");
                    logoInput.value = "";
                    return;
                }
                setLogoPreview(file);
            }
        });
    }

    if (primaryDropzone && primaryInput) {
        primaryDropzone.addEventListener("dragover", (event) => {
            event.preventDefault();
            primaryDropzone.classList.add("is-dragover");
        });

        primaryDropzone.addEventListener("dragleave", () => {
            primaryDropzone.classList.remove("is-dragover");
        });

        primaryDropzone.addEventListener("drop", (event) => {
            event.preventDefault();
            primaryDropzone.classList.remove("is-dragover");
            const file = event.dataTransfer.files[0];
            if (!file) return;
            const ext = file.name.split('.').pop().toLowerCase();
            // هنتأكد إن ملف الصورة الرئيسية اللي اتسحب امتداده صح
            if (!['webp', 'png', 'glb'].includes(ext)) {
                alert(`Warning: The file "${file.name}" is not supported. Only webp, png, and glb are supported.`);
                setStatus("Primary file must be webp, png, or glb.", "error");
                return;
            }
            setPrimaryInputFile(file);
        });

        primaryInput.addEventListener("change", () => {
            const file = primaryInput.files[0];
            if (file) {
                const ext = file.name.split('.').pop().toLowerCase();
                // هنتأكد إن ملف الصورة الرئيسية المختار امتداده صح
                if (!['webp', 'png', 'glb'].includes(ext)) {
                    alert(`Warning: The file "${file.name}" is not supported. Only webp, png, and glb are supported.`);
                    setStatus("Primary file must be webp, png, or glb.", "error");
                    primaryInput.value = "";
                    return;
                }
                setPrimaryPreview(file);
            }
        });
    }

    if (input) {
        input.addEventListener("change", () => uploadFiles(input.files));
    }

    bindGalleryCards();
});

function getCsrfToken() {
    const input = document.querySelector("input[name='csrfmiddlewaretoken']");
    if (input && input.value) {
        return input.value;
    }
    return getCookie("csrftoken");
}

function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split(";") : [];
    for (const cookie of cookies) {
        const trimmed = cookie.trim();
        if (trimmed.startsWith(`${name}=`)) {
            return decodeURIComponent(trimmed.substring(name.length + 1));
        }
    }
    return "";
}

function escapeHtml(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
