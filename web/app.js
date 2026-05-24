const listings = [
  {
    id: 685605,
    title: "1-комнатная квартира на Ginta Latina",
    district: "Чокана",
    address: "str. Ginta Latina 21",
    price: 390,
    rooms: 1,
    floor: "4/9",
    status: "active",
    date: "2026-05-03",
    image: "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=85",
    video: false,
    kids: true,
    pets: true,
    newBuild: false,
    source: "https://t.me/",
    description: "Светлая квартира с аккуратной мебелью, быстрым доступом к транспорту и спокойным жилым двором.",
    features: ["Можно с детьми", "Можно с животными", "Тихий двор"],
  },
  {
    id: 685612,
    title: "2-комнатная квартира с ливингом",
    district: "Чокана",
    address: "Maria Dragan 38/2",
    price: 500,
    rooms: 2,
    floor: "8/12",
    status: "active",
    date: "2026-05-03",
    image: "https://images.unsplash.com/photo-1600210491892-03d54c0aaf87?auto=format&fit=crop&w=1200&q=85",
    video: false,
    kids: true,
    pets: false,
    newBuild: false,
    source: "https://t.me/",
    description: "Практичная планировка для пары или семьи, отдельная спальня и просторная зона отдыха.",
    features: ["Ливинг", "Семейный формат", "Готова к заселению"],
  },
  {
    id: 685575,
    title: "1-комнатная квартира в новом доме",
    district: "Чокана",
    address: "ул. Джинтэ Латинэ 16/12",
    price: 450,
    rooms: 1,
    floor: "9/12",
    status: "active",
    date: "2026-05-03",
    image: "https://images.unsplash.com/photo-1560185007-c5ca9d2c014d?auto=format&fit=crop&w=1200&q=85",
    video: false,
    kids: false,
    pets: false,
    newBuild: true,
    source: "https://t.me/",
    description: "Новострой с нейтральным интерьером, хорошим светом и чистой входной группой.",
    features: ["Новострой", "Светлая кухня", "Свежий ремонт"],
  },
  {
    id: 685422,
    title: "1-комнатная квартира с автономным отоплением",
    district: "Чокана",
    address: "str. Петру Заднипру",
    price: 600,
    rooms: 1,
    floor: "6/10",
    status: "active",
    date: "2026-05-03",
    image: "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=1200&q=85",
    video: true,
    kids: false,
    pets: false,
    newBuild: true,
    source: "https://t.me/",
    description: "Современный объект с автономным отоплением, диваном и спокойной цветовой палитрой.",
    features: ["Видео", "Автономное отопление", "Новострой"],
  },
  {
    id: 685429,
    title: "2-комнатная квартира у Florilor",
    district: "Рышкановка",
    address: "str. Florilor 30/2",
    price: 600,
    rooms: 2,
    floor: "2/5",
    status: "active",
    date: "2026-05-03",
    image: "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=1200&q=85",
    video: false,
    kids: true,
    pets: true,
    newBuild: false,
    source: "https://t.me/",
    description: "Квартира с кондиционером, автономным отоплением и редким разрешением на проживание с питомцами.",
    features: ["Кондиционер", "Можно с детьми", "Можно с животными"],
  },
  {
    id: 685482,
    title: "1-комнатная квартира с ливингом на Димо",
    district: "Рышкановка",
    address: "str. Димо 1/1",
    price: 550,
    rooms: 1,
    floor: "3/5",
    status: "active",
    date: "2026-05-03",
    image: "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=85",
    video: false,
    kids: false,
    pets: false,
    newBuild: false,
    source: "https://t.me/",
    description: "Компактный городской формат с ливингом, свежим ремонтом и быстрым выездом в центр.",
    features: ["Ливинг", "Свежий ремонт", "Тихая улица"],
  },
  {
    id: 684748,
    title: "1-комнатная квартира с ливингом",
    district: "Чокана",
    address: "str. Mircea cel Batran 41/A",
    price: 650,
    rooms: 1,
    floor: "10/15",
    status: "reserved",
    date: "2026-05-02",
    image: "https://images.unsplash.com/photo-1600047509358-9dc75507daeb?auto=format&fit=crop&w=1200&q=85",
    video: true,
    kids: true,
    pets: false,
    newBuild: true,
    source: "https://t.me/",
    description: "Видовой этаж, новый дом и аккуратная мебель. Объект сейчас в статусе брони.",
    features: ["Бронь", "Видео", "Новострой"],
  },
  {
    id: 684712,
    title: "2-комнатная квартира на Kiev",
    district: "Рышкановка",
    address: "str. Kiev 12/1",
    price: 450,
    rooms: 2,
    floor: "4/5",
    status: "active",
    date: "2026-05-02",
    image: "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1200&q=85",
    video: true,
    kids: true,
    pets: true,
    newBuild: false,
    source: "https://t.me/",
    description: "Редкое сочетание цены, района и условий: можно с детьми и по договоренности с животными.",
    features: ["Видео", "Можно с детьми", "Можно с животными"],
  },
];

