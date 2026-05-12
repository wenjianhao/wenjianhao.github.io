(function () {
  const section = document.querySelector(".visitor-preview-section");
  if (!section) return;

  const defaultData = {
    source: "preview",
    views: 12438,
    visitors: 3184,
    countries: 42,
    updated_at: null,
    locations: [
      { code: "US", name: "United States", views: 4200 },
      { code: "CA", name: "Canada", views: 780 },
      { code: "GB", name: "United Kingdom", views: 960 },
      { code: "DE", name: "Germany", views: 620 },
      { code: "IN", name: "India", views: 1320 },
      { code: "CN", name: "China", views: 880 },
      { code: "AU", name: "Australia", views: 530 },
      { code: "BR", name: "Brazil", views: 460 }
    ]
  };

  const countryCentroids = {
    US: [39.8, -98.6], CA: [56.1, -106.3], MX: [23.6, -102.5], BR: [-14.2, -51.9],
    AR: [-38.4, -63.6], CL: [-35.7, -71.5], CO: [4.6, -74.1], PE: [-9.2, -75.0],
    GB: [55.3, -3.4], IE: [53.1, -8.0], FR: [46.2, 2.2], DE: [51.2, 10.5],
    NL: [52.1, 5.3], BE: [50.5, 4.5], ES: [40.4, -3.7], PT: [39.4, -8.2],
    IT: [41.9, 12.6], CH: [46.8, 8.3], AT: [47.5, 14.5], PL: [52.1, 19.1],
    CZ: [49.8, 15.5], DK: [56.0, 9.5], NO: [60.5, 8.5], SE: [62.0, 15.0],
    FI: [64.0, 26.0], UA: [49.0, 32.0], RO: [45.9, 24.9], GR: [39.1, 22.9],
    TR: [39.0, 35.0], RU: [61.5, 105.3], IL: [31.0, 35.0], SA: [23.9, 45.1],
    AE: [24.3, 54.4], EG: [26.8, 30.8], ZA: [-30.6, 22.9], NG: [9.1, 8.7],
    KE: [0.0, 37.9], IN: [22.6, 79.0], PK: [30.4, 69.3], BD: [23.7, 90.4],
    CN: [35.9, 104.2], JP: [36.2, 138.3], KR: [36.5, 127.9], TW: [23.7, 121.0],
    HK: [22.3, 114.2], SG: [1.35, 103.8], MY: [4.2, 102.0], TH: [15.8, 101.0],
    VN: [14.1, 108.3], ID: [-2.5, 118.0], PH: [12.9, 122.8], AU: [-25.3, 133.8],
    NZ: [-40.9, 174.9]
  };

  const countryAliases = {
    "UNITED STATES": "US",
    "UNITED STATES OF AMERICA": "US",
    "USA": "US",
    "CANADA": "CA",
    "UNITED KINGDOM": "GB",
    "UK": "GB",
    "GREAT BRITAIN": "GB",
    "GERMANY": "DE",
    "FRANCE": "FR",
    "INDIA": "IN",
    "CHINA": "CN",
    "AUSTRALIA": "AU",
    "BRAZIL": "BR",
    "SOUTH KOREA": "KR",
    "KOREA, REPUBLIC OF": "KR",
    "JAPAN": "JP",
    "TAIWAN": "TW",
    "HONG KONG": "HK",
    "SINGAPORE": "SG",
    "NETHERLANDS": "NL",
    "SWITZERLAND": "CH",
    "SWEDEN": "SE",
    "NORWAY": "NO",
    "FINLAND": "FI",
    "SPAIN": "ES",
    "ITALY": "IT",
    "PORTUGAL": "PT",
    "TURKEY": "TR",
    "ISRAEL": "IL",
    "MEXICO": "MX",
    "ARGENTINA": "AR",
    "CHILE": "CL",
    "COLOMBIA": "CO",
    "PERU": "PE",
    "SOUTH AFRICA": "ZA",
    "NIGERIA": "NG",
    "KENYA": "KE",
    "NEW ZEALAND": "NZ"
  };

  const labelOffsets = {
    US: [14, -14],
    CA: [14, -18],
    GB: [14, -10],
    DE: [14, 16],
    IN: [14, 18],
    CN: [14, -14],
    AU: [14, -12],
    BR: [14, -12],
    JP: [14, -10],
    KR: [14, 16]
  };

  function formatNumber(value) {
    return new Intl.NumberFormat("en-US").format(Number(value || 0));
  }

  function project(lat, lon) {
    const width = 1000;
    const height = 500;
    const padX = 42;
    const padY = 42;
    const x = padX + ((lon + 180) / 360) * (width - padX * 2);
    const y = padY + ((90 - lat) / 180) * (height - padY * 2);
    return [x, y];
  }

  function normalizeCode(location) {
    const raw = String(location.code || location.id || location.country_code || "").trim();
    if (/^[A-Za-z]{2}$/.test(raw)) return raw.toUpperCase();
    const name = String(location.name || location.country || raw).trim().toUpperCase();
    return countryAliases[name] || "";
  }

  function render(data) {
    const viewsEl = section.querySelector("[data-visitor-views]");
    const visitorsEl = section.querySelector("[data-visitor-visitors]");
    const countriesEl = section.querySelector("[data-visitor-countries]");
    const updatedEl = section.querySelector("[data-visitor-updated]");
    const captionEl = section.querySelector("[data-visitor-caption]");
    const dotLayer = section.querySelector("[data-visitor-dots]");
    const labelLayer = section.querySelector("[data-visitor-labels]");
    const countryListEl = section.querySelector("[data-visitor-country-list]");

    viewsEl.textContent = formatNumber(data.views);
    visitorsEl.textContent = formatNumber(data.visitors);
    countriesEl.textContent = formatNumber(data.countries);

    if (data.updated_at) {
      const dt = new Date(data.updated_at);
      updatedEl.textContent = "Updated " + dt.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric"
      });
    } else if (data.source === "preview") {
      updatedEl.textContent = "Preview mode. Real analytics will appear after GoatCounter is connected.";
    } else {
      updatedEl.textContent = "Analytics data available.";
    }

    captionEl.textContent = data.source === "preview"
      ? "Preview world map with example visitor locations"
      : "Country-level visitor locations from GoatCounter";

    dotLayer.innerHTML = "";
    labelLayer.innerHTML = "";
    countryListEl.innerHTML = "";
    const locations = Array.isArray(data.locations) ? data.locations.slice() : [];
    const usable = locations
      .map((item) => {
        const code = normalizeCode(item);
        const centroid = countryCentroids[code];
        if (!centroid) return null;
        const weight = Number(item.views || item.count || item.visitors || 0);
        return { ...item, code, weight, centroid };
      })
      .filter(Boolean)
      .sort((a, b) => b.weight - a.weight)
      .slice(0, 30);

    const topCountries = usable.slice(0, 6);

    const maxWeight = usable.reduce((max, item) => Math.max(max, item.weight), 1);

    for (const item of usable) {
      const [x, y] = project(item.centroid[0], item.centroid[1]);
      const radius = 4 + (item.weight / maxWeight) * 8;
      const halo = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      halo.setAttribute("cx", x.toFixed(1));
      halo.setAttribute("cy", y.toFixed(1));
      halo.setAttribute("r", (radius + 5).toFixed(1));
      halo.setAttribute("class", "visitor-dot-halo");

      const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      dot.setAttribute("cx", x.toFixed(1));
      dot.setAttribute("cy", y.toFixed(1));
      dot.setAttribute("r", radius.toFixed(1));
      dot.setAttribute("class", "visitor-dot");

      const title = document.createElementNS("http://www.w3.org/2000/svg", "title");
      title.textContent = `${item.name || item.code}: ${formatNumber(item.weight)} views`;
      dot.appendChild(title);

      dotLayer.appendChild(halo);
      dotLayer.appendChild(dot);
    }

    for (const item of topCountries) {
      const [x, y] = project(item.centroid[0], item.centroid[1]);
      const [dx, dy] = labelOffsets[item.code] || [12, -12];
      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", x.toFixed(1));
      line.setAttribute("y1", y.toFixed(1));
      line.setAttribute("x2", (x + dx).toFixed(1));
      line.setAttribute("y2", (y + dy).toFixed(1));
      line.setAttribute("class", "visitor-label-line");

      const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
      label.setAttribute("x", (x + dx + 4).toFixed(1));
      label.setAttribute("y", (y + dy + 4).toFixed(1));
      label.setAttribute("class", "visitor-label-text");
      label.textContent = item.name || item.code;

      labelLayer.appendChild(line);
      labelLayer.appendChild(label);
    }

    for (const item of topCountries) {
      const row = document.createElement("div");
      row.className = "visitor-country-row";

      const left = document.createElement("div");
      left.className = "visitor-country-name";
      left.textContent = item.name || item.code;

      const right = document.createElement("div");
      right.className = "visitor-country-count";
      right.textContent = formatNumber(item.weight);

      row.appendChild(left);
      row.appendChild(right);
      countryListEl.appendChild(row);
    }
  }

  fetch("/data/visitors.json?ts=20260511a", { cache: "no-store" })
    .then((response) => {
      if (!response.ok) throw new Error("Failed to load visitor data");
      return response.json();
    })
    .then((data) => render(data))
    .catch(() => render(defaultData));
})();
