#! /usr/bin/env python

# Simple EZID command line client.  The output is UTF-8 encoded and by
# default is left in %-encoded form.
#
# Usage: ezid.py [options] credentials operation...
#
#   options:
#     -d decode output
#     -o one line per value: convert newlines to spaces
#     -t format timestamps
#
#   credentials:
#     username:password
#     sessionid (as returned by previous login)
#     - (none)
#
#   operation:
#     m[int] shoulder [label value label value ...]
#     c[reate] identifier [label value label value ...]
#     v[iew] identifier
#     u[pdate] identifier [label value label value ...]
#     d[elete] identifier
#     login
#     logout
#     s[tatus] [*|subsystemlist]
#
# In the above, if a label is "@", the associated value is treated as
# a filename and metadata fields are read from the named
# ANVL-formatted file.  For example, if file metadata.txt contains:
#
#   erc.who: Proust, Marcel
#   erc.what: Remembrance of Things Past
#   erc.when: 1922
#
# then an identifier with that metadata can be minted by invoking:
#
#   ezid.py p username:password mint ark:/99999/fk4 @ metadata.txt
#
# Otherwise, if a value has the form "@filename", a (single) value is
# read from the named file.  For example, if file metadata.xml
# contains a DataCite XML record, then an identifier with that record
# as the value of the 'datacite' field can be minted by invoking:
#
#   ezid.py p username:password mint doi:10.5072/FK2 datacite @metadata.xml
#
# In both of the above cases, the contents of the named file are
# assumed to be UTF-8 encoded.  And in both cases, the interpretation
# of @ can be defeated by doubling it.
#
# Greg Janee <gjanee@ucop.edu>
# April 2011

import codecs
import re
import sys
import time
import types
import urllib
import urllib2

knownServers = {
  "l" : "REDACTED",
  "d" : "REDACTED",
  "s" : "REDACTED",
  "w" : "REDACTED",
  "p" : "http://n2t.net/ezid"
}

operations = {
  # operation : number of arguments
  "mint" : lambda l: l%2 == 1,
  "create" : lambda l: l%2 == 1,
  "view" : 1,
  "update" : lambda l: l%2 == 1,
  "delete" : 1,
  "login" : 0,
  "logout" : 0,
  "status" : lambda l: l in [0, 1]
}

usageText = """Usage: %s [options] credentials operation...

  options:
    -d decode output
    -o one line per value: convert newlines to spaces
    -t format timestamps

  credentials:
    username:password
    sessionid (as returned by previous login)
    - (none)

  operation:
    m[int] shoulder [label value label value ...]
    c[reate] identifier [label value label value ...]
    v[iew] identifier
    u[pdate] identifier [label value label value ...]
    d[elete] identifier
    login
    logout
    s[tatus] [*|subsystemlist]
"""

def usageError ():
  sys.stderr.write(usageText % sys.argv[0])
  sys.exit(1)

class MyHTTPErrorProcessor (urllib2.HTTPErrorProcessor):
  def http_response (self, request, response):
    # Bizarre that Python leaves this out.
    if response.code == 201:
      return response
    else:
      return urllib2.HTTPErrorProcessor.http_response(self, request, response)
  https_response = http_response

def formatAnvl (l):
  r = []
  for i in range(0, len(l), 2):
    k = l[i]
    if k == "@":
      f = codecs.open(l[i+1], encoding="UTF-8")
      r.extend(ll.strip() for ll in f.readlines())
      f.close()
    else:
      if k == "@@":
        k = "@"
      else:
        k = re.sub("[%:\r\n]", lambda c: "%%%02X" % ord(c.group(0)), k)
      v = l[i+1]
      if v.startswith("@@"):
        v = v[1:]
      elif v.startswith("@") and len(v) > 1:
        f = codecs.open(v[1:], encoding="UTF-8")
        v = f.read()
        f.close()
      v = re.sub("[%\r\n]", lambda c: "%%%02X" % ord(c.group(0)), v)
      r.append("%s: %s" % (k, v))
  return "\n".join(r)