const galleryImages = [
  "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=85",
  "https://images.unsplash.com/photo-1600210491892-03d54c0aaf87?auto=format&fit=crop&w=1200&q=85",
  "https://images.unsplash.com/photo-1560185007-c5ca9d2c014d?auto=format&fit=crop&w=1200&q=85",
  "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=1200&q=85",
];

const state = {
  search: "",
  district: "all",
  rooms: "all",
  status: "all",
  minPrice: "",
  maxPrice: "",
  pets: false,
  kids: false,
  newBuild: false,
  activePhotos: [],
  activePhotoIndex: 0,
};

const els = {
  grid: document.querySelector("#listingGrid"),
  resultCount: document.querySelector("#resultCount"),
  visibleCount: document.querySelector("#visibleCount"),
  avgPrice: document.querySelector("#avgPrice"),
  activeCount: document.querySelector("#activeCount"),
  districtCount: document.querySelector("#districtCount"),
  empty: document.querySelector("#emptyState"),
  search: document.querySelector("#searchInput"),
  district: document.querySelector("#districtFilter"),
  districtSelect: document.querySelector("#districtSelect"),
  districtTrigger: document.querySelector("#districtTrigger"),
  districtMenu: document.querySelector("#districtMenu"),
  minPrice: document.querySelector("#minPrice"),
  maxPrice: document.querySelector("#maxPrice"),
  rooms: document.querySelector("#roomsFilter"),
  status: document.querySelector("#statusFilter"),
  pets: document.querySelector("#petsFilter"),
  kids: document.querySelector("#kidsFilter"),
  newBuild: document.querySelector("#newBuildFilter"),
  sort: document.querySelector("#sortFilter"),
  resetTop: document.querySelector("#resetTop"),
  dialog: document.querySelector("#listingDialog"),
  dialogContent: document.querySelector("#dialogContent"),
  closeDialog: document.querySelector("#closeDialog"),
};

function formatPrice(price) {
  return `${price.toLocaleString("ru-RU")} EUR`;
}

function statusLabel(status) {
  return status === "reserved" ? "Бронь" : "Свободна";
}

function populateDistricts() {
  const districts = ["all", ...new Set(listings.map((item) => item.district))].sort((a, b) => {
    if (a === "all") return -1;
    if (b === "all") return 1;
    return a.localeCompare(b, "ru");
  });

  if (els.district) {
    districts.slice(1).forEach((district) => {
      const option = document.createElement("option");
      option.value = district;
      option.textContent = district;
      els.district.append(option);
    });
  }

  if (els.districtMenu) {
    els.districtMenu.innerHTML = districts.map((district) => `
      <button type="button" role="option" data-value="${district}" aria-selected="${district === state.district}">
        ${district === "all" ? "Все районы" : district}
      </button>
    `).join("");
  }
}

function updateDistrictSelect() {
  const label = state.district === "all" ? "Все районы" : state.district;
  if (els.districtTrigger) els.districtTrigger.querySelector("span").textContent = label;
  if (els.districtMenu) {
    [...els.districtMenu.querySelectorAll("[data-value]")].forEach((option) => {
      option.setAttribute("aria-selected", String(option.dataset.value === state.district));
    });
  }
  if (els.district) els.district.value = state.district;
}

function getFilteredListings() {
  const query = state.search.trim().toLowerCase();
  const min = Number(state.minPrice) || 0;
  const max = Number(state.maxPrice) || Infinity;

  const filtered = listings.filter((item) => {
    const haystack = `${item.title} ${item.district} ${item.address} ${item.description} ${item.features.join(" ")}`.toLowerCase();
    return (
      (!query || haystack.includes(query)) &&
      (state.district === "all" || item.district === state.district) &&
      (state.rooms === "all" || item.rooms === Number(state.rooms)) &&
      (state.status === "all" || item.status === state.status) &&
      item.price >= min &&
      item.price <= max &&
      (!state.pets || item.pets) &&
      (!state.kids || item.kids) &&
      (!state.newBuild || item.newBuild)
    );
  });

  return filtered.sort((a, b) => new Date(b.date) - new Date(a.date));
}

