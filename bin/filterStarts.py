#!/usr/bin/env python
# Author: Tomas Bruna

# Filter out starts which are overlapped by at least CDSCoverageThreshold CDS
# alignments. CDS regions which start before a start starting coordinate and end
# after a start ending coordinate are considered to be overlapping. Both input
# files (start codons and CDS coordinates in gff format) need to be sorted by
# chromosome, start and end. For example like this: sort -k1,1 -k4,4n -k5,5n
# starts.gff > starts_sorted.gff.
#
# positional arguments:
#   starts.gff            Sorted start codons in gff format.
#   cds.gff               Sorted CDS regions in gff format. If the 6th score
#                         column contains a number, this number is treated as
#                         coverage of the given CDS region.
#   CDSCoverageThreshold  CDS overlap threshold. Starts with maxCDSCoverage or
#                         more overlapping CDS regions are filtered out.
#
# optional arguments:
#   -h, --help            show this help message and exit


import csv
import argparse


class CDS:

    def __init__(self, start, end, coverage):
        self.start = start
        self.end = end
        self.coverage = coverage


def loadCDS(cdsFileName):
    codingSegments = {}
    cdsFile = open(cdsFileName)
    cdses = csv.reader(cdsFile, delimiter='\t')
    for row in cdses:
        if not row[0] in codingSegments:
            codingSegments[row[0]] = []

        coverage = 1
        if row[5] != ".":
            coverage = int(row[5])

        codingSegments[row[0]].append(CDS(int(row[3]),
                                      int(row[4]), coverage))
    cdsFile.close()
    return codingSegments


def filterStarts(startsFileName, cdsFileName, threshold):
    codingSegments = loadCDS(cdsFileName)

    startsFile = open(startsFileName)
    starts = csv.reader(startsFile, delimiter='\t')

    prevChromosome = ""
    CDSpointer = 0
    CDSNum = 0

    for start in starts:
        chrom = start[0]
        startStart = int(start[3])
        startEnd = int(start[4])

        if prevChromosome != chrom:
            CDSpointer = 0
            CDSNum = len(codingSegments[chrom])

        while (CDSpointer < CDSNum and
               codingSegments[chrom][CDSpointer].end <= startEnd):
            # Shift CDS starting point to first CDS which can overlap
            # with any of the subsequent starts
            CDSpointer += 1

        startOverlaps = 0
        i = CDSpointer
        while i < CDSNum and codingSegments[chrom][i].start < startStart:
            # While any CDS starts before the current start
            if (codingSegments[chrom][i].start < startStart
               and codingSegments[chrom][i].end > startEnd):
                startOverlaps += codingSegments[chrom][i].coverage
            i += 1

        if startOverlaps < threshold:
            print("\t".join(start))

        prevChromosome = chrom

    startsFile.close()


def main():
    args = parseCmd()
    filterStarts(args.starts, args.cds, args.coverage)


def parseCmd():

    parser = argparse.ArgumentParser(description='Filter out starts which are \
        overlapped by at least CDSCoverageThreshold CDS alignments. CDS regions which start \
        before a start starting coordinate and end after a start ending coordinate \
        are considered to be overlapping. Both input files (start codons and CDS \
        coordinates in gff format) need to be sorted by chromosome, start and end. \
        For example like this: sort -k1,1 -k4,4n -k5,5n starts.gff > starts_sorted.gff.')

    parser.add_argument('starts', metavar='starts.gff', type=str,
                        help='Sorted start codons in gff format.')
    parser.add_argument('cds', metavar='cds.gff', type=str,
                        help='Sorted CDS regions in gff format. If the 6th score column \
                        contains a number, this number is treated as coverage of the \
                        given CDS region.')
    parser.add_argument('coverage', metavar='CDSCoverageThreshold', type=int,
                        help='CDS overlap threshold. Starts with maxCDSCoverage \
                        or more overlapping CDS regions are filtered out.')

    return parser.parse_args()


if __name__ == '__main__':
    main()
