import angr
from pwn import *
find_addr = 0x400e58

proj = angr.Project("./prodkey", auto_load_libs=False)

sm = proj.factory.simulation_manager()
sm.explore(find = find_addr)

s = sm.found[0].state.posix.dumps(0)

print "found : " + s[:30]

r = remote("rev.tamuctf.com", 8189)

r.sendlineafter("continue:", "".join(s))

r.interactive()

r.close()