function renderStats(items) {
  const avg = items.length ? Math.round(items.reduce((sum, item) => sum + item.price, 0) / items.length) : 0;
  els.resultCount.textContent = items.length;
  if (els.visibleCount) els.visibleCount.textContent = items.length;
  if (els.avgPrice) els.avgPrice.textContent = formatPrice(avg);
  if (els.activeCount) els.activeCount.textContent = items.filter((item) => item.status === "active").length;
  if (els.districtCount) els.districtCount.textContent = new Set(items.map((item) => item.district)).size;
}

function renderListings() {
  const items = getFilteredListings();
  renderStats(items);
  els.empty.hidden = items.length > 0;
  els.grid.innerHTML = items.map((item) => `
    <article class="listing-card" data-open="${item.id}" tabindex="0" role="button" aria-label="Открыть ${item.title}">
      <div class="image-wrap">
        <img src="${item.image}" alt="${item.title}" loading="lazy" />
      </div>
      <div class="card-body">
        <div class="card-top">
          <div>
            <div class="price">${formatPrice(item.price)}</div>
          </div>
          <div class="district">${new Date(item.date).toLocaleDateString("ru-RU")}</div>
        </div>
        <h2>${item.title}</h2>
        <div class="district">${item.district} · ${item.address}</div>
        <div class="meta">
          <span><strong>${item.rooms}</strong> комнат${item.rooms === 1 ? "а" : "ы"}</span>
          <span><strong>${item.floor}</strong> этаж</span>
        </div>
        <div class="features">
          ${item.features.map((feature) => `<span>${feature}</span>`).join("")}
        </div>
      </div>
    </article>
  `).join("");
}

function setSegment(container, value) {
  if (!container) return;
  [...container.querySelectorAll("button")].forEach((button) => {
    button.classList.toggle("is-active", button.dataset.value === value);
  });
}

function resetFilters() {
  Object.assign(state, {
    search: "",
    district: "all",
    rooms: "all",
    status: "all",
    minPrice: "",
    maxPrice: "",
    pets: false,
    kids: false,
    newBuild: false,
  });

  if (els.district) els.district.value = "all";
  updateDistrictSelect();
  els.minPrice.value = "";
  els.maxPrice.value = "";
  els.pets.checked = false;
  els.kids.checked = false;
  els.newBuild.checked = false;
  if (els.sort) els.sort.value = "fresh";
  if (els.search) els.search.value = "";
  setSegment(els.rooms, "all");
  setSegment(els.status, "all");
  renderListings();
}

function openListing(id) {
  const item = listings.find((listing) => listing.id === Number(id));
  if (!item) return;
  const photos = [item.image, ...galleryImages.filter((image) => image !== item.image)].slice(0, 4);
  const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${item.address}, ${item.district}, Chisinau`)}`;
  state.activePhotos = photos;
  state.activePhotoIndex = 0;
  els.dialogContent.innerHTML = `
    <div class="dialog-layout">
      <section class="dialog-gallery">
        <div class="dialog-photo-stage">
          <img class="dialog-main-image" src="${photos[0]}" alt="${item.title}" />
          <button type="button" class="gallery-arrow prev" data-gallery-step="-1" aria-label="Предыдущее фото">‹</button>
          <button type="button" class="gallery-arrow next" data-gallery-step="1" aria-label="Следующее фото">›</button>
        </div>
        <div class="dialog-thumbs">
          ${photos.map((photo, index) => `
            <button type="button" class="${index === 0 ? "is-active" : ""}" data-photo="${photo}" aria-label="Фото ${index + 1}">
              <img src="${photo}" alt="" />
            </button>
          `).join("")}
        </div>
      </section>
      <section class="dialog-info">
        <h2>${formatPrice(item.price)}</h2>
        <h3>${item.title}</h3>
        <div class="dialog-address-row">
          <a class="map-link" href="${mapsUrl}" target="_blank" rel="noreferrer" aria-label="Открыть адрес на карте">
            <svg aria-hidden="true" viewBox="0 0 32 32" class="map-pin-icon">
              <path class="pin-shape" d="M16 3.2c-5 0-9 4-9 9 0 7.1 9 16.2 9 16.2s9-9.1 9-16.2c0-5-4-9-9-9Z" />
              <circle class="pin-hole" cx="16" cy="12.2" r="3.3" />
              <ellipse class="pin-ring ring-1" cx="16" cy="27.2" rx="8.8" ry="2.2" />
              <ellipse class="pin-ring ring-2" cx="16" cy="27.2" rx="5.4" ry="1.2" />
            </svg>
          </a>
          <div>
            <span>${item.district} · ${item.address}</span>
            <strong>${item.rooms} комнат${item.rooms === 1 ? "а" : "ы"} · ${item.floor} этаж</strong>
          </div>
        </div>
        <p>${item.description}</p>
        <div class="features">${item.features.map((feature) => `<span>${feature}</span>`).join("")}</div>
      </section>
    </div>
  `;
  els.dialog.showModal();
}

