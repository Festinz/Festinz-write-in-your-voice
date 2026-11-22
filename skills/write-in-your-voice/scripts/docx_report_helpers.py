#!/usr/bin/env python3
"""python-docx helpers for report layout: presets, figures, tables, equations.

Requires python-docx (pip install python-docx). Image equations also need matplotlib.

    from docx_report_helpers import Report
    r = Report(preset="compact", font="Times New Roman")
    r.heading("1. Results", level=1)
    r.paragraph("Table 1 lists the **selected** values.")      # ** ** marks bold
    r.table("Table 1. Measured and nominal resistance", ["Resistor", "Nominal", "Measured"],
            [["R1", "1000", "987"], ["R2", "4700", "4712"]], widths_cm=[3, 4, 4])
    r.figure("setup.png", width_cm=12, caption="Figure 1. Measurement setup")
    r.equation(r.text("e = 100 × ")
               + r.frac(r.sub("R", "meas") + r.text(" − ") + r.sub("R", "nom"), r.sub("R", "nom")))
    r.save("report.docx")

Run "python docx_report_helpers.py --demo demo.docx" to write a sample file.

Layout rules applied: table title directly above the table and kept with it, light
header shading, figure caption in its own paragraph directly below the image,
native Office Math equations (or 600-dpi images for PDF converters that cannot
render formulas).
"""

import argparse
from pathlib import Path

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

PRESETS = {
    # margins in cm: top, bottom, left, right
    "compact": dict(margins=(2.2, 2.0, 2.3, 2.3), body_pt=10, line=1.12, before=5, after=2.5,
                    align="left", caption_bold=True, caption_brackets=True, header_fill="DDEBF7"),
    "standard": dict(margins=(2.5, 2.5, 2.5, 2.5), body_pt=11, line=1.5, before=0, after=4,
                     align="justify", caption_bold=False, caption_brackets=False,
                     header_fill="E7E7E7"),
}
MATH_FONT = "Cambria Math"
SMALL_PT = 9


