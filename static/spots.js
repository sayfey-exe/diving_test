// Carte interactive des spots de plongée (Leaflet + tuiles OpenStreetMap).
(function () {
  var el = document.getElementById("map");
  if (!el || typeof L === "undefined") return;

  var spots = [];
  try { spots = JSON.parse(el.dataset.spots || "[]"); } catch (e) { spots = []; }
  var spotUrlTpl = el.dataset.spotUrl || "/spots/__ID__";

  // Icônes Leaflet servies localement (sinon les marqueurs sont invisibles).
  // On supprime _getIconUrl pour éviter que Leaflet préfixe son imagePath
  // auto-détecté à nos URLs absolues (sinon chemin dupliqué → 404).
  delete L.Icon.Default.prototype._getIconUrl;
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: "/static/vendor/leaflet/images/marker-icon-2x.png",
    iconUrl: "/static/vendor/leaflet/images/marker-icon.png",
    shadowUrl: "/static/vendor/leaflet/images/marker-shadow.png",
  });

  var map = L.map("map", { scrollWheelZoom: true }).setView([42.5, 6.0], 6);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map);

  var bounds = [];
  spots.forEach(function (s) {
    var m = L.marker([s.lat, s.lon]).addTo(map);
    var url = spotUrlTpl.replace("__ID__", encodeURIComponent(s.id));
    var html =
      '<div class="map-popup">' +
      '<strong>' + escapeHtml(s.nom) + "</strong>" +
      '<div class="map-popup-sub">' + escapeHtml(s.lieu) + "</div>" +
      '<div class="map-popup-meta">🐟 ' + s.nb_poissons + " espèces · 📸 " + s.nb_photos + " photo" + (s.nb_photos !== 1 ? "s" : "") + "</div>" +
      '<a class="map-popup-link" href="' + url + '">Voir le spot →</a>' +
      "</div>";
    m.bindPopup(html);
    bounds.push([s.lat, s.lon]);
  });

  if (bounds.length) {
    map.fitBounds(bounds, { padding: [40, 40], maxZoom: 8 });
  }

  function escapeHtml(str) {
    return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }
})();
