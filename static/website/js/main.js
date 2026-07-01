document.addEventListener("DOMContentLoaded", () => {
    document.documentElement.classList.add("is-ready");

    // Country Selector with Flag Icons - Complete List
    const countrySelector = document.querySelector(".contact-phone-wrapper .country-selector");
    if (countrySelector) {
        const allCountries = [
            {code:"+93",name:"Afghanistan",iso:"af"},{code:"+355",name:"Albania",iso:"al"},
            {code:"+213",name:"Algeria",iso:"dz"},{code:"+376",name:"Andorra",iso:"ad"},
            {code:"+244",name:"Angola",iso:"ao"},{code:"+54",name:"Argentina",iso:"ar"},
            {code:"+374",name:"Armenia",iso:"am"},{code:"+61",name:"Australia",iso:"au"},
            {code:"+43",name:"Austria",iso:"at"},{code:"+994",name:"Azerbaijan",iso:"az"},
            {code:"+973",name:"Bahrain",iso:"bh"},{code:"+880",name:"Bangladesh",iso:"bd"},
            {code:"+375",name:"Belarus",iso:"by"},{code:"+32",name:"Belgium",iso:"be"},
            {code:"+501",name:"Belize",iso:"bz"},{code:"+229",name:"Benin",iso:"bj"},
            {code:"+975",name:"Bhutan",iso:"bt"},{code:"+591",name:"Bolivia",iso:"bo"},
            {code:"+387",name:"Bosnia",iso:"ba"},{code:"+267",name:"Botswana",iso:"bw"},
            {code:"+55",name:"Brazil",iso:"br"},{code:"+673",name:"Brunei",iso:"bn"},
            {code:"+359",name:"Bulgaria",iso:"bg"},{code:"+226",name:"Burkina Faso",iso:"bf"},
            {code:"+257",name:"Burundi",iso:"bi"},{code:"+855",name:"Cambodia",iso:"kh"},
            {code:"+237",name:"Cameroon",iso:"cm"},{code:"+1",name:"Canada",iso:"ca"},
            {code:"+238",name:"Cape Verde",iso:"cv"},{code:"+236",name:"Central African Rep",iso:"cf"},
            {code:"+235",name:"Chad",iso:"td"},{code:"+56",name:"Chile",iso:"cl"},
            {code:"+86",name:"China",iso:"cn"},{code:"+57",name:"Colombia",iso:"co"},
            {code:"+269",name:"Comoros",iso:"km"},{code:"+242",name:"Congo",iso:"cg"},
            {code:"+506",name:"Costa Rica",iso:"cr"},{code:"+385",name:"Croatia",iso:"hr"},
            {code:"+53",name:"Cuba",iso:"cu"},{code:"+357",name:"Cyprus",iso:"cy"},
            {code:"+420",name:"Czech Republic",iso:"cz"},{code:"+45",name:"Denmark",iso:"dk"},
            {code:"+253",name:"Djibouti",iso:"dj"},{code:"+593",name:"Ecuador",iso:"ec"},
            {code:"+20",name:"Egypt",iso:"eg"},{code:"+503",name:"El Salvador",iso:"sv"},
            {code:"+240",name:"Equatorial Guinea",iso:"gq"},{code:"+291",name:"Eritrea",iso:"er"},
            {code:"+372",name:"Estonia",iso:"ee"},{code:"+251",name:"Ethiopia",iso:"et"},
            {code:"+679",name:"Fiji",iso:"fj"},{code:"+358",name:"Finland",iso:"fi"},
            {code:"+33",name:"France",iso:"fr"},{code:"+241",name:"Gabon",iso:"ga"},
            {code:"+220",name:"Gambia",iso:"gm"},{code:"+995",name:"Georgia",iso:"ge"},
            {code:"+49",name:"Germany",iso:"de"},{code:"+233",name:"Ghana",iso:"gh"},
            {code:"+30",name:"Greece",iso:"gr"},{code:"+502",name:"Guatemala",iso:"gt"},
            {code:"+224",name:"Guinea",iso:"gn"},{code:"+245",name:"Guinea-Bissau",iso:"gw"},
            {code:"+592",name:"Guyana",iso:"gy"},{code:"+509",name:"Haiti",iso:"ht"},
            {code:"+504",name:"Honduras",iso:"hn"},{code:"+852",name:"Hong Kong",iso:"hk"},
            {code:"+36",name:"Hungary",iso:"hu"},{code:"+354",name:"Iceland",iso:"is"},
            {code:"+91",name:"India",iso:"in"},{code:"+62",name:"Indonesia",iso:"id"},
            {code:"+98",name:"Iran",iso:"ir"},{code:"+964",name:"Iraq",iso:"iq"},
            {code:"+353",name:"Ireland",iso:"ie"},{code:"+972",name:"Israel",iso:"il"},
            {code:"+39",name:"Italy",iso:"it"},{code:"+225",name:"Ivory Coast",iso:"ci"},
            {code:"+81",name:"Japan",iso:"jp"},{code:"+962",name:"Jordan",iso:"jo"},
            {code:"+7",name:"Kazakhstan",iso:"kz"},{code:"+254",name:"Kenya",iso:"ke"},
            {code:"+965",name:"Kuwait",iso:"kw"},{code:"+996",name:"Kyrgyzstan",iso:"kg"},
            {code:"+856",name:"Laos",iso:"la"},{code:"+371",name:"Latvia",iso:"lv"},
            {code:"+961",name:"Lebanon",iso:"lb"},{code:"+266",name:"Lesotho",iso:"ls"},
            {code:"+231",name:"Liberia",iso:"lr"},{code:"+218",name:"Libya",iso:"ly"},
            {code:"+423",name:"Liechtenstein",iso:"li"},{code:"+370",name:"Lithuania",iso:"lt"},
            {code:"+352",name:"Luxembourg",iso:"lu"},{code:"+261",name:"Madagascar",iso:"mg"},
            {code:"+265",name:"Malawi",iso:"mw"},{code:"+60",name:"Malaysia",iso:"my"},
            {code:"+960",name:"Maldives",iso:"mv"},{code:"+223",name:"Mali",iso:"ml"},
            {code:"+356",name:"Malta",iso:"mt"},{code:"+222",name:"Mauritania",iso:"mr"},
            {code:"+230",name:"Mauritius",iso:"mu"},{code:"+52",name:"Mexico",iso:"mx"},
            {code:"+373",name:"Moldova",iso:"md"},{code:"+377",name:"Monaco",iso:"mc"},
            {code:"+976",name:"Mongolia",iso:"mn"},{code:"+382",name:"Montenegro",iso:"me"},
            {code:"+212",name:"Morocco",iso:"ma"},{code:"+258",name:"Mozambique",iso:"mz"},
            {code:"+95",name:"Myanmar",iso:"mm"},{code:"+264",name:"Namibia",iso:"na"},
            {code:"+977",name:"Nepal",iso:"np"},{code:"+31",name:"Netherlands",iso:"nl"},
            {code:"+64",name:"New Zealand",iso:"nz"},{code:"+505",name:"Nicaragua",iso:"ni"},
            {code:"+227",name:"Niger",iso:"ne"},{code:"+234",name:"Nigeria",iso:"ng"},
            {code:"+850",name:"North Korea",iso:"kp"},{code:"+389",name:"North Macedonia",iso:"mk"},
            {code:"+47",name:"Norway",iso:"no"},{code:"+968",name:"Oman",iso:"om"},
            {code:"+92",name:"Pakistan",iso:"pk"},{code:"+970",name:"Palestine",iso:"ps"},
            {code:"+507",name:"Panama",iso:"pa"},{code:"+675",name:"Papua New Guinea",iso:"pg"},
            {code:"+595",name:"Paraguay",iso:"py"},{code:"+51",name:"Peru",iso:"pe"},
            {code:"+63",name:"Philippines",iso:"ph"},{code:"+48",name:"Poland",iso:"pl"},
            {code:"+351",name:"Portugal",iso:"pt"},{code:"+974",name:"Qatar",iso:"qa"},
            {code:"+40",name:"Romania",iso:"ro"},{code:"+7",name:"Russia",iso:"ru"},
            {code:"+250",name:"Rwanda",iso:"rw"},{code:"+966",name:"Saudi Arabia",iso:"sa"},
            {code:"+221",name:"Senegal",iso:"sn"},{code:"+381",name:"Serbia",iso:"rs"},
            {code:"+248",name:"Seychelles",iso:"sc"},{code:"+232",name:"Sierra Leone",iso:"sl"},
            {code:"+65",name:"Singapore",iso:"sg"},{code:"+421",name:"Slovakia",iso:"sk"},
            {code:"+386",name:"Slovenia",iso:"si"},{code:"+252",name:"Somalia",iso:"so"},
            {code:"+27",name:"South Africa",iso:"za"},{code:"+82",name:"South Korea",iso:"kr"},
            {code:"+211",name:"South Sudan",iso:"ss"},{code:"+34",name:"Spain",iso:"es"},
            {code:"+94",name:"Sri Lanka",iso:"lk"},{code:"+249",name:"Sudan",iso:"sd"},
            {code:"+597",name:"Suriname",iso:"sr"},{code:"+46",name:"Sweden",iso:"se"},
            {code:"+41",name:"Switzerland",iso:"ch"},{code:"+963",name:"Syria",iso:"sy"},
            {code:"+886",name:"Taiwan",iso:"tw"},{code:"+992",name:"Tajikistan",iso:"tj"},
            {code:"+255",name:"Tanzania",iso:"tz"},{code:"+66",name:"Thailand",iso:"th"},
            {code:"+228",name:"Togo",iso:"tg"},{code:"+216",name:"Tunisia",iso:"tn"},
            {code:"+90",name:"Turkey",iso:"tr"},{code:"+993",name:"Turkmenistan",iso:"tm"},
            {code:"+256",name:"Uganda",iso:"ug"},{code:"+380",name:"Ukraine",iso:"ua"},
            {code:"+971",name:"United Arab Emirates",iso:"ae"},{code:"+44",name:"United Kingdom",iso:"gb"},
            {code:"+1",name:"United States",iso:"us"},{code:"+598",name:"Uruguay",iso:"uy"},
            {code:"+998",name:"Uzbekistan",iso:"uz"},{code:"+678",name:"Vanuatu",iso:"vu"},
            {code:"+58",name:"Venezuela",iso:"ve"},{code:"+84",name:"Vietnam",iso:"vn"},
            {code:"+967",name:"Yemen",iso:"ye"},{code:"+260",name:"Zambia",iso:"zm"},
            {code:"+263",name:"Zimbabwe",iso:"zw"}
        ];

        allCountries.sort((a,b) => a.name.localeCompare(b.name));
        let currentCountry = allCountries.find(c => c.code === "+20") || allCountries[0];
        let dropdown = null, searchInput = null;

        const updateDisplay = (country) => {
            currentCountry = country;
            
            // تحديث العلم
            const flagSpan = countrySelector.querySelector(".fi");
            if (flagSpan) {
                flagSpan.className = `fi fi-${country.iso}`;
            }
            
            // تحديث الكود
            const codeSpan = countrySelector.querySelector("span:nth-of-type(2)");
            if (codeSpan) {
                codeSpan.textContent = country.code;
            }
            
            // حفظ كود الدولة في data attribute
            countrySelector.setAttribute('data-country-code', country.code);
        };

        const createOption = (country) => {
            const opt = document.createElement("div");
            opt.className = "country-option";
            opt.innerHTML = `<span class="fi fi-${country.iso}"></span><span class="country-code">${country.code}</span><span class="country-name">${country.name}</span>`;
            opt.addEventListener("click", () => { 
                updateDisplay(country);
                closeDropdown(); 
            });
            return opt;
        };

        const filterCountries = (term) => {
            term = term.toLowerCase().trim();
            return term ? allCountries.filter(c => c.name.toLowerCase().includes(term) || c.code.includes(term)) : allCountries;
        };

        const renderList = (countries) => {
            const list = dropdown.querySelector(".country-list");
            list.innerHTML = countries.length ? "" : "<div class='no-results'>No countries found</div>";
            countries.forEach(c => list.appendChild(createOption(c)));
        };

        const openDropdown = () => {
            dropdown = document.createElement("div");
            dropdown.className = "country-dropdown is-open";
            
            const searchBox = document.createElement("div");
            searchBox.className = "country-search-container";
            searchInput = document.createElement("input");
            searchInput.type = "text";
            searchInput.className = "country-search-input";
            searchInput.placeholder = "Search country or code...";
            searchInput.autocomplete = "off";
            
            searchInput.addEventListener("input", (e) => {
                renderList(filterCountries(e.target.value));
            });
            
            searchInput.addEventListener("click", (e) => {
                e.stopPropagation();
            });
            
            searchInput.addEventListener("keydown", (e) => {
                e.stopPropagation();
            });
            
            searchBox.appendChild(searchInput);

            const list = document.createElement("div");
            list.className = "country-list";

            dropdown.appendChild(searchBox);
            dropdown.appendChild(list);
            countrySelector.parentElement.style.position = "relative";
            countrySelector.parentElement.appendChild(dropdown);
            renderList(allCountries);
            
            setTimeout(() => {
                if (searchInput) {
                    searchInput.focus();
                }
            }, 100);
        };

        const closeDropdown = () => {
            if (dropdown?.parentElement) {
                dropdown.parentElement.removeChild(dropdown);
                dropdown = searchInput = null;
            }
        };

        countrySelector.addEventListener("click", (e) => { 
            e.stopPropagation(); 
            dropdown ? closeDropdown() : openDropdown(); 
        });
        
        document.addEventListener("click", (e) => {
            if (dropdown && !dropdown.contains(e.target) && !countrySelector.contains(e.target)) {
                closeDropdown();
            }
        });
        
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape" && dropdown) {
                closeDropdown();
            }
        });
        
        // إضافة كود الدولة للرقم عند إرسال الفورم
        const contactForm = countrySelector.closest('form');
        if (contactForm) {
            contactForm.addEventListener('submit', (e) => {
                const phoneInput = contactForm.querySelector('input[name="phone"]');
                if (phoneInput && phoneInput.value) {
                    const countryCode = countrySelector.getAttribute('data-country-code') || '+20';
                    const phoneValue = phoneInput.value.trim();
                    
                    // إذا الرقم مش مبتدي بـ +، أضف كود الدولة
                    if (!phoneValue.startsWith('+')) {
                        phoneInput.value = countryCode + ' ' + phoneValue;
                    }
                }
            });
        }
    }

    const specsModal = document.querySelector("[data-specs-modal]");
    const specsProduct = document.querySelector("[data-specs-modal-product]");
    const specsMessage = document.querySelector("[data-specs-message]");
    const specsSolutionSlug = document.querySelector("[data-specs-solution-slug]");
    const specsCloseButton = document.querySelector("[data-specs-close]");
    const specsButtons = document.querySelectorAll("[data-specs-product]");
    const specsNameInput = document.getElementById("specs-name");

    const openSpecsModal = (productName, productSlug) => {
        if (!specsModal) return;
        const product = productName || "VANCOM";
        if (specsProduct) specsProduct.textContent = product;
        if (specsMessage) specsMessage.value = `GET SPECS request for ${product}`;
        if (specsSolutionSlug) specsSolutionSlug.value = productSlug || "";
        specsModal.classList.add("is-open");
        specsModal.setAttribute("aria-hidden", "false");
        if (specsNameInput) specsNameInput.focus();
    };

    const closeSpecsModal = () => {
        if (!specsModal) return;
        specsModal.classList.remove("is-open");
        specsModal.setAttribute("aria-hidden", "true");
        
        // Clean up open dropdown in the specs modal
        const openDropdown = specsModal.querySelector(".country-dropdown");
        if (openDropdown) {
            openDropdown.parentElement.removeChild(openDropdown);
        }
        specsModal.style.overflowY = "auto";
    };

    specsButtons.forEach(btn => btn.addEventListener("click", () => openSpecsModal(btn.dataset.specsProduct, btn.dataset.specsSlug)));
    if (specsCloseButton) specsCloseButton.addEventListener("click", closeSpecsModal);
    if (specsModal) specsModal.addEventListener("click", e => e.target === specsModal && closeSpecsModal());
    document.addEventListener("keydown", e => e.key === "Escape" && specsModal?.classList.contains("is-open") && closeSpecsModal());

    const visualDataScript = document.getElementById("service-visual-data");
    if (!visualDataScript) return;

    let visuals = [];
    try { visuals = JSON.parse(visualDataScript.textContent); } catch (error) { return; }
    if (!Array.isArray(visuals) || visuals.length === 0) return;

    const caption = document.querySelector("[data-service-caption]");
    const visualImage = document.querySelector("[data-service-image]");
    const visualModel = document.querySelector("[data-service-model]");
    const drone = document.querySelector(".service-vulture-drone");
    const previousButton = document.querySelector(".service-visual-arrow-prev");
    const nextButton = document.querySelector(".service-visual-arrow-next");

    let activeIndex = 0, isTransitioning = false;

    const renderVisual = (oldIndex = null) => {
        const item = visuals[activeIndex];
        if (caption) caption.textContent = item.caption || item.title || "";

        if (item.image) {
            const isGlb = item.image.split('?')[0].split('#')[0].toLowerCase().endsWith('.glb');

            if (visualImage && visualModel) {
                if (isGlb) {
                    visualImage.style.display = "none";
                    visualModel.style.display = "block";
                    visualModel.src = item.image;
                    visualModel.alt = item.title || item.caption || "3D Model";
                } else {
                    visualModel.style.display = "none";
                    visualImage.style.display = "block";

                    if (oldIndex !== null && oldIndex !== activeIndex) {
                        isTransitioning = true;
                        visualImage.classList.add("is-fading");
                        setTimeout(() => {
                            visualImage.src = item.image;
                            visualImage.alt = item.title || item.caption || "VULTURE UAV";
                            visualImage.dataset.variant = String(activeIndex);
                            if (drone) drone.dataset.variant = String(activeIndex);
                            visualImage.offsetHeight;
                            visualImage.classList.remove("is-fading");
                            isTransitioning = false;
                        }, 250);
                    } else {
                        visualImage.src = item.image;
                        visualImage.alt = item.title || item.caption || "VULTURE UAV";
                        visualImage.dataset.variant = String(activeIndex);
                        if (drone) drone.dataset.variant = String(activeIndex);
                    }
                }
            } else if (visualImage) {
                visualImage.src = item.image;
                visualImage.alt = item.title || item.caption || "VULTURE UAV";
                visualImage.dataset.variant = String(activeIndex);
                if (drone) drone.dataset.variant = String(activeIndex);
            }
        } else if (drone) drone.dataset.variant = String(activeIndex);
    };

    const moveVisual = (direction) => {
        if (isTransitioning) return;
        const oldIndex = activeIndex;
        activeIndex = (activeIndex + direction + visuals.length) % visuals.length;
        renderVisual(oldIndex);
    };

    if (previousButton) previousButton.addEventListener("click", () => moveVisual(-1));
    if (nextButton) nextButton.addEventListener("click", () => moveVisual(1));

    renderVisual();
});

