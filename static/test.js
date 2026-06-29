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
  function isAnswered(q) {
    var a = answers[q.id];
    if (q.multi) return Array.isArray(a) && a.length > 0;
    return a !== undefined && a !== null;
  }

  function renderQuestion() {
    var q = QUESTIONS[current];
    var multi = !!q.multi;
    var chosen = answers[q.id];
    var chosenArr = multi ? (Array.isArray(chosen) ? chosen : []) : null;

    var html = '<div class="q-card">' +
      '<p class="q-chapter">' + escapeHtml(q.chapitre_titre) +
        (multi ? ' <span class="q-multi-badge">choix multiples</span>' : '') + '</p>' +
      '<h2>' + escapeHtml(q.q) + '</h2>' +
      (multi ? '<p class="q-multi-hint">☑ Plusieurs réponses possibles : coche toutes les bonnes.</p>' : '') +
      '<div class="q-options">';
    q.options.forEach(function (opt, i) {
      var isSel = multi ? (chosenArr.indexOf(i) !== -1) : (chosen === i);
      html += '<button type="button" class="q-opt' + (isSel ? ' selected' : '') +
        (multi ? ' q-opt-multi' : '') + '" data-index="' + i + '">' +
        '<span class="letter">' + LETTERS[i] + '</span>' +
        '<span>' + escapeHtml(opt) + '</span></button>';
    });
    html += '</div></div>';
    elQZone.innerHTML = html;

    elQZone.querySelectorAll(".q-opt").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var i = parseInt(btn.dataset.index, 10);
        if (multi) {
          var arr = Array.isArray(answers[q.id]) ? answers[q.id] : [];
          var p = arr.indexOf(i);
          if (p === -1) arr.push(i); else arr.splice(p, 1);
          answers[q.id] = arr;
          btn.classList.toggle("selected");
        } else {
          answers[q.id] = i;
          elQZone.querySelectorAll(".q-opt").forEach(function (b) { b.classList.remove("selected"); });
          btn.classList.add("selected");
        }
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
      dots[i].classList.toggle("answered", isAnswered(QUESTIONS[i]));
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
    var nbRep = 0;
    QUESTIONS.forEach(function (q) { if (isAnswered(q)) nbRep++; });
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

    // Sauvegarde / invitation à se connecter
    if (data.saved) {
      html += '<p class="save-hint save-ok">✅ Résultat enregistré dans ton profil.</p>';
    } else {
      html += '<p class="save-hint save-info">💾 <a href="/connexion">Connecte-toi</a> ' +
        'ou <a href="/inscription">crée un compte</a> pour sauvegarder tes résultats et suivre ta progression.</p>';
    }

    // Actions
    html += '<div class="results-actions">' +
      '<a class="btn btn-primary" href="' + window.location.pathname + '">↻ Refaire un test</a>' +
      '<a class="btn btn-ghost" href="/cours">📚 Revoir le cours</a>' +
      (data.authenticated ? '<a class="btn btn-ghost" href="/profil">👤 Mon profil</a>' : '') +
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

    // Envoi des remarques sur les questions
    elResults.addEventListener("click", function (e) {
      var btn = e.target.closest(".comment-send");
      if (!btn) return;
      var box = btn.closest(".corr-comment-box");
      var textarea = box.querySelector("textarea");
      var status = box.querySelector(".comment-status");
      var texte = (textarea.value || "").trim();
      if (!texte) { status.textContent = "Écris une remarque d'abord."; status.className = "comment-status err"; return; }
      btn.disabled = true;
      status.textContent = "Envoi…"; status.className = "comment-status";
      fetch("/question/" + encodeURIComponent(btn.dataset.qid) + "/commentaire", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ comment: texte }),
      })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (d.ok) {
            status.textContent = "✅ Merci, ta remarque est enregistrée !";
            status.className = "comment-status ok";
            textarea.disabled = true;
          } else {
            status.textContent = d.error || "Erreur.";
            status.className = "comment-status err";
            btn.disabled = false;
          }
        })
        .catch(function () {
          status.textContent = "Erreur réseau.";
          status.className = "comment-status err";
          btn.disabled = false;
        });
    });
  }

  function renderCorrItem(d, idx) {
    var cls = d.juste ? "ok" : "ko";
    var tag = d.juste ? '<span class="corr-tag ok">✓ Juste</span>'
                      : '<span class="corr-tag ko">✗ Faux</span>';
    var multiBadge = d.multi ? ' <span class="q-multi-badge">choix multiples</span>' : '';
    var html = '<div class="corr-item ' + cls + '">' +
      '<p class="corr-q">' + (idx + 1) + '. ' + escapeHtml(d.q) + multiBadge + tag + '</p>';
    var corrects = d.corrects || [];
    var choix = d.choix || [];
    d.options.forEach(function (opt, i) {
      var isCorrect = corrects.indexOf(i) !== -1;
      var isChosen = choix.indexOf(i) !== -1;
      var oc = isCorrect ? " right" : (isChosen ? " chosen-wrong" : "");
      var mark = isCorrect ? "✔ " : (isChosen ? "✗ " : "");
      html += '<div class="corr-opt' + oc + '">' + mark + escapeHtml(opt) + '</div>';
    });
    if (!choix.length) {
      html += '<div class="corr-opt chosen-wrong">— Pas de réponse</div>';
    }
    html += '<div class="corr-expl">💡 ' + escapeHtml(d.explication) +
      ' <a href="/cours/' + d.chapitre_slug + '">Revoir : ' + escapeHtml(d.chapitre_titre) + ' →</a></div>';
    // Zone de commentaire (remarque sur la question)
    html += '<details class="corr-comment">' +
      '<summary>💬 Une remarque sur cette question ?</summary>' +
      '<div class="corr-comment-box">' +
        '<textarea placeholder="Ex : énoncé ambigu, réponse discutable, faute de frappe..." maxlength="1000"></textarea>' +
        '<div class="corr-comment-actions">' +
          '<button type="button" class="btn btn-ghost btn-sm comment-send" data-qid="' + escapeHtml(d.id) + '">Envoyer ma remarque</button>' +
          '<span class="comment-status"></span>' +
        '</div>' +
      '</div></details>';
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
