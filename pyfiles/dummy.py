import sys

if __name__ == "__main__":
    print "HELLO WORLD"
    fetchnum=50
    arglst = sys.argv

    if len(arglst)==3:
        fetchnum = int(arglst[2])
    if len(arglst)>=2:
        print fetchnum
        print arglst[1]
