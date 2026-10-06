import json, re, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROFILE=ROOT/"examples/marie-curie/profile.json"
GEN=ROOT/"scripts/profile_generator.py"

class GeneratorTests(unittest.TestCase):
    def test_marie_profile_generates_exact_section_geometry(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run([sys.executable,str(GEN),str(PROFILE),"--output",d,"--validate"],check=True)
            out=Path(d)
            for name,w,h in [("header.svg",880,360),("links.svg",880,120),("stats.svg",880,560),("stack.svg",880,360),("footer.svg",880,80)]:
                s=(out/name).read_text()
                self.assertRegex(s,fr'<svg[^>]*width="{w}" height="{h}" viewBox="0 0 {w} {h}"')
            links=sorted((out/"links").glob("*.svg"))
            self.assertEqual(len(links),8)
            self.assertEqual(4*220,880)
            first=links[0].read_text(); fourth=links[3].read_text()
            self.assertIn("M16 0V80",first)
            self.assertIn("M204 0V80",fourth)
            for f in links:
                self.assertRegex(f.read_text(),r'<svg[^>]*width="220" height="80" viewBox="0 0 220 80"')

if __name__=="__main__":
    unittest.main()