// Modal Country Selector - نفس الوظيفة للمودال
document.addEventListener("DOMContentLoaded", () => {
    const modalCountrySelector = document.querySelector(".specs-modal-country-selector");
    if (modalCountrySelector) {
        const allCountries = [
            {code:"+93",name:"Afghanistan",iso:"af"},{code:"+355",name:"Albania",iso:"al"},
            {code:"+213",name:"Algeria",iso:"dz"},{code:"+376",name:"Andorra",iso:"ad"},
            {code:"+244",name:"Angola",iso:"ao"},{code:"+54",name:"Argentina",iso:"ar"},
            {code:"+374",name:"Armenia",iso:"am"},{code:"+61",name:"Australia",iso:"au"},
            {code:"+43",name:"Austria",iso:"at"},{code:"+994",name:"Azerbaijan",iso:"az"},
            {code:"+973",name:"Bahrain",iso:"bh"},{code:"+880",name:"Bangladesh",iso:"bd"},
            {code:"+375",name:"Belarus",iso:"by"},{code:"+32",name:"Belgium",iso:"be"},
            {code:"+501",name:"Belize",iso:"bz"},{code:"+229",name:"Benin",iso:"bj"},
            {code:"+975",name:"Bhutan",iso:"bt"},{code:"+591",name:"Bolivia",iso:"bo"},
            {code:"+387",name:"Bosnia",iso:"ba"},{code:"+267",name:"Botswana",iso:"bw"},
            {code:"+55",name:"Brazil",iso:"br"},{code:"+673",name:"Brunei",iso:"bn"},
            {code:"+359",name:"Bulgaria",iso:"bg"},{code:"+226",name:"Burkina Faso",iso:"bf"},
            {code:"+257",name:"Burundi",iso:"bi"},{code:"+855",name:"Cambodia",iso:"kh"},
            {code:"+237",name:"Cameroon",iso:"cm"},{code:"+1",name:"Canada",iso:"ca"},
            {code:"+238",name:"Cape Verde",iso:"cv"},{code:"+236",name:"Central African Rep",iso:"cf"},
            {code:"+235",name:"Chad",iso:"td"},{code:"+56",name:"Chile",iso:"cl"},
            {code:"+86",name:"China",iso:"cn"},{code:"+57",name:"Colombia",iso:"co"},
            {code:"+269",name:"Comoros",iso:"km"},{code:"+242",name:"Congo",iso:"cg"},
            {code:"+506",name:"Costa Rica",iso:"cr"},{code:"+385",name:"Croatia",iso:"hr"},
            {code:"+53",name:"Cuba",iso:"cu"},{code:"+357",name:"Cyprus",iso:"cy"},
            {code:"+420",name:"Czech Republic",iso:"cz"},{code:"+45",name:"Denmark",iso:"dk"},
            {code:"+253",name:"Djibouti",iso:"dj"},{code:"+593",name:"Ecuador",iso:"ec"},
            {code:"+20",name:"Egypt",iso:"eg"},{code:"+503",name:"El Salvador",iso:"sv"},
            {code:"+240",name:"Equatorial Guinea",iso:"gq"},{code:"+291",name:"Eritrea",iso:"er"},
            {code:"+372",name:"Estonia",iso:"ee"},{code:"+251",name:"Ethiopia",iso:"et"},
            {code:"+679",name:"Fiji",iso:"fj"},{code:"+358",name:"Finland",iso:"fi"},
            {code:"+33",name:"France",iso:"fr"},{code:"+241",name:"Gabon",iso:"ga"},
            {code:"+220",name:"Gambia",iso:"gm"},{code:"+995",name:"Georgia",iso:"ge"},
            {code:"+49",name:"Germany",iso:"de"},{code:"+233",name:"Ghana",iso:"gh"},
            {code:"+30",name:"Greece",iso:"gr"},{code:"+502",name:"Guatemala",iso:"gt"},
            {code:"+224",name:"Guinea",iso:"gn"},{code:"+245",name:"Guinea-Bissau",iso:"gw"},
            {code:"+592",name:"Guyana",iso:"gy"},{code:"+509",name:"Haiti",iso:"ht"},
            {code:"+504",name:"Honduras",iso:"hn"},{code:"+852",name:"Hong Kong",iso:"hk"},
            {code:"+36",name:"Hungary",iso:"hu"},{code:"+354",name:"Iceland",iso:"is"},
            {code:"+91",name:"India",iso:"in"},{code:"+62",name:"Indonesia",iso:"id"},
            {code:"+98",name:"Iran",iso:"ir"},{code:"+964",name:"Iraq",iso:"iq"},
            {code:"+353",name:"Ireland",iso:"ie"},{code:"+972",name:"Israel",iso:"il"},
            {code:"+39",name:"Italy",iso:"it"},{code:"+225",name:"Ivory Coast",iso:"ci"},
            {code:"+81",name:"Japan",iso:"jp"},{code:"+962",name:"Jordan",iso:"jo"},
            {code:"+7",name:"Kazakhstan",iso:"kz"},{code:"+254",name:"Kenya",iso:"ke"},
            {code:"+965",name:"Kuwait",iso:"kw"},{code:"+996",name:"Kyrgyzstan",iso:"kg"},
            {code:"+856",name:"Laos",iso:"la"},{code:"+371",name:"Latvia",iso:"lv"},
            {code:"+961",name:"Lebanon",iso:"lb"},{code:"+266",name:"Lesotho",iso:"ls"},
            {code:"+231",name:"Liberia",iso:"lr"},{code:"+218",name:"Libya",iso:"ly"},
            {code:"+423",name:"Liechtenstein",iso:"li"},{code:"+370",name:"Lithuania",iso:"lt"},
            {code:"+352",name:"Luxembourg",iso:"lu"},{code:"+261",name:"Madagascar",iso:"mg"},
            {code:"+265",name:"Malawi",iso:"mw"},{code:"+60",name:"Malaysia",iso:"my"},
            {code:"+960",name:"Maldives",iso:"mv"},{code:"+223",name:"Mali",iso:"ml"},
            {code:"+356",name:"Malta",iso:"mt"},{code:"+222",name:"Mauritania",iso:"mr"},
            {code:"+230",name:"Mauritius",iso:"mu"},{code:"+52",name:"Mexico",iso:"mx"},
            {code:"+373",name:"Moldova",iso:"md"},{code:"+377",name:"Monaco",iso:"mc"},
            {code:"+976",name:"Mongolia",iso:"mn"},{code:"+382",name:"Montenegro",iso:"me"},
            {code:"+212",name:"Morocco",iso:"ma"},{code:"+258",name:"Mozambique",iso:"mz"},
            {code:"+95",name:"Myanmar",iso:"mm"},{code:"+264",name:"Namibia",iso:"na"},
            {code:"+977",name:"Nepal",iso:"np"},{code:"+31",name:"Netherlands",iso:"nl"},
            {code:"+64",name:"New Zealand",iso:"nz"},{code:"+505",name:"Nicaragua",iso:"ni"},
            {code:"+227",name:"Niger",iso:"ne"},{code:"+234",name:"Nigeria",iso:"ng"},
            {code:"+850",name:"North Korea",iso:"kp"},{code:"+389",name:"North Macedonia",iso:"mk"},
            {code:"+47",name:"Norway",iso:"no"},{code:"+968",name:"Oman",iso:"om"},
            {code:"+92",name:"Pakistan",iso:"pk"},{code:"+970",name:"Palestine",iso:"ps"},
            {code:"+507",name:"Panama",iso:"pa"},{code:"+675",name:"Papua New Guinea",iso:"pg"},
            {code:"+595",name:"Paraguay",iso:"py"},{code:"+51",name:"Peru",iso:"pe"},
            {code:"+63",name:"Philippines",iso:"ph"},{code:"+48",name:"Poland",iso:"pl"},
            {code:"+351",name:"Portugal",iso:"pt"},{code:"+974",name:"Qatar",iso:"qa"},
            {code:"+40",name:"Romania",iso:"ro"},{code:"+7",name:"Russia",iso:"ru"},
            {code:"+250",name:"Rwanda",iso:"rw"},{code:"+966",name:"Saudi Arabia",iso:"sa"},
            {code:"+221",name:"Senegal",iso:"sn"},{code:"+381",name:"Serbia",iso:"rs"},
            {code:"+248",name:"Seychelles",iso:"sc"},{code:"+232",name:"Sierra Leone",iso:"sl"},
            {code:"+65",name:"Singapore",iso:"sg"},{code:"+421",name:"Slovakia",iso:"sk"},
            {code:"+386",name:"Slovenia",iso:"si"},{code:"+252",name:"Somalia",iso:"so"},
            {code:"+27",name:"South Africa",iso:"za"},{code:"+82",name:"South Korea",iso:"kr"},
            {code:"+211",name:"South Sudan",iso:"ss"},{code:"+34",name:"Spain",iso:"es"},
            {code:"+94",name:"Sri Lanka",iso:"lk"},{code:"+249",name:"Sudan",iso:"sd"},
            {code:"+597",name:"Suriname",iso:"sr"},{code:"+46",name:"Sweden",iso:"se"},
            {code:"+41",name:"Switzerland",iso:"ch"},{code:"+963",name:"Syria",iso:"sy"},
            {code:"+886",name:"Taiwan",iso:"tw"},{code:"+992",name:"Tajikistan",iso:"tj"},
            {code:"+255",name:"Tanzania",iso:"tz"},{code:"+66",name:"Thailand",iso:"th"},
            {code:"+228",name:"Togo",iso:"tg"},{code:"+216",name:"Tunisia",iso:"tn"},
            {code:"+90",name:"Turkey",iso:"tr"},{code:"+993",name:"Turkmenistan",iso:"tm"},
            {code:"+256",name:"Uganda",iso:"ug"},{code:"+380",name:"Ukraine",iso:"ua"},
            {code:"+971",name:"UAE",iso:"ae"},{code:"+44",name:"UK",iso:"gb"},
            {code:"+1",name:"USA",iso:"us"},{code:"+598",name:"Uruguay",iso:"uy"},
            {code:"+998",name:"Uzbekistan",iso:"uz"},{code:"+678",name:"Vanuatu",iso:"vu"},
            {code:"+58",name:"Venezuela",iso:"ve"},{code:"+84",name:"Vietnam",iso:"vn"},
            {code:"+967",name:"Yemen",iso:"ye"},{code:"+260",name:"Zambia",iso:"zm"},
            {code:"+263",name:"Zimbabwe",iso:"zw"}
        ];

        allCountries.sort((a,b) => a.name.localeCompare(b.name));
        let dropdown = null, searchInput = null;

        const updateDisplay = (country) => {
            const flagSpan = modalCountrySelector.querySelector(".fi");
            if (flagSpan) flagSpan.className = `fi fi-${country.iso}`;
            
            const codeSpan = modalCountrySelector.querySelector("span:nth-of-type(2)");
            if (codeSpan) codeSpan.textContent = country.code;
            
            // حفظ كود الدولة في data attribute
            modalCountrySelector.setAttribute('data-country-code', country.code);
        };

        const createOption = (country) => {
            const opt = document.createElement("div");
            opt.className = "country-option";
            opt.innerHTML = `<span class="fi fi-${country.iso}"></span><span class="country-code">${country.code}</span><span class="country-name">${country.name}</span>`;
            opt.addEventListener("click", () => { 
                updateDisplay(country);
                closeDropdown(); 
            });
            return opt;
        };

        const filterCountries = (term) => {
            term = term.toLowerCase().trim();
            return term ? allCountries.filter(c => c.name.toLowerCase().includes(term) || c.code.includes(term)) : allCountries;
        };

        const renderList = (countries) => {
            const list = dropdown.querySelector(".country-list");
            list.innerHTML = countries.length ? "" : "<div class='no-results'>No countries found</div>";
            countries.forEach(c => list.appendChild(createOption(c)));
        };

        const openDropdown = () => {
            dropdown = document.createElement("div");
            dropdown.className = "country-dropdown is-open";
            
            const searchBox = document.createElement("div");
            searchBox.className = "country-search-container";
            searchInput = document.createElement("input");
            searchInput.type = "text";
            searchInput.className = "country-search-input";
            searchInput.placeholder = "Search country or code...";
            searchInput.autocomplete = "off";
            
            searchInput.addEventListener("input", (e) => renderList(filterCountries(e.target.value)));
            searchInput.addEventListener("click", (e) => e.stopPropagation());
            searchInput.addEventListener("keydown", (e) => e.stopPropagation());
            searchBox.appendChild(searchInput);

            const list = document.createElement("div");
            list.className = "country-list";

            dropdown.appendChild(searchBox);
            dropdown.appendChild(list);
            modalCountrySelector.parentElement.style.position = "relative";
            modalCountrySelector.parentElement.appendChild(dropdown);
            renderList(allCountries);
            setTimeout(() => searchInput?.focus(), 100);

            // Prevent specs-modal from scrolling when dropdown is open
            const specsModal = document.querySelector("[data-specs-modal]");
            if (specsModal) {
                specsModal.style.overflowY = "hidden";
            }
        };

        const closeDropdown = () => {
            if (dropdown?.parentElement) {
                dropdown.parentElement.removeChild(dropdown);
                dropdown = searchInput = null;
            }
            // Restore scrolling on specs-modal
            const specsModal = document.querySelector("[data-specs-modal]");
            if (specsModal) {
                specsModal.style.overflowY = "auto";
            }
        };

        modalCountrySelector.addEventListener("click", (e) => { 
            e.stopPropagation(); 
            dropdown ? closeDropdown() : openDropdown(); 
        });
        
        document.addEventListener("click", (e) => {
            if (dropdown && !dropdown.contains(e.target) && !modalCountrySelector.contains(e.target)) {
                closeDropdown();
            }
        });
        
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape" && dropdown) closeDropdown();
        });
        
        // إضافة كود الدولة للرقم عند إرسال فورم المودال
        const modalForm = modalCountrySelector.closest('form');
        if (modalForm) {
            modalForm.addEventListener('submit', (e) => {
                const phoneInput = modalForm.querySelector('input[name="phone"]');
                if (phoneInput && phoneInput.value) {
                    const countryCode = modalCountrySelector.getAttribute('data-country-code') || '+20';
                    const phoneValue = phoneInput.value.trim();
                    
                    // إذا الرقم مش مبتدي بـ +، أضف كود الدولة
                    if (!phoneValue.startsWith('+')) {
                        phoneInput.value = countryCode + ' ' + phoneValue;
                    }
                }
            });
        }
    }
});
