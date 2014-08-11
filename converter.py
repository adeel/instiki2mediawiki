# converter.py

import os.path
import re
import cgi
import sys
import subprocess

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

category_regex = re.compile(r"(:)?category\s*:(.*)", re.IGNORECASE)
redirect_regex = re.compile(r"\[\[\!redirects\s+([^\]\s][^\]]*?)\s*\]\]", re.IGNORECASE)
toc_regex = re.compile(r"\=\s*Contents\s*\=\s*\n*\s*\*\s*table of contents", re.IGNORECASE)

def remove_tocs(contents):
  return toc_regex.sub("", contents)

def title_to_wiki_style(s):
  s = s.strip()
  if len(s) == 0:
    return s
  return s[0].upper() + s[1:]

def category_to_wiki_style(c):
  return "[[Category:%s]]" % cgi.escape(title_to_wiki_style(c))

def replace_category(match):
  return "\n".join(map(category_to_wiki_style, match.group(2).split(',')))

def replace_categories(input):
  return category_regex.sub(replace_category, input)

def get_redirects(contents):
  return map(lambda x: title_to_wiki_style(x.group(1)),
    redirect_regex.finditer(contents))

def remove_redirects(contents):
  return redirect_regex.sub("", contents)

def register_redirect(s, t, register):
  if s and t and s != t:
    if s not in register.keys():
      register[s] = t

def get_page_list(dir):
  return map(lambda x: dir + "/" + x.replace(".meta", ""),
    filter(lambda x: x.endswith(".meta"), os.listdir(dir)))

def get_page_title(p):
  meta = open(p + ".meta", 'r').read()
  r = re.compile(r"name\s*:(.*)", re.IGNORECASE)
  ms = r.findall(meta)
  if not ms:
    return
  else:
    return title_to_wiki_style(ms[-1])

def write_redirects_register(register, path):
  open(path, 'w').write("\n".join(
    ["%s -> %s" % (s, t) for s, t in register.items()]))

def convert_markdown_to_wiki_syntax(path):
  subprocess.call("maruku --wiki --math-engine none %s" % path)

def get_db_session(url):
  return sessionmaker(
    bind=create_engine('sqlite:///../instiki/db/production.db.sqlite3'))()

def process_revision(r, p, w, processed):
  """
  Processes an individual revision, and returns the new state of the 
  processed data.
  TODO: At the moment, this does nothing.
  """
  if not processed.get(w.address):
    processed[w.address] = {}
  if not processed[w.address].get(p.id):
    processed[w.address][p.id] = {}
  if not processed[w.address][p.id].get(r.id):
    processed[w.address][p.id][r.id] = {}
  processed[w.address][p.id][r.id] = r.__dict__

def convert(options):
  """
  Accepts the following options (all required):
    `instiki_db`: a database connection url for the Instiki installation
    `mediawiki_db`: a database connection url for the MediaWiki installation
    `main_web`: the address of the main web of the Instiki installation, which
                is to become the default namespace of the MediaWiki
                installation
  Given this data it processes each revision of each page of the main web of
  the Instiki installation, and converts it to MediaWiki syntax.  After
  processing is complete, it saves all the data into the database which
  `mediawiki_db` points to.
  """
  in_db_url = options.get("instiki_db")
  mw_db_url = options.get("mediawiki_db")
  main_web_addr = options.get("main_web")

  in_db = get_db_session(in_db_url)
  mw_db = get_db_session(mw_db_url)
  main_web = in_db.query(Web).filter_by(address=main_web_addr).first()
  if not main_web:
    raise Exception("No web could be found with the address '%s'." % main_web_addr)

  processed = {}
  for p in main_web.pages:
    for r in p.revisions:
      processed = parse_revision(r, p, main_web, processed)

  # TODO: save to MediaWiki database

  ## old script:
  # redir_register = {}

  # for p in get_page_list(indir):
  #   x = open(p, 'r').read()

  #   x = remove_tocs(x)

  #   rs = get_redirects(x)
  #   x = remove_redirects(x)
  #   [register_redirect(r, get_page_title(p), redir_register) for r in rs]

  #   x = replace_categories(x)

  #   path = outdir + "/" + os.path.basename(p)
  #   open(path, 'w').write(x)

  #   convert_markdown_to_wiki_syntax(path)

  # write_redirects_register(redir_register, "redirects.txt")
