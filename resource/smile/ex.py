m = "XUBdTFdScw5XCVRGTglJXEpMSFpOQE5AVVxJBRpLT10aYBpIVwlbCVZATl1WTBpaTkBOQFVcSQdH"
m = map(ord, m.decode("base64"))

idx = 0
mask = ":)"

r = ""
for c in m:
	r += chr(c ^ ord(mask[idx]))
	idx = 1 - idx

print r
