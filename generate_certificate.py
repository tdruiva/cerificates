# -*- coding: utf-8 -*-

import csv, re
import codecs, hashlib, os.path, unicodedata, string

from subprocess import Popen, PIPE

class Certificate:
  def __init__(self, name):
    OUT_DIR = '/home/user1/Projects/certificates/to_print'
    svg_filename = 'certificate.svg'
    svg_file = codecs.open(svg_filename, "rb", "utf8")

    svg_content = svg_file.read()

    content = svg_content.replace("%%NOMBRE%%", name.decode('utf-8'))

    normalized_name = self._normalize_name(name)
    self.in_file = os.path.join("/tmp", normalized_name + ".svg")
    tmp_file = codecs.open(self.in_file, "w", "utf8")
    tmp_file.write(content)
    tmp_file.close()

    self.out_file = os.path.join(OUT_DIR + '/pdf', normalized_name + ".pdf")

  def _normalize_name(self, name):
    return re.sub(r"\W+", '_', name).strip().lower()[:30]

  def as_pdf(self):
    inkscape = '/usr/bin/inkscape'
    p = Popen([inkscape, '-z', '-f', self.in_file, '-A', self.out_file], stdin=PIPE, stdout=PIPE)
    p.wait()
    return self.out_file


CSV_PATH = 'names_to_print.csv'

with open(CSV_PATH, "rb") as csv_file:
  rows = csv.reader(csv_file, delimiter='\t')

  for row in rows:
    name = row[0]
    result = Certificate(name).as_pdf()

    if os.path.isfile(result):
      print 'Certificate: ' + name + ' ========= OK'
    else:
      print 'Certificate: ' + name + ' ########## FAIL'