# Process command line arguments.

decodeOutput = False
oneLine = False
formatTimestamps = False
while len(sys.argv) >= 2 and sys.argv[1].startswith("-") and\
  len(sys.argv[1]) > 1:
  for c in sys.argv[1][1:]:
    if c == "d":
      decodeOutput = True
    elif c == "o":
      oneLine = True
    elif c == "t":
      formatTimestamps = True
    else:
      usageError()
  del sys.argv[1]
# Mimic the selection of the production server (server selection is
# not supported in this public version of the code).
sys.argv.insert(1, "p")
if len(sys.argv) < 4: usageError()
server = knownServers.get(sys.argv[1], sys.argv[1])
opener = urllib2.build_opener(MyHTTPErrorProcessor())
if ":" in sys.argv[2]:
  if server.startswith("http:") and sys.argv[1] != "l":
    server = "https" + server[4:]
  h = urllib2.HTTPBasicAuthHandler()
  h.add_password("EZID", server, *sys.argv[2].split(":", 1))
  opener.add_handler(h)
  cookie = None
elif sys.argv[2] != "-":
  cookie = "sessionid=" + sys.argv[2]
else:
  cookie = None
operation = [o for o in operations if o.startswith(sys.argv[3])]
if len(operation) != 1: usageError()
operation = operation[0]
if (type(operations[operation]) is int and\
  len(sys.argv)-4 != operations[operation]) or\
  (type(operations[operation]) is types.LambdaType and\
  not operations[operation](len(sys.argv)-4)): usageError()

# Assemble the request.

if operation in ["mint", "create", "update"]:
  path = "shoulder" if operation == "mint" else "id"
  arg = urllib.quote(sys.argv[4], ":/")
  request = urllib2.Request("%s/%s/%s" % (server, path, arg))
  request.get_method = lambda: "PUT" if operation == "create" else "POST"
  if len(sys.argv) > 5:
    request.add_header("Content-Type", "text/plain; charset=UTF-8")
    request.add_data(formatAnvl(sys.argv[5:]).encode("UTF-8"))
elif operation == "view":
  id = urllib.quote(sys.argv[4], ":/")
  request = urllib2.Request("%s/id/%s" % (server, id))
elif operation == "delete":
  id = urllib.quote(sys.argv[4], ":/")
  request = urllib2.Request("%s/id/%s" % (server, id))
  request.get_method = lambda: "DELETE"
elif operation in ["login", "logout"]:
  request = urllib2.Request("%s/%s" % (server, operation))
elif operation == "status":
  if len(sys.argv) > 4:
    s = "?subsystems=" + sys.argv[4]
  else:
    s = ""
  request = urllib2.Request("%s/status%s" % (server, s))

if cookie: request.add_header("Cookie", cookie)

# Issue the request and output the return.

try:
  c = opener.open(request)
  output = c.read()
  if not output.endswith("\n"): output += "\n"
  if operation == "login":
    output += c.info()["set-cookie"].split(";")[0].split("=")[1] + "\n"
except urllib2.HTTPError, e:
  sys.stderr.write("%s %s\n" % (e.code, e.msg))
  output = e.fp.read()
  if not output.endswith("\n"): output += "\n"
  sys.stderr.write(output)
else:
  output = output.splitlines()
  if operation == "view":
    # Just a nicety.
    statusLine = output[0]
    output = output[1:]
    output.sort()
    output.insert(0, statusLine)
  for l in output:
    if formatTimestamps and (l.startswith("_created:") or\
      l.startswith("_updated:")):
      ls = l.split(":")
      l = ls[0] + ": " + time.strftime("%Y-%m-%dT%H:%M:%S",
        time.localtime(int(ls[1])))
    if decodeOutput:
      l = re.sub("%([0-9a-fA-F][0-9a-fA-F])",
        lambda m: chr(int(m.group(1), 16)), l)
    if oneLine: l = l.replace("\n", " ").replace("\r", " ")
    print l