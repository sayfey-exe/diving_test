// Zoom au clic sur les images des fiches.
(function () {
  document.querySelectorAll(".fiche-figure img").forEach(function (img) {
    img.addEventListener("click", function () {
      img.classList.toggle("img-zoomed");
    });
  });
})();

// Auto-évaluation interactive sur les fiches de cours.
// Chaque question révèle immédiatement la bonne réponse + l'explication.
(function () {
  document.querySelectorAll(".quiz-q").forEach(function (qEl) {
    var correct = parseInt(qEl.dataset.correct, 10);
    var options = qEl.querySelectorAll(".quiz-opt");
    var feedback = qEl.querySelector(".quiz-feedback");
    var answered = false;

    options.forEach(function (opt) {
      opt.addEventListener("click", function () {
        if (answered) return;
        answered = true;
        var chosen = parseInt(opt.dataset.index, 10);

        options.forEach(function (o, i) {
          o.disabled = true;
          if (i === correct) o.classList.add("is-correct");
          if (i === chosen && chosen !== correct) o.classList.add("is-wrong");
        });

        var ok = chosen === correct;
        var img = document.createElement("img");
        img.className = "quiz-pascal";
        img.src = "/static/img/" + (ok ? "pascal-content.gif" : "pascal-pas-content.gif");
        img.alt = ok ? "Pascal est content" : "Pascal n'est pas content";
        var span = document.createElement("span");
        span.textContent = (ok ? "✅ Bonne réponse ! " : "❌ Raté. ") +
          (feedback.dataset.explication || "");
        feedback.appendChild(img);
        feedback.appendChild(span);
        feedback.classList.add("show", ok ? "ok" : "ko");
      });
    });
  });
})();
