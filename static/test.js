// Gestion des tests "blanc" et "examen".
(function () {
  var app = document.getElementById("test-app");
  if (!app) return;

  var MODE = app.dataset.mode;            // "blanc" | "examen"
  var DUREE_MIN = parseInt(app.dataset.duree, 10) || 40;
  var SUBMIT_URL = app.dataset.submitUrl;
  var QUESTIONS = JSON.parse(document.getElementById("questions-data").textContent);
  var LETTERS = ["A", "B", "C", "D", "E", "F"];

  var answers = {};      // { questionId: indexChoisi }
  var current = 0;
  var timerId = null;
  var remaining = DUREE_MIN * 60;
  var finished = false;

  // Éléments
  var elIntro = document.getElementById("test-intro");
  var elPlay = document.getElementById("test-play");
  var elResults = document.getElementById("test-results");
  var elQZone = document.getElementById("question-zone");
  var elProgressLabel = document.getElementById("progress-label");
  var elProgressFill = document.getElementById("progress-fill");
  var elDots = document.getElementById("test-dots");
  var elTimer = document.getElementById("timer");
  var btnStart = document.getElementById("btn-start");
  var btnPrev = document.getElementById("btn-prev");
  var btnNext = document.getElementById("btn-next");
  var btnSkip = document.getElementById("btn-skip");
  var btnFinish = document.getElementById("btn-finish");

  // ---------------------------------------------------------------- Démarrage
  btnStart.addEventListener("click", function () {
    elIntro.hidden = true;
    elPlay.hidden = false;
    buildDots();
    renderQuestion();
    if (MODE === "examen") startTimer();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  // ---------------------------------------------------------------- Timer
  function startTimer() {
    updateTimer();
    timerId = setInterval(function () {
      remaining--;
      updateTimer();
      if (remaining <= 0) {
        clearInterval(timerId);
        submit();
      }
    }, 1000);
  }
  function updateTimer() {
    if (!elTimer) return;
    var m = Math.floor(remaining / 60);
    var s = remaining % 60;
    elTimer.textContent = (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
    if (remaining <= 60) elTimer.classList.add("warning");
  }

  // ---------------------------------------------------------------- Rendu question
  function renderQuestion() {
    var q = QUESTIONS[current];
    var chosen = answers[q.id];

    var html = '<div class="q-card">' +
      '<p class="q-chapter">' + escapeHtml(q.chapitre_titre) + '</p>' +
      '<h2>' + escapeHtml(q.q) + '</h2>' +
      '<div class="q-options">';
    q.options.forEach(function (opt, i) {
      var sel = (chosen === i) ? " selected" : "";
      html += '<button type="button" class="q-opt' + sel + '" data-index="' + i + '">' +
        '<span class="letter">' + LETTERS[i] + '</span>' +
        '<span>' + escapeHtml(opt) + '</span></button>';
    });
    html += '</div></div>';
    elQZone.innerHTML = html;

    elQZone.querySelectorAll(".q-opt").forEach(function (btn) {
      btn.addEventListener("click", function () {
        answers[q.id] = parseInt(btn.dataset.index, 10);
        elQZone.querySelectorAll(".q-opt").forEach(function (b) { b.classList.remove("selected"); });
        btn.classList.add("selected");
        updateDots();
        updateControls();
      });
    });

    elProgressLabel.textContent = "Question " + (current + 1) + " / " + QUESTIONS.length;
    elProgressFill.style.width = ((current + 1) / QUESTIONS.length * 100) + "%";
    updateControls();
    updateDots();
  }

  function updateControls() {
    btnPrev.disabled = (current === 0);
    var isLast = (current === QUESTIONS.length - 1);
    btnNext.hidden = isLast;
    btnFinish.hidden = !isLast;
  }

  // ---------------------------------------------------------------- Dots
  function buildDots() {
    elDots.innerHTML = "";
    QUESTIONS.forEach(function (q, i) {
      var d = document.createElement("button");
      d.className = "dot";
      d.textContent = i + 1;
      d.addEventListener("click", function () { current = i; renderQuestion(); });
      elDots.appendChild(d);
    });
    updateDots();
  }
  function updateDots() {
    var dots = elDots.children;
    for (var i = 0; i < dots.length; i++) {
      dots[i].classList.toggle("answered", answers[QUESTIONS[i].id] !== undefined);
      dots[i].classList.toggle("current", i === current);
    }
  }

  // ---------------------------------------------------------------- Navigation
  btnPrev.addEventListener("click", function () { if (current > 0) { current--; renderQuestion(); } });
  btnNext.addEventListener("click", function () { if (current < QUESTIONS.length - 1) { current++; renderQuestion(); } });
  if (btnSkip) btnSkip.addEventListener("click", function () {
    if (current < QUESTIONS.length - 1) { current++; renderQuestion(); }
  });
  btnFinish.addEventListener("click", function () { confirmAndSubmit(); });

  function confirmAndSubmit() {
    var nbRep = Object.keys(answers).length;
    var manquantes = QUESTIONS.length - nbRep;
    var msg = manquantes > 0
      ? "Il te reste " + manquantes + " question(s) sans réponse. Terminer quand même ?"
      : "Terminer et voir tes résultats ?";
    if (window.confirm(msg)) submit();
  }

  // ---------------------------------------------------------------- Soumission
  function submit() {
    if (finished) return;
    finished = true;
    if (timerId) clearInterval(timerId);

    fetch(SUBMIT_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ reponses: answers }),
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (data.error) { alert(data.error); window.location.reload(); return; }
        renderResults(data);
      })
      .catch(function () { alert("Erreur réseau. Réessaie."); finished = false; });
  }

  // ---------------------------------------------------------------- Résultats
  function renderResults(data) {
    elPlay.hidden = true;
    elResults.hidden = false;

    var pct = data.total ? Math.round(data.score / data.total * 100) : 0;
    var pass = data.note20 >= 10;
    var color = pass ? "var(--success)" : (pct >= 40 ? "var(--warn)" : "var(--danger)");
    var verdict = pass ? "Réussi 🎉" : "À retravailler";

    var html = '<div class="score-hero">' +
      '<div class="score-ring" style="background: conic-gradient(' + color + ' ' + pct + '%, #e6eef5 0);">' +
        '<div style="background:#fff;width:108px;height:108px;border-radius:50%;display:grid;place-items:center;">' +
          '<div><div class="score-num">' + data.score + '</div>' +
          '<div class="score-tot">/ ' + data.total + '</div></div>' +
        '</div>' +
      '</div>' +
      '<p class="score-verdict ' + (pass ? "verdict-pass" : "verdict-fail") + '">' + verdict + '</p>' +
      '<p class="score-note">Note : <strong>' + data.note20 + ' / 20</strong> · ' + pct + '% de bonnes réponses</p>' +
      '</div>';

    // Bilan par chapitre
    html += '<div class="chapter-breakdown"><h3>📊 Bilan par chapitre</h3>';
    var chaps = Object.keys(data.par_chapitre).sort();
    chaps.forEach(function (name) {
      var s = data.par_chapitre[name];
      var p = Math.round(s.ok / s.total * 100);
      var c = p >= 60 ? "var(--success)" : (p >= 40 ? "var(--warn)" : "var(--danger)");
      html += '<div class="cb-row">' +
        '<span class="cb-name">' + escapeHtml(name) + '</span>' +
        '<span class="cb-bar"><span class="cb-bar-fill" style="width:' + p + '%;background:' + c + ';"></span></span>' +
        '<span class="cb-score">' + s.ok + '/' + s.total + '</span></div>';
    });
    html += '</div>';

    // Actions
    html += '<div class="results-actions">' +
      '<a class="btn btn-primary" href="' + window.location.pathname + '">↻ Refaire un test</a>' +
      '<a class="btn btn-ghost" href="/cours">📚 Revoir le cours</a>' +
      '</div>';

    // Correction détaillée (mode blanc uniquement)
    if (data.details) {
      html += '<div class="filter-toggle">' +
        '<button data-filter="all" class="active">Tout (' + data.total + ')</button>' +
        '<button data-filter="ko">Mes erreurs (' + (data.total - data.score) + ')</button>' +
        '</div>';
      html += '<div class="correction"><h3>📖 Correction détaillée</h3>';
      data.details.forEach(function (d, idx) {
        html += renderCorrItem(d, idx);
      });
      html += '</div>';
    }

    elResults.innerHTML = html;
    window.scrollTo({ top: 0, behavior: "smooth" });

    // Filtre erreurs / tout
    var toggle = elResults.querySelector(".filter-toggle");
    if (toggle) {
      toggle.addEventListener("click", function (e) {
        var b = e.target.closest("button");
        if (!b) return;
        toggle.querySelectorAll("button").forEach(function (x) { x.classList.remove("active"); });
        b.classList.add("active");
        var filter = b.dataset.filter;
        elResults.querySelectorAll(".corr-item").forEach(function (item) {
          item.style.display = (filter === "ko" && item.classList.contains("ok")) ? "none" : "";
        });
      });
    }
  }

  function renderCorrItem(d, idx) {
    var cls = d.juste ? "ok" : "ko";
    var tag = d.juste ? '<span class="corr-tag ok">✓ Juste</span>'
                      : '<span class="corr-tag ko">✗ Faux</span>';
    var html = '<div class="corr-item ' + cls + '">' +
      '<p class="corr-q">' + (idx + 1) + '. ' + escapeHtml(d.q) + tag + '</p>';
    d.options.forEach(function (opt, i) {
      var oc = "";
      if (i === d.correct) oc = " right";
      else if (i === d.choix) oc = " chosen-wrong";
      var mark = (i === d.correct) ? "✔ " : ((i === d.choix) ? "✗ " : "");
      html += '<div class="corr-opt' + oc + '">' + mark + escapeHtml(opt) + '</div>';
    });
    if (d.choix === null || d.choix === undefined) {
      html += '<div class="corr-opt chosen-wrong">— Pas de réponse</div>';
    }
    html += '<div class="corr-expl">💡 ' + escapeHtml(d.explication) +
      ' <a href="/cours/' + d.chapitre_slug + '">Revoir : ' + escapeHtml(d.chapitre_titre) + ' →</a></div>';
    html += '</div>';
    return html;
  }

  // ---------------------------------------------------------------- Utils
  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  // Avertir si on quitte en cours d'examen
  window.addEventListener("beforeunload", function (e) {
    if (!finished && !elPlay.hidden) { e.preventDefault(); e.returnValue = ""; }
  });
})();
