import os
import fitz
import toml

from mamba import description, it, before
from fitzutils import ToCEntry
from pdftocgen.tocgen import gen_toc

dirpath = os.path.dirname(os.path.abspath(__file__))

with description("gen_toc") as self:
    with before.all:
        self.level2 = fitz.open(os.path.join(dirpath, "files/level2.pdf"))
        self.level2_recipe = toml.load(
            open(os.path.join(dirpath, "files/level2_recipe.toml"))
        )
        self.level2_expect = [
            ToCEntry(level=1, title='1 Section One',
                     pagenum=1, vpos=237.6484375),
            ToCEntry(level=1, title='2 Section Two',
                     pagenum=1, vpos=567.3842163085938),
            ToCEntry(level=2, title='2.1 Subsection Two.One',
                     pagenum=2, vpos=452.56671142578125),
            ToCEntry(level=1,
                     title='3 Section Three, with looong loooong looong ti- tle',
                     pagenum=3, vpos=335.569580078125),
            ToCEntry(level=2, title='3.1 Subsection Three.One, '
                     'with even loooooooooooonger title, and probably even more',
                     pagenum=3, vpos=619.4886474609375),
            ToCEntry(level=2, title='3.2 Subsection Three.Two',
                     pagenum=4, vpos=512.3426513671875),
            ToCEntry(level=2, title='3.3 Subsection Three.Three',
                     pagenum=5, vpos=125.79861450195312),
            ToCEntry(level=1, title='4 The End',
                     pagenum=5, vpos=366.62347412109375)
        ]

        self.onepage = fitz.open(os.path.join(dirpath, "files/onepage.pdf"))
        self.onepage_recipe = toml.load(
            open(os.path.join(dirpath, "files/onepage_recipe.toml"))
        )
        self.onepage_greedy = toml.load(
            open(os.path.join(dirpath, "files/onepage_greedy.toml"))
        )
        self.onepage_expect = [
            # false positive, but easy to remove in post-processing
            ToCEntry(level=2, title='krasjet',
                     pagenum=1, vpos=196.53366088867188),
            ToCEntry(level=1, title='1 Section One',
                     pagenum=1, vpos=237.6484375),
            ToCEntry(level=1, title='2 Section Two',
                     pagenum=1, vpos=265.44744873046875),
            ToCEntry(level=2, title='2.1 Subsection Two.One',
                     pagenum=1, vpos=291.0536804199219),
            ToCEntry(level=2, title='2.2 Subsection Two.Two \xd7 2',
                     pagenum=1, vpos=311.1368103027344),
            ToCEntry(level=1, title='3 Section Three, with looong loooong looong ti- tle',
                     pagenum=1, vpos=334.00946044921875),
            ToCEntry(level=2, title='3.1 Subsection Three.One, '
                     'with even loooooooooooonger title, and probably even more',
                     pagenum=1, vpos=377.5487060546875),
            ToCEntry(level=2, title='3.2 Subsection Three.Two',
                     pagenum=1, vpos=411.8786926269531),
            ToCEntry(level=2, title='3.3 Subsection Three.Three',
                     pagenum=1, vpos=432.26068115234375),
            ToCEntry(level=3, title='3.3.1 Subsubsection Three.Three.One',
                     pagenum=1, vpos=452.1441345214844),
            ToCEntry(level=3, title='3.3.2 Subsubsection Three.Three.Two',
                     pagenum=1, vpos=470.53314208984375),
            ToCEntry(level=3, title='3.3.3 Subsubsection Three.Three.Three',
                     pagenum=1, vpos=488.9231262207031),
            ToCEntry(level=2, title='3.4 Subsection Three.Four',
                     pagenum=1, vpos=507.8106994628906),
            ToCEntry(level=2, title='3.5 Subsection Three.Five',
                     pagenum=1, vpos=528.191650390625),
            ToCEntry(level=1, title='4 The End',
                     pagenum=1, vpos=550.7654418945312)
        ]

        self.onepage_greedy_expect = [
            # hooray, no more false positives
            ToCEntry(level=1, title='1 Section One',
                     pagenum=1, vpos=237.6484375),
            ToCEntry(level=1, title='2 Section Two',
                     pagenum=1, vpos=265.44744873046875),
            ToCEntry(level=2, title='2.1 Subsection Two.One',
                     pagenum=1, vpos=291.0536804199219),
            ToCEntry(level=2, title='2.2 Subsection Two.Two \xd7 2',
                     pagenum=1, vpos=311.1368103027344),
            ToCEntry(level=1, title='3 Section Three, with looong loooong looong ti- tle',
                     pagenum=1, vpos=334.00946044921875),
            ToCEntry(level=2, title='3.1 Subsection Three.One, '
                     'with even loooooooooooonger title, and probably even more',
                     pagenum=1, vpos=377.5487060546875),
            ToCEntry(level=2, title='3.2 Subsection Three.Two',
                     pagenum=1, vpos=411.8786926269531),
            ToCEntry(level=2, title='3.3 Subsection Three.Three',
                     pagenum=1, vpos=432.26068115234375),
            ToCEntry(level=3, title='3.3.1 Subsubsection Three.Three.One',
                     pagenum=1, vpos=452.1441345214844),
            ToCEntry(level=3, title='3.3.2 Subsubsection Three.Three.Two',
                     pagenum=1, vpos=470.53314208984375),
            ToCEntry(level=3, title='3.3.3 Subsubsection Three.Three.Three',
                     pagenum=1, vpos=488.9231262207031),
            ToCEntry(level=2, title='3.4 Subsection Three.Four',
                     pagenum=1, vpos=507.8106994628906),
            ToCEntry(level=2, title='3.5 Subsection Three.Five',
                     pagenum=1, vpos=528.191650390625),
            ToCEntry(level=1, title='4 The End',
                     pagenum=1, vpos=550.7654418945312)
        ]

        self.hardmode = fitz.open(os.path.join(dirpath, "files/hardmode.pdf"))
        self.hardmode_recipe = toml.load(
            open(os.path.join(dirpath, "files/hardmode_recipe.toml"))
        )

        self.hardmode_expect = [
            ToCEntry(level=1, title='1 Section One',
                     pagenum=1, vpos=174.1232452392578),
            ToCEntry(level=1, title='2 Section 1 + 1 = 2',
                     pagenum=1, vpos=584.5831909179688),
            ToCEntry(level=2, title='2.1 Subsection Two.One',
                     pagenum=1, vpos=425.2061462402344),
            ToCEntry(level=1, title='e ln(3)',
                     pagenum=2, vpos=516.01708984375),
            ToCEntry(level=2, title='3.1 Subsection e ln(3) .1, '
                     'with looo- ooooooooong title',
                     pagenum=2, vpos=302.5021057128906),
            ToCEntry(level=2, title='3.2 S ubsection Three.Two, another long title',
                     pagenum=3, vpos=396.212158203125),
            ToCEntry(level=2, title='3.3 Subsection Three.Three',
                     pagenum=3, vpos=68.84815979003906),
            ToCEntry(level=1, title='4 The x → ∞ End',
                     pagenum=3, vpos=483.49920654296875)
        ]

    with it("generates 2-level toc correctly"):
        assert gen_toc(self.level2, self.level2_recipe) == self.level2_expect

    with it("handles headings on same page correctly"):
        assert gen_toc(
            self.onepage, self.onepage_recipe
        ) == self.onepage_expect

    with it("handles math in heading correctly"):
        assert gen_toc(
            self.onepage, self.onepage_recipe
        ) == self.onepage_expect

    with it("handles greedy filter correctly"):
        assert gen_toc(
            self.onepage, self.onepage_greedy
        ) == self.onepage_greedy_expect

    with it("passes the HARD MODE"):
        assert gen_toc(
            self.hardmode, self.hardmode_recipe
        ) == self.hardmode_expect
