// Sửa document.xml giữ định dạng từng run, có tô màu chỗ đổi
const fs = require("fs");
const dec = s => s.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&amp;/g, "&");
const enc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const AFTER_COLOR = ["w:spacing", "w:w", "w:kern", "w:position", "w:sz", "w:szCs", "w:highlight", "w:u", "w:effect", "w:bdr", "w:shd", "w:fitText", "w:vertAlign", "w:rtl", "w:cs", "w:em", "w:lang", "w:eastAsianLayout", "w:specVanish", "w:oMath"];
const AFTER_B = ["w:i", "w:iCs", "w:caps", "w:smallCaps", "w:strike", "w:dstrike", "w:outline", "w:shadow", "w:emboss", "w:imprint", "w:noProof", "w:snapToGrid", "w:vanish", "w:webHidden", "w:color", ...AFTER_COLOR];

function insBefore(inner, tags, piece) {
  let pos = inner.length;
  for (const t of tags) { const i = inner.search(new RegExp("<" + t + "[ />]")); if (i >= 0 && i < pos) pos = i; }
  return inner.slice(0, pos) + piece + inner.slice(pos);
}
function styleRPr(rpr, color, bold) {
  let inner = rpr ? rpr.replace(/^<w:rPr>/, "").replace(/<\/w:rPr>$/, "") : "";
  inner = inner.replace(/<w:color [^>]*\/>/g, "");
  if (color) inner = insBefore(inner, AFTER_COLOR, `<w:color w:val="${color}"/>`);
  if (bold) { inner = inner.replace(/<w:b(?: [^>]*)?\/>/g, "").replace(/<w:bCs(?: [^>]*)?\/>/g, ""); inner = insBefore(inner, AFTER_B, "<w:b/><w:bCs/>"); }
  return "<w:rPr>" + inner + "</w:rPr>";
}
const mkRun = (rpr, text) => `<w:r>${rpr || ""}<w:t xml:space="preserve">${enc(text)}</w:t></w:r>`;

