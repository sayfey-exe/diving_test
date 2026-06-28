// Graphique d'évolution des scores — SVG maison, sans dépendance externe.
(function () {
  var el = document.getElementById("score-chart");
  if (!el) return;

  var points;
  try { points = JSON.parse(el.dataset.points || "[]"); } catch (e) { points = []; }
  if (!points.length) { el.innerHTML = "<p>Pas encore de données.</p>"; return; }

  // Dimensions (le SVG est responsive via viewBox).
  var W = 640, H = 280, padL = 38, padR = 16, padT = 18, padB = 34;
  var plotW = W - padL - padR, plotH = H - padT - padB;
  var maxY = 20; // note sur 20

  function x(i) {
    if (points.length === 1) return padL + plotW / 2;
    return padL + (i / (points.length - 1)) * plotW;
  }
  function y(v) { return padT + plotH - (v / maxY) * plotH; }

  var svg = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="chart-svg" role="img" ' +
            'aria-label="Évolution des notes">';

  // Grille horizontale + libellés (0,5,10,15,20)
  [0, 5, 10, 15, 20].forEach(function (g) {
    var gy = y(g);
    svg += '<line x1="' + padL + '" y1="' + gy + '" x2="' + (W - padR) + '" y2="' + gy +
           '" class="chart-grid"/>';
    svg += '<text x="' + (padL - 8) + '" y="' + (gy + 4) + '" class="chart-axis" text-anchor="end">' + g + '</text>';
  });

  // Ligne de la moyenne de réussite (10/20)
  svg += '<line x1="' + padL + '" y1="' + y(10) + '" x2="' + (W - padR) + '" y2="' + y(10) +
         '" class="chart-pass"/>';

  // Tracé de la courbe
  var d = "";
  points.forEach(function (p, i) { d += (i === 0 ? "M" : "L") + x(i).toFixed(1) + " " + y(p.note).toFixed(1) + " "; });
  svg += '<path d="' + d + '" class="chart-line"/>';

  // Points + valeurs + dates
  points.forEach(function (p, i) {
    var cx = x(i), cy = y(p.note);
    var cls = p.mode === "examen" ? "chart-dot dot-examen" : "chart-dot dot-blanc";
    svg += '<circle cx="' + cx.toFixed(1) + '" cy="' + cy.toFixed(1) + '" r="5" class="' + cls + '">' +
           '<title>' + p.date + ' — ' + p.note + '/20 (' + p.mode + ')</title></circle>';
    svg += '<text x="' + cx.toFixed(1) + '" y="' + (cy - 10).toFixed(1) + '" class="chart-val" text-anchor="middle">' + p.note + '</text>';
    // une date sur deux si beaucoup de points
    if (points.length <= 12 || i % 2 === 0) {
      svg += '<text x="' + cx.toFixed(1) + '" y="' + (H - 12) + '" class="chart-axis" text-anchor="middle">' + p.date + '</text>';
    }
  });

  svg += "</svg>";
  svg += '<div class="chart-legend">' +
         '<span><span class="lg-dot dot-blanc"></span> Test blanc</span>' +
         '<span><span class="lg-dot dot-examen"></span> Test examen</span>' +
         '<span><span class="lg-line"></span> Seuil 10/20</span></div>';
  el.innerHTML = svg;
})();
