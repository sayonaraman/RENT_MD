const listings = [
  {
    id: 685605,
    title: "1-комнатная квартира на Ginta Latina",
    district: "Чокана",
    address: "str. Ginta Latina 21",
    price: 390,
    rooms: 1,
    area: 44,
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
    area: 62,
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
    area: 47,
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
    area: 50,
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
    area: 58,
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
    area: 52,
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
    area: 55,
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
    area: 54,
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
  const districts = [...new Set(listings.map((item) => item.district))].sort();
  districts.forEach((district) => {
    const option = document.createElement("option");
    option.value = district;
    option.textContent = district;
    els.district.append(option);
  });
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
    <article class="listing-card">
      <div class="image-wrap">
        <img src="${item.image}" alt="${item.title}" loading="lazy" />
        <div class="badge-row">
          <span class="status ${item.status}">${statusLabel(item.status)}</span>
          ${item.video ? '<span class="media-badge">Видео</span>' : '<span class="media-badge">Фото</span>'}
        </div>
      </div>
      <div class="card-body">
        <div class="card-top">
          <div>
            <div class="price">${formatPrice(item.price)}</div>
            <div class="district">${item.district}</div>
          </div>
          <div class="district">${new Date(item.date).toLocaleDateString("ru-RU")}</div>
        </div>
        <h2>${item.title}</h2>
        <div class="district">${item.address}</div>
        <div class="meta">
          <span><strong>${item.rooms}</strong>комнат</span>
          <span><strong>${item.area} м²</strong>площадь</span>
          <span><strong>${item.floor}</strong>этаж</span>
        </div>
        <div class="features">
          ${item.features.map((feature) => `<span>${feature}</span>`).join("")}
        </div>
        <div class="card-actions">
          <button class="primary-button" data-open="${item.id}">Смотреть</button>
          <a class="telegram-button" href="${item.source}" target="_blank" rel="noreferrer">Telegram</a>
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

  els.district.value = "all";
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
  els.dialogContent.innerHTML = `
    <div class="dialog-layout">
      <img src="${item.image}" alt="${item.title}" />
      <section class="dialog-info">
        <span class="status ${item.status}">${statusLabel(item.status)}</span>
        <h2>${formatPrice(item.price)}</h2>
        <p class="eyebrow">${item.district}</p>
        <h3>${item.title}</h3>
        <p>${item.description}</p>
        <div class="detail-list">
          <div><span>Адрес</span><strong>${item.address}</strong></div>
          <div><span>Комнаты</span><strong>${item.rooms}</strong></div>
          <div><span>Площадь</span><strong>${item.area} м²</strong></div>
          <div><span>Этаж</span><strong>${item.floor}</strong></div>
        </div>
        <div class="features">${item.features.map((feature) => `<span>${feature}</span>`).join("")}</div>
        <div class="card-actions">
          <a class="telegram-button" href="${item.source}" target="_blank" rel="noreferrer">Открыть в Telegram</a>
        </div>
      </section>
    </div>
  `;
  els.dialog.showModal();
}

function bindEvents() {
  if (els.search) {
    els.search.addEventListener("input", (event) => {
      state.search = event.target.value;
      renderListings();
    });
  }
  els.district.addEventListener("change", (event) => {
    state.district = event.target.value;
    renderListings();
  });
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
  els.resetTop.addEventListener("click", resetFilters);
  els.grid.addEventListener("click", (event) => {
    const button = event.target.closest("[data-open]");
    if (button) openListing(button.dataset.open);
  });
  els.closeDialog.addEventListener("click", () => els.dialog.close());
}

populateDistricts();
bindEvents();
renderListings();