def _esc(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Report:
    """A DOCX document with the layout rules of the chosen preset."""

    def __init__(self, preset="compact", font="Times New Roman", equations="native",
                 equation_dir=None, page_numbers=True):
        if preset not in PRESETS:
            raise ValueError(f"preset must be one of {sorted(PRESETS)}")
        if equations not in ("native", "image"):
            raise ValueError("equations must be 'native' or 'image'")
        self.p = PRESETS[preset]
        self.font = font
        self.equations = equations
        self.equation_dir = Path(equation_dir) if equation_dir else None
        self._eq_count = 0
        self.doc = Document()
        self._page_setup()
        self._styles()
        if page_numbers:
            self._page_number_footer()

    # ----- setup ---------------------------------------------------------
    def _page_setup(self):
        s = self.doc.sections[0]
        s.page_width, s.page_height = Cm(21.0), Cm(29.7)  # A4
        top, bottom, left, right = self.p["margins"]
        s.top_margin, s.bottom_margin = Cm(top), Cm(bottom)
        s.left_margin, s.right_margin = Cm(left), Cm(right)
        self.text_width_cm = 21.0 - left - right

    def _styles(self):
        normal = self.doc.styles["Normal"]
        normal.font.name = self.font
        normal.font.size = Pt(self.p["body_pt"])
        normal.element.rPr.rFonts.set(qn("w:eastAsia"), self.font)
        fmt = normal.paragraph_format
        fmt.line_spacing = self.p["line"]
        fmt.space_before, fmt.space_after = Pt(self.p["before"]), Pt(self.p["after"])
        for name, size, before, after in (("Heading 1", 13, 12, 4), ("Heading 2", 11, 8, 2)):
            style = self.doc.styles[name]
            style.font.name, style.font.size = self.font, Pt(size)
            style.font.bold, style.font.italic = True, False
            style.font.color.rgb = RGBColor(0, 0, 0)
            rfonts = style.element.get_or_add_rPr().get_or_add_rFonts()
            for slot in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
                rfonts.set(qn(slot), self.font)
            for theme in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
                if rfonts.get(qn(theme)) is not None:
                    del rfonts.attrib[qn(theme)]
            style.paragraph_format.space_before = Pt(before)
            style.paragraph_format.space_after = Pt(after)
            style.paragraph_format.keep_with_next = True

    def _page_number_footer(self):
        p = self.doc.sections[0].footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for kind in ("begin", None, "end"):
            run = self._font(p.add_run(), SMALL_PT)
            if kind:
                node = OxmlElement("w:fldChar")
                node.set(qn("w:fldCharType"), kind)
            else:
                node = OxmlElement("w:instrText")
                node.set(qn("xml:space"), "preserve")
                node.text = "PAGE"
            run._r.append(node)

    def set_metadata(self, title="", author=""):
        """Set the document title and author (do not leave tool defaults)."""
        self.doc.core_properties.title = title
        self.doc.core_properties.author = author

    # ----- text ----------------------------------------------------------
    def _font(self, run, size=None, bold=None):
        run.font.name = self.font
        rfonts = run._element.get_or_add_rPr().get_or_add_rFonts()
        for slot in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
            rfonts.set(qn(slot), self.font)
        run.font.size = Pt(size or self.p["body_pt"])
        if bold is not None:
            run.font.bold = bold
        return run

    def paragraph(self, text="", size=None, align=None, keep_with_next=False):
        """Body paragraph. Text between ** ** is set in bold."""
        p = self.doc.add_paragraph()
        align = align or self.p["align"]
        p.alignment = {"left": WD_ALIGN_PARAGRAPH.LEFT, "center": WD_ALIGN_PARAGRAPH.CENTER,
                       "justify": WD_ALIGN_PARAGRAPH.JUSTIFY}[align]
        for i, part in enumerate(text.split("**")):
            if part:
                self._font(p.add_run(part), size, bold=True if i % 2 else None)
        p.paragraph_format.keep_with_next = keep_with_next
        return p

    def heading(self, text, level=1):
        h = self.doc.add_heading(level=level)
        self._font(h.add_run(text), 13 if level == 1 else 11, bold=True)
        return h

    # ----- tables --------------------------------------------------------
    def table(self, title, headers, rows, widths_cm=None, left_columns=(), bold_rows=()):
        """Titled table: the title sits directly above and stays with the table."""
        t = self.doc.add_paragraph()
        t.alignment = WD_ALIGN_PARAGRAPH.CENTER
        self._font(t.add_run(title), SMALL_PT, bold=self.p["caption_bold"])
        t.paragraph_format.space_before, t.paragraph_format.space_after = Pt(6), Pt(2.5)
        t.paragraph_format.keep_with_next = True

        table = self.doc.add_table(rows=1, cols=len(headers))
        table.style = "Table Grid"
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        self._cell_margins(table)

        def fill(cell, value, bold=False, left=False):
            cell.text = ""
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if left else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            self._font(p.add_run(str(value)), SMALL_PT, bold=bold)

        for i, header in enumerate(headers):
            fill(table.rows[0].cells[i], header, bold=True)
            self._shade(table.rows[0].cells[i], self.p["header_fill"])
        for r_index, values in enumerate(rows):
            if len(values) != len(headers):
                raise ValueError(f"row {r_index} has {len(values)} cells, expected {len(headers)}")
            cells = table.add_row().cells
            for i, value in enumerate(values):
                fill(cells[i], value, bold=r_index in bold_rows, left=i in left_columns)
        widths_cm = widths_cm or [self.text_width_cm * 0.95 / len(headers)] * len(headers)
        if sum(widths_cm) > self.text_width_cm + 1e-6:
            raise ValueError("table is wider than the text area")
        for row in table.rows:
            row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
            for i, width in enumerate(widths_cm):
                row.cells[i].width = Cm(width)
        for i, width in enumerate(widths_cm):
            table.columns[i].width = Cm(width)
        for row in table.rows[:-1]:  # keep the rows (and the title) on one page
            for cell in row.cells:
                cell.paragraphs[0].paragraph_format.keep_with_next = True
        spacer = self.doc.add_paragraph()
        spacer.paragraph_format.space_before = spacer.paragraph_format.space_after = Pt(0)
        spacer.paragraph_format.line_spacing = Pt(4)
        return table

    @staticmethod
    def _shade(cell, fill):
        tc_pr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        for key, value in (("w:val", "clear"), ("w:color", "auto"), ("w:fill", fill)):
            shd.set(qn(key), value)
        later = [tc_pr.find(qn(f"w:{tag}")) for tag in
                 ("noWrap", "tcMar", "textDirection", "tcFitText", "vAlign", "hideMark")]
        later = [node for node in later if node is not None]
        if later:
            later[0].addprevious(shd)  # schema order inside w:tcPr
        else:
            tc_pr.append(shd)

    @staticmethod
    def _cell_margins(table, top=40, bottom=40, left=90, right=90):
        mar = OxmlElement("w:tblCellMar")
        for side, value in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
            node = OxmlElement(f"w:{side}")
            node.set(qn("w:w"), str(value))
            node.set(qn("w:type"), "dxa")
            mar.append(node)
        look = table._tbl.tblPr.find(qn("w:tblLook"))
        if look is not None:
            look.addprevious(mar)
        else:
            table._tbl.tblPr.append(mar)

    # ----- figures -------------------------------------------------------
    def figure(self, image_path, width_cm, caption):
        """Centered image with the caption in its own paragraph directly below."""
        if width_cm > self.text_width_cm + 1e-6:
            raise ValueError("figure is wider than the text area")
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before, p.paragraph_format.space_after = Pt(5), Pt(1)
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.keep_with_next = True
        p.add_run().add_picture(str(image_path), width=Cm(width_cm))
        if self.p["caption_brackets"] and not caption.startswith("["):
            caption = f"[{caption}]"
        c = self.doc.add_paragraph()
        c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        self._font(c.add_run(caption), SMALL_PT, bold=self.p["caption_bold"])
        c.paragraph_format.space_before, c.paragraph_format.space_after = Pt(0), Pt(5)
        return c

    # ----- equations -----------------------------------------------------
    @staticmethod
    def text(value, upright=False):
        style = '<m:rPr><m:sty m:val="p"/></m:rPr>' if upright else ""
        return (f'<m:r>{style}<w:rPr><w:rFonts w:ascii="{MATH_FONT}" w:hAnsi="{MATH_FONT}" '
                f'w:cs="{MATH_FONT}"/></w:rPr><m:t xml:space="preserve">{_esc(value)}</m:t></m:r>')

    @classmethod
    def sub(cls, base, subscript):
        return (f"<m:sSub><m:e>{cls.text(base)}</m:e>"
                f"<m:sub>{cls.text(subscript, upright=True)}</m:sub></m:sSub>")

    @classmethod
    def sup(cls, base, superscript):
        return (f"<m:sSup><m:e>{cls.text(base)}</m:e>"
                f"<m:sup>{cls.text(superscript)}</m:sup></m:sSup>")

    @staticmethod
    def frac(numerator_xml, denominator_xml):
        return ('<m:f><m:fPr><m:type m:val="bar"/></m:fPr>'
                f"<m:num>{numerator_xml}</m:num><m:den>{denominator_xml}</m:den></m:f>")

    def equation(self, omml, mathtext=None):
        """Centered equation. omml is built with text/sub/sup/frac.

        With equations="image" the mathtext string (matplotlib syntax, e.g.
        r"$A = 100 \\times \\dfrac{N_c}{N}$") is typeset to a 600-dpi image instead,
        for PDF converters that cannot render Office Math.
        """
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = p.paragraph_format.space_after = Pt(3)
        if self.equations == "image":
            if not mathtext:
                raise ValueError("equations='image' needs the mathtext argument")
            p.paragraph_format.line_spacing = 1.0
            p.add_run().add_picture(str(self._equation_image(mathtext)))
            return p
        p.paragraph_format.line_spacing = 1.25
        p._p.append(parse_xml(
            '<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
            'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<m:oMathParaPr><m:jc m:val="center"/></m:oMathParaPr>'
            f"<m:oMath>{omml}</m:oMath></m:oMathPara>"))
        return p

    def _equation_image(self, mathtext):
        import matplotlib
        matplotlib.use("Agg", force=True)
        import matplotlib.pyplot as plt
        self._eq_count += 1
        folder = self.equation_dir or Path("_equations")
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"equation_{self._eq_count}.png"
        with plt.rc_context({"mathtext.fontset": "stix"}):
            fig = plt.figure(figsize=(0.1, 0.1))
            fig.text(0, 0, mathtext, fontsize=self.p["body_pt"] + 0.5)
            fig.savefig(path, dpi=600, bbox_inches="tight", pad_inches=0.02, facecolor="white")
            plt.close(fig)
        return path

    # ----- output --------------------------------------------------------
    def save(self, path):
        zoom = self.doc.settings.element.find(qn("w:zoom"))
        if zoom is not None and zoom.get(qn("w:percent")) is None:
            zoom.set(qn("w:percent"), "100")  # the default template omits a required attribute
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.doc.save(path)
        return path


def demo(path, preset="compact", equations="native"):
    out = Path(path)
    r = Report(preset=preset, equations=equations, equation_dir=out.parent / "_equations")
    r.set_metadata(title="Layout demo", author="")
    r.heading("1. Layout demo", level=1)
    r.paragraph("This file shows the **table**, **figure** and **equation** rules of the "
                f"{preset} preset. Table 1 is titled above; the equation is centered.")
    r.table("Table 1. Measured and nominal resistance (ohm)",
            ["Resistor", "Nominal", "Measured", "Error (%)"],
            [["R1", 1000, 987, "−1.30"], ["R2", 4700, 4712, "+0.26"]],
            widths_cm=[4, 3, 3, 4], bold_rows=(1,))
    r.paragraph("The relative error is computed from the values in Table 1:", keep_with_next=True)
    r.equation(r.text("e = 100 × ")
               + r.frac(r.sub("R", "meas") + r.text(" − ") + r.sub("R", "nom"), r.sub("R", "nom")),
               mathtext=r"$e = 100 \times \dfrac{R_{\mathrm{meas}} - R_{\mathrm{nom}}}{R_{\mathrm{nom}}}$")
    print("wrote", r.save(out))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--demo", metavar="OUT.docx", help="write a sample document")
    parser.add_argument("--preset", choices=sorted(PRESETS), default="compact")
    parser.add_argument("--equations", choices=("native", "image"), default="native")
    args = parser.parse_args()
    if not args.demo:
        parser.error("nothing to do: pass --demo OUT.docx, or import Report from this module")
    demo(args.demo, args.preset, args.equations)
