document.addEventListener("DOMContentLoaded", () => {
    document.documentElement.classList.add("is-ready");

    // Country Selector Functionality with All Countries
    const countrySelector = document.querySelector(".country-selector");
    if (countrySelector) {
        // قائمة كاملة بجميع دول العالم مع أكوادها
        const countries = [
            { code: "+93", name: "Afghanistan", flag: "🇦🇫" },
            { code: "+355", name: "Albania", flag: "🇦🇱" },
            { code: "+213", name: "Algeria", flag: "🇩🇿" },
            { code: "+376", name: "Andorra", flag: "🇦🇩" },
            { code: "+244", name: "Angola", flag: "🇦🇴" },
            { code: "+54", name: "Argentina", flag: "🇦🇷" },
            { code: "+374", name: "Armenia", flag: "🇦🇲" },
            { code: "+61", name: "Australia", flag: "🇦🇺" },
            { code: "+43", name: "Austria", flag: "🇦🇹" },
            { code: "+994", name: "Azerbaijan", flag: "🇦🇿" },
            { code: "+973", name: "Bahrain", flag: "🇧🇭" },
            { code: "+880", name: "Bangladesh", flag: "🇧🇩" },
            { code: "+375", name: "Belarus", flag: "🇧🇾" },
            { code: "+32", name: "Belgium", flag: "🇧🇪" },
            { code: "+501", name: "Belize", flag: "🇧🇿" },
            { code: "+229", name: "Benin", flag: "🇧🇯" },
            { code: "+975", name: "Bhutan", flag: "🇧🇹" },
            { code: "+591", name: "Bolivia", flag: "🇧🇴" },
            { code: "+387", name: "Bosnia", flag: "🇧🇦" },
            { code: "+267", name: "Botswana", flag: "🇧🇼" },
            { code: "+55", name: "Brazil", flag: "🇧🇷" },
            { code: "+673", name: "Brunei", flag: "🇧🇳" },
            { code: "+359", name: "Bulgaria", flag: "🇧🇬" },
            { code: "+226", name: "Burkina Faso", flag: "🇧🇫" },
            { code: "+257", name: "Burundi", flag: "🇧🇮" },
            { code: "+855", name: "Cambodia", flag: "🇰🇭" },
            { code: "+237", name: "Cameroon", flag: "🇨🇲" },
            { code: "+1", name: "Canada", flag: "🇨🇦" },
            { code: "+238", name: "Cape Verde", flag: "🇨🇻" },
            { code: "+236", name: "Central African Republic", flag: "🇨🇫" },
            { code: "+235", name: "Chad", flag: "🇹🇩" },
            { code: "+56", name: "Chile", flag: "🇨🇱" },
            { code: "+86", name: "China", flag: "🇨🇳" },
            { code: "+57", name: "Colombia", flag: "🇨🇴" },
            { code: "+269", name: "Comoros", flag: "🇰🇲" },
            { code: "+242", name: "Congo", flag: "🇨🇬" },
            { code: "+506", name: "Costa Rica", flag: "🇨🇷" },
            { code: "+385", name: "Croatia", flag: "🇭🇷" },
            { code: "+53", name: "Cuba", flag: "🇨🇺" },
            { code: "+357", name: "Cyprus", flag: "🇨🇾" },
            { code: "+420", name: "Czech Republic", flag: "🇨🇿" },
            { code: "+45", name: "Denmark", flag: "🇩🇰" },
            { code: "+253", name: "Djibouti", flag: "🇩🇯" },
            { code: "+593", name: "Ecuador", flag: "🇪🇨" },
            { code: "+20", name: "Egypt", flag: "🇪🇬" },
            { code: "+503", name: "El Salvador", flag: "🇸🇻" },
            { code: "+240", name: "Equatorial Guinea", flag: "🇬🇶" },
            { code: "+291", name: "Eritrea", flag: "🇪🇷" },
            { code: "+372", name: "Estonia", flag: "🇪🇪" },
            { code: "+251", name: "Ethiopia", flag: "🇪🇹" },
            { code: "+679", name: "Fiji", flag: "🇫🇯" },
            { code: "+358", name: "Finland", flag: "🇫🇮" },
            { code: "+33", name: "France", flag: "🇫🇷" },
            { code: "+241", name: "Gabon", flag: "🇬🇦" },
            { code: "+220", name: "Gambia", flag: "🇬🇲" },
            { code: "+995", name: "Georgia", flag: "🇬🇪" },
            { code: "+49", name: "Germany", flag: "🇩🇪" },
            { code: "+233", name: "Ghana", flag: "🇬🇭" },
            { code: "+30", name: "Greece", flag: "🇬🇷" },
            { code: "+502", name: "Guatemala", flag: "🇬🇹" },
            { code: "+224", name: "Guinea", flag: "🇬🇳" },
            { code: "+245", name: "Guinea-Bissau", flag: "🇬🇼" },
            { code: "+592", name: "Guyana", flag: "🇬🇾" },
            { code: "+509", name: "Haiti", flag: "🇭🇹" },
            { code: "+504", name: "Honduras", flag: "🇭🇳" },
            { code: "+852", name: "Hong Kong", flag: "🇭🇰" },
            { code: "+36", name: "Hungary", flag: "🇭🇺" },
            { code: "+354", name: "Iceland", flag: "🇮🇸" },
            { code: "+91", name: "India", flag: "🇮🇳" },
            { code: "+62", name: "Indonesia", flag: "🇮🇩" },
            { code: "+98", name: "Iran", flag: "🇮🇷" },
            { code: "+964", name: "Iraq", flag: "🇮🇶" },
            { code: "+353", name: "Ireland", flag: "🇮🇪" },
            { code: "+972", name: "Israel", flag: "🇮🇱" },
            { code: "+39", name: "Italy", flag: "🇮🇹" },
            { code: "+225", name: "Ivory Coast", flag: "🇨🇮" },
            { code: "+81", name: "Japan", flag: "🇯🇵" },
            { code: "+962", name: "Jordan", flag: "🇯🇴" },
            { code: "+7", name: "Kazakhstan", flag: "🇰🇿" },
            { code: "+254", name: "Kenya", flag: "🇰🇪" },
            { code: "+965", name: "Kuwait", flag: "🇰🇼" },
            { code: "+996", name: "Kyrgyzstan", flag: "🇰🇬" },
            { code: "+856", name: "Laos", flag: "🇱🇦" },
            { code: "+371", name: "Latvia", flag: "🇱🇻" },
            { code: "+961", name: "Lebanon", flag: "🇱🇧" },
            { code: "+266", name: "Lesotho", flag: "🇱🇸" },
            { code: "+231", name: "Liberia", flag: "🇱🇷" },
            { code: "+218", name: "Libya", flag: "🇱🇾" },
            { code: "+423", name: "Liechtenstein", flag: "🇱🇮" },
            { code: "+370", name: "Lithuania", flag: "🇱🇹" },
            { code: "+352", name: "Luxembourg", flag: "🇱🇺" },
            { code: "+261", name: "Madagascar", flag: "🇲🇬" },
            { code: "+265", name: "Malawi", flag: "🇲🇼" },
            { code: "+60", name: "Malaysia", flag: "🇲🇾" },
            { code: "+960", name: "Maldives", flag: "🇲🇻" },
            { code: "+223", name: "Mali", flag: "🇲🇱" },
            { code: "+356", name: "Malta", flag: "🇲🇹" },
            { code: "+222", name: "Mauritania", flag: "🇲🇷" },
            { code: "+230", name: "Mauritius", flag: "🇲🇺" },
            { code: "+52", name: "Mexico", flag: "🇲🇽" },
            { code: "+373", name: "Moldova", flag: "🇲🇩" },
            { code: "+377", name: "Monaco", flag: "🇲🇨" },
            { code: "+976", name: "Mongolia", flag: "🇲🇳" },
            { code: "+382", name: "Montenegro", flag: "🇲🇪" },
            { code: "+212", name: "Morocco", flag: "🇲🇦" },
            { code: "+258", name: "Mozambique", flag: "🇲🇿" },
            { code: "+95", name: "Myanmar", flag: "🇲🇲" },
            { code: "+264", name: "Namibia", flag: "🇳🇦" },
            { code: "+977", name: "Nepal", flag: "🇳🇵" },
            { code: "+31", name: "Netherlands", flag: "🇳🇱" },
            { code: "+64", name: "New Zealand", flag: "🇳🇿" },
            { code: "+505", name: "Nicaragua", flag: "🇳🇮" },
            { code: "+227", name: "Niger", flag: "🇳🇪" },
            { code: "+234", name: "Nigeria", flag: "🇳🇬" },
            { code: "+850", name: "North Korea", flag: "🇰🇵" },
            { code: "+389", name: "North Macedonia", flag: "🇲🇰" },
            { code: "+47", name: "Norway", flag: "🇳🇴" },
            { code: "+968", name: "Oman", flag: "🇴🇲" },
            { code: "+92", name: "Pakistan", flag: "🇵🇰" },
            { code: "+970", name: "Palestine", flag: "🇵🇸" },
            { code: "+507", name: "Panama", flag: "🇵🇦" },
            { code: "+675", name: "Papua New Guinea", flag: "🇵🇬" },
            { code: "+595", name: "Paraguay", flag: "🇵🇾" },
            { code: "+51", name: "Peru", flag: "🇵🇪" },
            { code: "+63", name: "Philippines", flag: "🇵🇭" },
            { code: "+48", name: "Poland", flag: "🇵🇱" },
            { code: "+351", name: "Portugal", flag: "🇵🇹" },
            { code: "+974", name: "Qatar", flag: "🇶🇦" },
            { code: "+40", name: "Romania", flag: "🇷🇴" },
            { code: "+7", name: "Russia", flag: "🇷🇺" },
            { code: "+250", name: "Rwanda", flag: "🇷🇼" },
            { code: "+966", name: "Saudi Arabia", flag: "🇸🇦" },
            { code: "+221", name: "Senegal", flag: "🇸🇳" },
            { code: "+381", name: "Serbia", flag: "🇷🇸" },
            { code: "+248", name: "Seychelles", flag: "🇸🇨" },
            { code: "+232", name: "Sierra Leone", flag: "🇸🇱" },
            { code: "+65", name: "Singapore", flag: "🇸🇬" },
            { code: "+421", name: "Slovakia", flag: "🇸🇰" },
            { code: "+386", name: "Slovenia", flag: "🇸🇮" },
            { code: "+252", name: "Somalia", flag: "🇸🇴" },
            { code: "+27", name: "South Africa", flag: "🇿🇦" },
            { code: "+82", name: "South Korea", flag: "🇰🇷" },
            { code: "+211", name: "South Sudan", flag: "🇸🇸" },
            { code: "+34", name: "Spain", flag: "🇪🇸" },
            { code: "+94", name: "Sri Lanka", flag: "🇱🇰" },
            { code: "+249", name: "Sudan", flag: "🇸🇩" },
            { code: "+597", name: "Suriname", flag: "🇸🇷" },
            { code: "+46", name: "Sweden", flag: "🇸🇪" },
            { code: "+41", name: "Switzerland", flag: "🇨🇭" },
            { code: "+963", name: "Syria", flag: "🇸🇾" },
            { code: "+886", name: "Taiwan", flag: "🇹🇼" },
            { code: "+992", name: "Tajikistan", flag: "🇹🇯" },
            { code: "+255", name: "Tanzania", flag: "🇹🇿" },
            { code: "+66", name: "Thailand", flag: "🇹🇭" },
            { code: "+228", name: "Togo", flag: "🇹🇬" },
            { code: "+216", name: "Tunisia", flag: "🇹🇳" },
            { code: "+90", name: "Turkey", flag: "🇹🇷" },
            { code: "+993", name: "Turkmenistan", flag: "🇹🇲" },
            { code: "+256", name: "Uganda", flag: "🇺🇬" },
            { code: "+380", name: "Ukraine", flag: "🇺🇦" },
            { code: "+971", name: "United Arab Emirates", flag: "🇦🇪" },
            { code: "+44", name: "United Kingdom", flag: "🇬🇧" },
            { code: "+1", name: "United States", flag: "🇺🇸" },
            { code: "+598", name: "Uruguay", flag: "🇺🇾" },
            { code: "+998", name: "Uzbekistan", flag: "🇺🇿" },
            { code: "+678", name: "Vanuatu", flag: "🇻🇺" },
            { code: "+58", name: "Venezuela", flag: "🇻🇪" },
            { code: "+84", name: "Vietnam", flag: "🇻🇳" },
            { code: "+967", name: "Yemen", flag: "🇾🇪" },
            { code: "+260", name: "Zambia", flag: "🇿🇲" },
            { code: "+263", name: "Zimbabwe", flag: "🇿🇼" }
        ];

        // ترتيب الدول أبجدياً
        countries.sort((a, b) => a.name.localeCompare(b.name));

        // الدولة الافتراضية (مصر)
        let currentCountry = countries.find(c => c.code === "+20");
        let dropdown = null;
        let searchInput = null;
        let filteredCountries = [...countries];

        const updateCountryDisplay = (country) => {
            currentCountry = country;
            const codeElement = countrySelector.querySelector("span:first-of-type");
            
            if (codeElement) {
                codeElement.textContent = country.code;
            }
        };

        const createCountryOption = (country) => {
            const option = document.createElement("div");
            option.className = "country-option";
            option.dataset.country = country.name;
            option.innerHTML = `
                <span class="country-flag">${country.flag}</span>
                <span class="country-code">${country.code}</span>
                <span class="country-name">${country.name}</span>
            `;

            option.addEventListener("click", () => {
                updateCountryDisplay(country);
                closeDropdown();
            });

            return option;
        };

        const filterCountries = (searchTerm) => {
            const term = searchTerm.toLowerCase().trim();
            
            if (!term) {
                return [...countries];
            }

            return countries.filter(country => 
                country.name.toLowerCase().includes(term) || 
                country.code.includes(term)
            );
        };

        const renderCountryList = (countriesToRender) => {
            const listContainer = dropdown.querySelector(".country-list");
            listContainer.innerHTML = "";

            if (countriesToRender.length === 0) {
                const noResults = document.createElement("div");
                noResults.className = "no-results";
                noResults.textContent = "No countries found";
                listContainer.appendChild(noResults);
                return;
            }

            countriesToRender.forEach(country => {
                listContainer.appendChild(createCountryOption(country));
            });
        };

        const createDropdown = () => {
            dropdown = document.createElement("div");
            dropdown.className = "country-dropdown";

            // حقل البحث
            const searchContainer = document.createElement("div");
            searchContainer.className = "country-search-container";
            
            searchInput = document.createElement("input");
            searchInput.type = "text";
            searchInput.className = "country-search-input";
            searchInput.placeholder = "Search country...";
            searchInput.autocomplete = "off";
            
            searchInput.addEventListener("input", (e) => {
                filteredCountries = filterCountries(e.target.value);
                renderCountryList(filteredCountries);
            });

            searchInput.addEventListener("click", (e) => {
                e.stopPropagation();
            });

            searchContainer.appendChild(searchInput);

            // قائمة الدول
            const listContainer = document.createElement("div");
            listContainer.className = "country-list";

            dropdown.appendChild(searchContainer);
            dropdown.appendChild(listContainer);

            renderCountryList(countries);

            return dropdown;
        };

        const openDropdown = () => {
            if (!dropdown) {
                dropdown = createDropdown();
            }
            
            const container = countrySelector.parentElement;
            container.style.position = "relative";
            container.appendChild(dropdown);

            // Focus on search input
            setTimeout(() => {
                if (searchInput) {
                    searchInput.focus();
                }
            }, 50);
        };

        const closeDropdown = () => {
            if (dropdown && dropdown.parentElement) {
                dropdown.parentElement.removeChild(dropdown);
                dropdown = null;
                searchInput = null;
                filteredCountries = [...countries];
            }
        };

        countrySelector.addEventListener("click", (e) => {
            e.stopPropagation();
            if (dropdown) {
                closeDropdown();
            } else {
                openDropdown();
            }
        });

        document.addEventListener("click", (e) => {
            if (dropdown && !countrySelector.contains(e.target) && !dropdown.contains(e.target)) {
                closeDropdown();
            }
        });

        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape" && dropdown) {
                closeDropdown();
            }
        });
    }

    const specsModal = document.querySelector("[data-specs-modal]");
    const specsProduct = document.querySelector("[data-specs-modal-product]");
    const specsMessage = document.querySelector("[data-specs-message]");
    const specsSolutionSlug = document.querySelector("[data-specs-solution-slug]");
    const specsCloseButton = document.querySelector("[data-specs-close]");
    const specsButtons = document.querySelectorAll("[data-specs-product]");
    const specsNameInput = document.getElementById("specs-name");

    const openSpecsModal = (productName, productSlug) => {
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

        if (specsSolutionSlug) {
            specsSolutionSlug.value = productSlug || "";
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
            openSpecsModal(button.dataset.specsProduct, button.dataset.specsSlug);
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
    const visualModel = document.querySelector("[data-service-model]");
    const drone = document.querySelector(".service-vulture-drone");
    const previousButton = document.querySelector(".service-visual-arrow-prev");
    const nextButton = document.querySelector(".service-visual-arrow-next");

    let activeIndex = 0;
    let isTransitioning = false;

    const renderVisual = (oldIndex = null) => {
        const item = visuals[activeIndex];

        if (caption) {
            caption.textContent = item.caption || item.title || "";
        }

        if (item.image) {
            // هنتحقق لو كان الملف من نوع glb
            const isGlb = item.image.split('?')[0].split('#')[0].toLowerCase().endsWith('.glb');

            if (visualImage && visualModel) {
                if (isGlb) {
                    // لو الملف glb هنظهر الـ model-viewer ونخفي الـ image
                    visualImage.style.display = "none";
                    visualModel.style.display = "block";
                    visualModel.src = item.image;
                    visualModel.alt = item.title || item.caption || "3D Model";
                } else {
                    // لو صورة عادية هنظهر الـ image ونخفي الـ model-viewer
                    visualModel.style.display = "none";
                    visualImage.style.display = "block";

                    if (oldIndex !== null && oldIndex !== activeIndex) {
                        isTransitioning = true;
                        visualImage.classList.add("is-fading");
                        setTimeout(() => {
                            visualImage.src = item.image;
                            visualImage.alt = item.title || item.caption || "VULTURE UAV";
                            visualImage.dataset.variant = String(activeIndex);
                            
                            if (drone) {
                                drone.dataset.variant = String(activeIndex);
                            }

                            // Force reflow
                            visualImage.offsetHeight;
                            visualImage.classList.remove("is-fading");
                            isTransitioning = false;
                        }, 250);
                    } else {
                        visualImage.src = item.image;
                        visualImage.alt = item.title || item.caption || "VULTURE UAV";
                        visualImage.dataset.variant = String(activeIndex);
                        if (drone) {
                            drone.dataset.variant = String(activeIndex);
                        }
                    }
                }
            } else if (visualImage) {
                visualImage.src = item.image;
                visualImage.alt = item.title || item.caption || "VULTURE UAV";
                visualImage.dataset.variant = String(activeIndex);
                if (drone) {
                    drone.dataset.variant = String(activeIndex);
                }
            }
        } else {
            if (drone) {
                drone.dataset.variant = String(activeIndex);
            }
        }
    };

    const moveVisual = (direction) => {
        if (isTransitioning) return;
        const oldIndex = activeIndex;
        activeIndex = (activeIndex + direction + visuals.length) % visuals.length;
        renderVisual(oldIndex);
    };

    if (previousButton) {
        previousButton.addEventListener("click", () => moveVisual(-1));
    }

    if (nextButton) {
        nextButton.addEventListener("click", () => moveVisual(1));
    }

    renderVisual();
});
