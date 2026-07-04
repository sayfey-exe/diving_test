// Carte interactive des spots de plongée (Leaflet + tuiles OpenStreetMap).
(function () {
  var el = document.getElementById("map");
  if (!el || typeof L === "undefined") return;

  var spots = [];
  try { spots = JSON.parse(el.dataset.spots || "[]"); } catch (e) { spots = []; }
  var spotUrlTpl = el.dataset.spotUrl || "/spots/__KEY__";
  var canAdd = el.dataset.canAdd === "yes";

  // Icônes Leaflet servies localement. On supprime _getIconUrl pour éviter que
  // Leaflet préfixe son imagePath auto-détecté à nos URLs absolues.
  delete L.Icon.Default.prototype._getIconUrl;
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: "/static/vendor/leaflet/images/marker-icon-2x.png",
    iconUrl: "/static/vendor/leaflet/images/marker-icon.png",
    shadowUrl: "/static/vendor/leaflet/images/marker-shadow.png",
  });

  var map = L.map("map", { scrollWheelZoom: true }).setView([42.7, 8.5], 6);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map);

  var bounds = [];
  spots.forEach(function (s) {
    var m = L.marker([s.lat, s.lon]).addTo(map);
    var url = spotUrlTpl.replace("__KEY__", encodeURIComponent(s.key));
    var tag = s.user ? '<span class="map-popup-tag">communauté</span>' : "";
    var html =
      '<div class="map-popup"><strong>' + escapeHtml(s.nom) + "</strong>" + tag +
      '<div class="map-popup-sub">' + escapeHtml(s.lieu || "") + "</div>" +
      '<div class="map-popup-meta">🐟 ' + s.nb_poissons + " espèces · 📸 " + s.nb_photos + " photo" + (s.nb_photos !== 1 ? "s" : "") + "</div>" +
      '<a class="map-popup-link" href="' + url + '">Voir le spot →</a></div>';
    m.bindPopup(html);
    bounds.push([s.lat, s.lon]);
  });
  if (bounds.length) map.fitBounds(bounds, { padding: [40, 40], maxZoom: 8 });

  // Ajout d'un spot en cliquant sur la carte (utilisateurs connectés).
  if (canAdd) {
    var newMarker = null;
    var latEl = document.getElementById("spot-lat");
    var lonEl = document.getElementById("spot-lon");
    var hint = document.getElementById("add-spot-hint");
    var submit = document.getElementById("add-spot-submit");
    map.on("click", function (e) {
      var lat = e.latlng.lat, lon = e.latlng.lng;
      if (newMarker) { newMarker.setLatLng(e.latlng); }
      else {
        newMarker = L.marker(e.latlng, { opacity: 0.85 }).addTo(map)
          .bindPopup("📍 Emplacement de ton nouveau spot").openPopup();
      }
      if (latEl) latEl.value = lat.toFixed(5);
      if (lonEl) lonEl.value = lon.toFixed(5);
      if (submit) submit.disabled = false;
      if (hint) hint.innerHTML = "✅ Emplacement choisi (" + lat.toFixed(4) + ", " + lon.toFixed(4) +
        "). Complète le formulaire ci-dessous.";
      var form = document.getElementById("add-spot");
      if (form) form.scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
  }

  function escapeHtml(str) {
    return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }
})();
