#!/usr/bin/env python3
# Author: Tomas Bruna

import unittest
import os
import subprocess
import shutil
import common


class TestProtHint(unittest.TestCase):

    def testProtHint(self):
        os.chdir(testDir + "/test_ProtHint")

        subprocess.call("../../bin/prothint.py genome.fasta proteins.fasta --geneMarkGtf genemark.gtf \
                        --workdir output --cleanup", shell=True)

        self.assertEqual(common.compareFiles("output/prothint.gff", "test_output/prothint.gff"), 0)
        self.assertEqual(common.compareFiles("output/evidence.gff", "test_output/evidence.gff"), 0)

        shutil.rmtree("output")

    def testProtHintNoShortExons(self):
        os.chdir(testDir + "/test_ProtHint")

        subprocess.call("../../bin/prothint.py genome.fasta proteins.fasta --geneMarkGtf genemark.gtf \
                        --workdir output_no_short --cleanup --minInitialExonScore 25", shell=True)

        self.assertEqual(common.compareFiles("output_no_short/prothint.gff", "test_output_no_short/prothint.gff"), 0)
        self.assertEqual(common.compareFiles("output_no_short/evidence.gff", "test_output_no_short/evidence.gff"), 0)

        shutil.rmtree("output_no_short")


if __name__ == '__main__':
    testDir = os.path.abspath(os.path.dirname(__file__))
    unittest.main()