class Doc {
  constructor(dir) { this.f = dir + "/word/document.xml"; this.x = fs.readFileSync(this.f, "utf8"); this.log = []; }
  save() { fs.writeFileSync(this.f, this.x, "utf8"); }
  paras() { const o = []; const re = /<w:p[ >][\s\S]*?<\/w:p>/g; let m; while ((m = re.exec(this.x))) o.push({ s: m.index, e: m.index + m[0].length, xml: m[0] }); return o; }
  static runs(px) { // các <w:r> có chữ
    const o = []; const re = /<w:r(?: [^>]*)?>(?:(?!<\/w:r>)[\s\S])*?<\/w:r>/g; let m;
    while ((m = re.exec(px))) { if (m[0].startsWith("<w:rPr")) continue;
      const rpr = (m[0].match(/<w:rPr>[\s\S]*?<\/w:rPr>/) || [""])[0];
      const txt = [...m[0].matchAll(/<w:t(?:\s[^>]*)?>([\s\S]*?)<\/w:t>/g)].map(a => dec(a[1])).join("");
      o.push({ s: m.index, e: m.index + m[0].length, xml: m[0], rpr, txt }); }
    return o;
  }
  static text(px) { return Doc.runs(px).map(r => r.txt).join(""); }
  find(n) { return this.paras().filter(p => Doc.text(p.xml).includes(n)); }
  // thay cụm chữ bằng chữ mới có màu; occurrence: lần thứ mấy trong văn bản (mặc định yêu cầu duy nhất)
  replace(from, to, color, bold = false, expect = 1) { return this.replaceParts(from, [[to, color, bold]], expect); }
  // parts: [[text, color, bold]] — color "keep" = giữ định dạng gốc, không tô
  replaceParts(from, parts, expect = 1) {
    const to = parts.map(p => p[0]).join(""); const color = null, bold = false;
    let hits = 0; const ps = this.paras();
    for (const p of ps) hits += Doc.text(p.xml).split(from).length - 1;
    if (hits !== expect) throw new Error(`"${from}" gặp ${hits} lần, cần ${expect}`);
    for (const p of ps.reverse()) {
      let px = p.xml; let guard = 0;
      while (Doc.text(px).includes(from) && guard++ < 20) {
        const rs = Doc.runs(px); const full = rs.map(r => r.txt).join(""); const at = full.indexOf(from), end = at + from.length;
        let pos = 0; const out = []; let firstIdx = -1, lastIdx = -1;
        rs.forEach((r, i) => { const a = pos, b = pos + r.txt.length; pos = b; if (b > at && a < end) { if (firstIdx < 0) firstIdx = i; lastIdx = i; } });
        let a0 = 0; for (let i = 0; i < firstIdx; i++) a0 += rs[i].txt.length;
        let aL = 0; for (let i = 0; i < lastIdx; i++) aL += rs[i].txt.length;
        const F = rs[firstIdx], L = rs[lastIdx];
        const left = F.txt.slice(0, at - a0), right = L.txt.slice(end - aL);
        let rep = "";
        if (left) rep += mkRun(F.rpr, left);
        for (const [t, c, b] of parts) rep += mkRun(c === "keep" ? F.rpr : styleRPr(F.rpr, c, b), t);
        if (right) rep += mkRun(L.rpr, right);
        px = px.slice(0, F.s) + rep + px.slice(L.e);
        if (to.includes(from)) break;
      }
      this.x = this.x.slice(0, p.s) + px + this.x.slice(p.e);
    }
    this.log.push(`thay: ${from}  →  ${to}`);
  }
  // nhân bản đoạn chứa anchor, đặt ngay sau; parts = [[text,color,bold],...]
  cloneAfter(anchor, parts) {
    const a = this.find(anchor); if (a.length !== 1) throw new Error(`anchor "${anchor}" gặp ${a.length}`);
    let px = a[0].xml.replace(/\sw14:paraId="[^"]*"/, "").replace(/\sw14:textId="[^"]*"/, "");
    const rs = Doc.runs(px); const base = (rs[rs.length - 1] || rs[0]).rpr;
    const body = parts.map(([t, c, b]) => mkRun(styleRPr(base, c, b), t)).join("");
    px = px.slice(0, rs[0].s) + body + px.slice(rs[rs.length - 1].e);
    this.x = this.x.slice(0, a[0].e) + px + this.x.slice(a[0].e);
    this.log.push(`chèn sau "${anchor.slice(0, 30)}": ${parts.map(p => p[0]).join("").slice(0, 70)}…`);
  }
  // chèn đoạn chú giải màu lên đầu thân văn bản
  legend(lines) {
    const i = this.x.indexOf("<w:body>") + 8;
    const rp = (c, b) => `<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>${b ? "<w:b/><w:bCs/>" : ""}${c ? `<w:color w:val="${c}"/>` : ""}<w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>`;
    const ps = lines.map(parts => `<w:p><w:pPr><w:pBdr><w:top w:val="single" w:sz="4" w:space="1" w:color="BFBFBF"/><w:left w:val="single" w:sz="4" w:space="4" w:color="BFBFBF"/><w:bottom w:val="single" w:sz="4" w:space="1" w:color="BFBFBF"/><w:right w:val="single" w:sz="4" w:space="4" w:color="BFBFBF"/></w:pBdr><w:spacing w:before="0" w:after="0"/><w:jc w:val="left"/></w:pPr>${parts.map(([t, c, b]) => `<w:r>${rp(c, b)}<w:t xml:space="preserve">${enc(t)}</w:t></w:r>`).join("")}</w:p>`).join("")
      + `<w:p><w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr></w:p>`;
    this.x = this.x.slice(0, i) + ps + this.x.slice(i);
    this.log.push("chèn khối chú giải màu đầu văn bản");
  }
}
module.exports = Doc;
