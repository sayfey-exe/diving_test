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
        feedback.textContent = (ok ? "✅ Bonne réponse ! " : "❌ Raté. ") +
          (feedback.dataset.explication || "");
        feedback.classList.add("show", ok ? "ok" : "ko");
      });
    });
  });
})();
