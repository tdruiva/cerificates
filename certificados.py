# -*- coding: utf-8 -*-

import csv, re
import codecs, hashlib, os.path, unicodedata, string

from subprocess import Popen, PIPE

class Certificate:
  def __init__(self, Certificates, sufix, page):
    Certificate_PATH = '/Users/tsilva/TW/Away_Day/missions/to_print'
    svg_filename = Certificate_PATH + '/missions.svg'

    svg_file = codecs.open(svg_filename, "rb", "utf8")

    content = svg_file.read()

    for index in range(len(Certificates)):
      Certificate = missions[index]
      content = content.replace("%%MISSAO" + str(index) + "%%", Certificate[sufix].decode('utf-8'))

      file_name = 'page_' + str(page) + '_' + sufix

      in_file = os.path.join("/tmp", file_name + ".svg")
      tmp_file = codecs.open(in_file, "w", "utf8")
      tmp_file.write(content)
      tmp_file.close()

      out_file = os.path.join(Certificate_PATH + '/pdf', file_name + ".svg")
      pdf_file = self._svg_to_pdf(in_file, out_file)

      if os.path.isfile(out_file):
        print 'Certificate: ' + file_name + ' ========= OK'
      else:
        print 'Certificate: ' + file_name + ' ########## FAIL'

  def normalize_name(self, name):
    name = re.sub(r"\W+", '_', name).strip().lower()
    return name[:30].rsplit(' ', 1)[0]

  def generate_hash(self, xid):
    ret = hashlib.sha224(xid).hexdigest()[:8]
    return ret

  def _svg_to_pdf(self, in_file, out_file):
    inkscape = '/Applications/Inkscape.app/Contents/Resources/bin/inkscape'
    p = Popen([inkscape, '-z', '-f', in_file, '-l', out_file], stdin=PIPE, stdout=PIPE)
    p.wait()
    return out_file


CSV_PATH = '/Users/tsilva/TW/Away_Day/Certificates.csv'
Certificates = []

with open(CSV_PATH, "rb") as csv_file:
  rows = csv.reader(csv_file, delimiter='\t')

  for row in rows:
    language_1 = row[1]
    language_2 = row[4]

    Certificates.append({
      'first': language_1,
      'second': language_2
    })

data = []
page = 1;
for index in range(len(Certificates)):
  data.append(Certificates[index])

  if len(data) == 10 or index == len(Certificates) - 1:
    Certificate(data, 'first', page)
    Certificate(data, 'second', page)
    page += 1
    data = []

