document.addEventListener("DOMContentLoaded", () => {
    document.documentElement.classList.add("is-ready");

    const specsModal = document.querySelector("[data-specs-modal]");
    const specsProduct = document.querySelector("[data-specs-modal-product]");
    const specsMessage = document.querySelector("[data-specs-message]");
    const specsCloseButton = document.querySelector("[data-specs-close]");
    const specsButtons = document.querySelectorAll("[data-specs-product]");
    const specsNameInput = document.getElementById("specs-name");

    const openSpecsModal = (productName) => {
        if (!specsModal) {
            return;
        }

        const product = productName || "VANCOM";
        if (specsProduct) {
            specsProduct.textContent = product;
        }

        if (specsMessage) {
            specsMessage.value = `GET SPECS request for ${product}`;
        }

        specsModal.classList.add("is-open");
        specsModal.setAttribute("aria-hidden", "false");

        if (specsNameInput) {
            specsNameInput.focus();
        }
    };

    const closeSpecsModal = () => {
        if (!specsModal) {
            return;
        }

        specsModal.classList.remove("is-open");
        specsModal.setAttribute("aria-hidden", "true");
    };

    specsButtons.forEach((button) => {
        button.addEventListener("click", () => {
            openSpecsModal(button.dataset.specsProduct);
        });
    });

    if (specsCloseButton) {
        specsCloseButton.addEventListener("click", closeSpecsModal);
    }

    if (specsModal) {
        specsModal.addEventListener("click", (event) => {
            if (event.target === specsModal) {
                closeSpecsModal();
            }
        });
    }

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && specsModal && specsModal.classList.contains("is-open")) {
            closeSpecsModal();
        }
    });

    const visualDataScript = document.getElementById("service-visual-data");
    if (!visualDataScript) {
        return;
    }

    let visuals = [];
    try {
        visuals = JSON.parse(visualDataScript.textContent);
    } catch (error) {
        return;
    }

    if (!Array.isArray(visuals) || visuals.length === 0) {
        return;
    }

    const caption = document.querySelector("[data-service-caption]");
    const visualImage = document.querySelector("[data-service-image]");
    const drone = document.querySelector(".service-vulture-drone");
    const previousButton = document.querySelector(".service-visual-arrow-prev");
    const nextButton = document.querySelector(".service-visual-arrow-next");

    let activeIndex = 0;

    const renderVisual = () => {
        const item = visuals[activeIndex];

        if (caption) {
            caption.textContent = item.caption || item.title || "";
        }

        if (visualImage && item.image) {
            const staticPrefix = visualImage.dataset.staticPrefix || "/static/";
            visualImage.src = `${staticPrefix}${item.image}`;
            visualImage.alt = item.title || item.caption || "VULTURE UAV";
            visualImage.dataset.variant = String(activeIndex);
        }

        if (drone) {
            drone.dataset.variant = String(activeIndex);
        }
    };

    const moveVisual = (direction) => {
        activeIndex = (activeIndex + direction + visuals.length) % visuals.length;
        renderVisual();
    };

    if (previousButton) {
        previousButton.addEventListener("click", () => moveVisual(-1));
    }

    if (nextButton) {
        nextButton.addEventListener("click", () => moveVisual(1));
    }

    renderVisual();
});