function showGalleryPhoto(index) {
  if (!state.activePhotos.length) return;
  state.activePhotoIndex = (index + state.activePhotos.length) % state.activePhotos.length;
  const photo = state.activePhotos[state.activePhotoIndex];
  const mainImage = els.dialogContent.querySelector(".dialog-main-image");
  if (mainImage) mainImage.src = photo;
  [...els.dialogContent.querySelectorAll(".dialog-thumbs button")].forEach((button, buttonIndex) => {
    button.classList.toggle("is-active", buttonIndex === state.activePhotoIndex);
  });
}

function bindEvents() {
  if (els.search) {
    els.search.addEventListener("input", (event) => {
      state.search = event.target.value;
      renderListings();
    });
  }
  if (els.district) {
    els.district.addEventListener("change", (event) => {
      state.district = event.target.value;
      updateDistrictSelect();
      renderListings();
    });
  }
  if (els.districtTrigger && els.districtMenu && els.districtSelect) {
    els.districtTrigger.addEventListener("click", () => {
      const isOpen = !els.districtMenu.hidden;
      els.districtMenu.hidden = isOpen;
      els.districtTrigger.setAttribute("aria-expanded", String(!isOpen));
    });
    els.districtMenu.addEventListener("click", (event) => {
      const option = event.target.closest("[data-value]");
      if (!option) return;
      state.district = option.dataset.value;
      updateDistrictSelect();
      els.districtMenu.hidden = true;
      els.districtTrigger.setAttribute("aria-expanded", "false");
      renderListings();
    });
    document.addEventListener("click", (event) => {
      if (els.districtSelect.contains(event.target)) return;
      els.districtMenu.hidden = true;
      els.districtTrigger.setAttribute("aria-expanded", "false");
    });
  }
  els.minPrice.addEventListener("input", (event) => {
    state.minPrice = event.target.value;
    renderListings();
  });
  els.maxPrice.addEventListener("input", (event) => {
    state.maxPrice = event.target.value;
    renderListings();
  });
  els.rooms.addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) return;
    state.rooms = button.dataset.value;
    setSegment(els.rooms, state.rooms);
    renderListings();
  });
  if (els.status) {
    els.status.addEventListener("click", (event) => {
      const button = event.target.closest("button");
      if (!button) return;
      state.status = button.dataset.value;
      setSegment(els.status, state.status);
      renderListings();
    });
  }
  els.pets.addEventListener("change", (event) => {
    state.pets = event.target.checked;
    renderListings();
  });
  els.kids.addEventListener("change", (event) => {
    state.kids = event.target.checked;
    renderListings();
  });
  els.newBuild.addEventListener("change", (event) => {
    state.newBuild = event.target.checked;
    renderListings();
  });
  if (els.sort) {
    els.sort.addEventListener("change", (event) => {
      state.sort = event.target.value;
      renderListings();
    });
  }
  if (els.resetTop) els.resetTop.addEventListener("click", resetFilters);
  els.grid.addEventListener("click", (event) => {
    const card = event.target.closest("[data-open]");
    if (card) openListing(card.dataset.open);
  });
  els.grid.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" && event.key !== " ") return;
    const card = event.target.closest("[data-open]");
    if (!card) return;
    event.preventDefault();
    openListing(card.dataset.open);
  });
  els.dialogContent.addEventListener("click", (event) => {
    const arrow = event.target.closest("[data-gallery-step]");
    if (arrow) {
      showGalleryPhoto(state.activePhotoIndex + Number(arrow.dataset.galleryStep));
      return;
    }
    const thumb = event.target.closest("[data-photo]");
    if (!thumb) return;
    showGalleryPhoto(state.activePhotos.indexOf(thumb.dataset.photo));
  });
  document.addEventListener("keydown", (event) => {
    if (!els.dialog.open) return;
    if (event.key === "ArrowLeft") showGalleryPhoto(state.activePhotoIndex - 1);
    if (event.key === "ArrowRight") showGalleryPhoto(state.activePhotoIndex + 1);
  });
  els.closeDialog.addEventListener("click", () => els.dialog.close());
}

populateDistricts();
bindEvents();
renderListings();
