# -*- coding: utf-8 -*-
import os


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_CORE = os.path.join(APP_ROOT, 'core')


def readRelevancy():
    rel = []
    with open(os.path.join(APP_CORE, "relevancy.txt"), "r") as f:
        for line in f:
            line = line.strip()
            rel.append(str.split(line, ' '))
    return rel


relevancy = readRelevancy()

if __name__ == '__main__':
    print relevancy
