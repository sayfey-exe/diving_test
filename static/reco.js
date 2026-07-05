// Reconnaissance d'espèce à la demande sur le formulaire d'upload de photo.
(function () {
  var form = document.getElementById("photo-form");
  var btn = document.getElementById("reco-btn");
  if (!form || !btn) return;

  var input = document.getElementById("photo-input");
  var result = document.getElementById("reco-result");
  var select = document.getElementById("fish-select");
  var newSpecies = document.getElementById("new-species");
  var url = form.dataset.recoUrl;

  function show(msg, cls) {
    result.hidden = false;
    result.className = "reco-result" + (cls ? " " + cls : "");
    result.innerHTML = msg;
  }

  btn.addEventListener("click", function () {
    if (!input || !input.files || !input.files.length) {
      show("Choisis d'abord une photo à analyser.", "reco-warn");
      return;
    }
    var fd = new FormData();
    fd.append("photo", input.files[0]);
    btn.disabled = true;
    var old = btn.textContent;
    btn.textContent = "🤖 Analyse en cours…";
    show("Analyse de la photo…", "");

    fetch(url, { method: "POST", body: fd, headers: { "X-Requested-With": "fetch" } })
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (res) {
        var d = res.d;
        if (d.available === false) {
          show("🤖 Reconnaissance indisponible : " + (d.message || ""), "reco-warn");
          return;
        }
        if (d.error) { show("⚠️ " + d.error, "reco-warn"); return; }
        if (!d.suggestion) {
          show(d.message || "Aucune espèce reconnue.", "reco-warn");
          return;
        }
        var s = d.suggestion;
        var pct = Math.round((s.confiance || 0) * 100);
        if (s.match_key && select) {
          // Espèce déjà au catalogue : on la présélectionne.
          select.value = s.match_key;
          if (select.value === s.match_key) {
            if (newSpecies) newSpecies.value = "";
            show("🤖 On dirait <strong>" + escapeHtml(s.nom) + "</strong> (confiance " +
              pct + " %). Espèce présélectionnée — vérifie puis envoie.", "reco-ok");
            return;
          }
        }
        // Espèce inconnue du catalogue : on préremplit la proposition.
        if (newSpecies) {
          newSpecies.value = s.nom;
          if (select) select.value = "";
        }
        show("🤖 On dirait <strong>" + escapeHtml(s.nom) + "</strong> (confiance " +
          pct + " %). Nouvelle espèce préremplie — elle sera validée par un admin.", "reco-ok");
      })
      .catch(function () { show("⚠️ Erreur pendant l'analyse. Réessaie.", "reco-warn"); })
      .finally(function () { btn.disabled = false; btn.textContent = old; });
  });

  function escapeHtml(str) {
    return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }
})();
