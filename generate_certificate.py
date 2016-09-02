# -*- coding: utf-8 -*-

import csv, re
import codecs, hashlib, os.path, unicodedata, string

from subprocess import Popen, PIPE

class Certificate:
  def __init__(self, name):
    svg_filename = 'certificate.svg'
    svg_file = codecs.open(svg_filename, "rb", "utf8")

    svg_content = svg_file.read()

    content = svg_content.replace("%%NOMBRE%%", name.decode('utf-8'))

    self.normalized_name = self._normalize_name(name)
    self.in_file = os.path.join("/tmp", self.normalized_name + ".svg")
    tmp_file = codecs.open(self.in_file, "w", "utf8")
    tmp_file.write(content)
    tmp_file.close()


  def _normalize_name(self, name):
    return re.sub(r"\W+", '_', name).strip().lower()[:30]

  def as_pdf(self):
    inkscape = '/usr/bin/inkscape'
    output_dir = os.getcwd() + '/to_print/pdf'
    if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    out_file = os.path.join(output_dir, self.normalized_name + ".pdf")
    p = Popen([inkscape, '-z', '-f', self.in_file, '-A', out_file], stdin=PIPE, stdout=PIPE)
    p.wait()
    return out_file


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
