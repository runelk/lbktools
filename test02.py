
import lbktools

out1, err1 = lbktools.run_mtag('Hei du der!')
print out1

print '------------------------------------------------'

out2, err2 = lbktools.run_cg3(out1)
print out2

print '------------------------------------------------'

out3, err3 = lbktools.run_stat(out2)
print out3
