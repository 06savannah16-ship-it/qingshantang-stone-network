(function () {
  var width = 1400;
  var height = 720;
  var marginY = 74;

  d3.json("data/network.json", function (error, data) {
    if (error) {
      document.getElementById("network").innerHTML = "<p style='padding:2rem'>关系数据加载失败，请通过本地服务器打开项目。</p>";
      return;
    }

    var works = data.works;
    var authors = unique(works.map(function (d) { return d.creator; }));
    var families = unique(works.map(function (d) { return d.recipient; }));
    var workStep = (height - marginY * 2) / Math.max(works.length - 1, 1);
    var familyConnections = {};

    works.forEach(function (work, i) {
      (familyConnections[work.recipient] || (familyConnections[work.recipient] = [])).push(marginY + i * workStep);
    });

    var nodes = [];
    authors.forEach(function (name) {
      var first = works.map(function (d) { return d.creator; }).indexOf(name);
      nodes.push({ id: "a-" + name, label: name, type: "author", x: 140, y: marginY + first * workStep });
    });
    works.forEach(function (work, i) {
      nodes.push({ id: "w-" + work.id, label: work.title, type: "work", x: 700, y: marginY + i * workStep, work: work });
    });
    families.forEach(function (name) {
      var ys = familyConnections[name];
      nodes.push({ id: "f-" + name, label: name, type: "family", x: 1260, y: d3.mean(ys) });
    });

    var byId = {};
    nodes.forEach(function (node) { byId[node.id] = node; });
    var links = [];
    works.forEach(function (work) {
      links.push({ source: byId["a-" + work.creator], target: byId["w-" + work.id], work: work });
      links.push({ source: byId["w-" + work.id], target: byId["f-" + work.recipient], work: work });
    });

    var svg = d3.select("#network").append("svg")
      .attr("viewBox", "0 0 " + width + " " + height)
      .attr("preserveAspectRatio", "xMidYMid meet");

    svg.append("text").attr("class", "column-label").attr("x", 110).attr("y", 34).text("书写者 / WRITER");
    svg.append("text").attr("class", "column-label").attr("x", 645).attr("y", 34).text("入选石刻 / WORK");
    svg.append("text").attr("class", "column-label").attr("text-anchor", "end").attr("x", 1290).attr("y", 34).text("记忆对象 / RECIPIENT");

    var link = svg.selectAll("path.link").data(links).enter().append("path")
      .attr("class", "link")
      .attr("d", function (d) {
        var offset = d.source.type === "author" ? 10 : 82;
        var startX = d.source.x + offset;
        var endX = d.target.x - (d.target.type === "family" ? 10 : 82);
        var midX = (startX + endX) / 2;
        return "M" + startX + "," + d.source.y + " C" + midX + "," + d.source.y + " " + midX + "," + d.target.y + " " + endX + "," + d.target.y;
      });

    var node = svg.selectAll("g.node").data(nodes).enter().append("g")
      .attr("class", function (d) { return "node " + d.type; })
      .attr("transform", function (d) { return "translate(" + d.x + "," + d.y + ")"; })
      .on("mouseenter", highlight)
      .on("mouseleave", clearHighlight)
      .on("click", function (d) {
        var work = d.work || firstConnectedWork(d, links);
        if (work) updateStory(work);
        highlight(d);
      });

    node.filter(function (d) { return d.type !== "work"; }).append("circle").attr("r", 7);
    node.filter(function (d) { return d.type === "work"; }).append("rect")
      .attr("x", -82).attr("y", -13).attr("width", 164).attr("height", 26);
    node.append("text")
      .attr("x", function (d) { return d.type === "author" ? 14 : (d.type === "family" ? -14 : 0); })
      .attr("dy", ".35em")
      .text(function (d) { return shorten(d.label, d.type === "work" ? 12 : 18); });

    function highlight(d) {
      var workIds = {};
      if (d.type === "work") workIds[d.work.id] = true;
      links.forEach(function (l) {
        if (l.source.id === d.id || l.target.id === d.id) workIds[l.work.id] = true;
      });
      node.classed("muted", function (n) {
        return !(n.id === d.id || (n.work && workIds[n.work.id]) || links.some(function (l) {
          return workIds[l.work.id] && (l.source.id === n.id || l.target.id === n.id);
        }));
      }).classed("active", function (n) {
        return n.id === d.id || (n.work && workIds[n.work.id]);
      });
      link.classed("muted", function (l) { return !workIds[l.work.id]; })
        .classed("active", function (l) { return !!workIds[l.work.id]; });
    }

    function clearHighlight() {
      node.classed("muted", false).classed("active", false);
      link.classed("muted", false).classed("active", false);
    }
  });

  function unique(values) {
    return values.filter(function (value, index) { return values.indexOf(value) === index; });
  }

  function firstConnectedWork(node, links) {
    for (var i = 0; i < links.length; i++) {
      if (links[i].source.id === node.id || links[i].target.id === node.id) return links[i].work;
    }
    return null;
  }

  function shorten(text, max) {
    return text.length > max ? text.slice(0, max - 1) + "…" : text;
  }

  function updateStory(work) {
    var story = document.getElementById("story");
    story.querySelector(".story-kicker").textContent = work.date + " · " + work.theme;
    var image = story.querySelector("img");
    image.src = work.image;
    image.alt = work.title + "拓片";
    story.querySelector("h2").textContent = work.title;
    story.querySelector(".story-route").textContent = work.creator + " → " + work.recipient;
    story.querySelector(".story-body").textContent = work.human_note;
    story.querySelector(".story-status").textContent = "证据状态：" + work.confidence;
  }
})();
