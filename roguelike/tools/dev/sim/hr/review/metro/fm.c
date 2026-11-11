/* review H-A HA-03 (lane HFA, 11-11): the shipped F rules (player/f_key -> press | press_re, the judge -> par_use; load.mcfunction
   #parGap 12 #parWsMax 3 #parWsT 80 #parWsClr 2 #parRe 3 #parChain 1, windows 3 / 6 / 10) against a gauntlet's strike ticks, for
   every metronome period and start. tests/test_metro.py checks the same thing with the real functions; this is the fast
   model the search tools use (it agreed with test_metro on every period of the old and new G1 / G2).
   gcc -O2 -shared -fPIC -o fm.so fm.c   (metro.py does it when fm.so is missing) */
#define GAP 12
#define WSMAX 3
#define WST 80
#define WSCLR 2
#define RE 3
#define CHAIN 1
static int run1(const int *s, int n, int t0, int k, int end) {
    long parAt = -1000000, parLk = -1000000, parHit = -1000000, parMl = -1000000;
    int ws = 0, pp = 0, j = 0;
    long t = t0;
    while (1) {
        long nextp = (t <= end) ? t : 1L << 40;
        long nexts = (j < n) ? s[j] : 1L << 40;
        if (nextp == (1L << 40) && nexts == (1L << 40)) break;
        if (nextp <= nexts) {             /* press first in its tick */
            if (nextp < parLk || nextp < parMl) parMl = nextp + RE;
            else {
                long d = nextp - parAt;
                if (parHit < parAt && d <= WST && ws < WSMAX) ws++;
                if (d > WST) ws = 0;
                parAt = nextp; parLk = nextp + GAP * (1 + ws);
            }
            t += k;
        } else {
            long st = nexts, jp = st - parAt;
            int usable = (parHit < parAt || parHit == st) && jp >= 0, tier = 0;
            if (usable && jp < 3) tier = 3; else if (usable && jp < 6) tier = 2; else if (usable && jp < 10) tier = 1;
            if (tier) { parHit = st; parLk = st + CHAIN; if (tier >= WSCLR) ws = 0; }
            if (tier == 3) pp++;
            j++;
        }
    }
    return pp;
}
int eval(const int *s, int n, int kmin, int kmax, int lo, int *maxk, int *c4, int *c5) {
    int end = s[n - 1], worst = 0;
    for (int k = kmin; k <= kmax; k++) {
        int m = 0, a = 0, b = 0;
        for (int t0 = lo; t0 <= end; t0++) {
            int pp = run1(s, n, t0, k, end);
            if (pp > m) m = pp;
            if (pp >= 4) a++;
            if (pp >= 5) b++;
        }
        maxk[k - kmin] = m; c4[k - kmin] = a; c5[k - kmin] = b;
        if (m > worst) worst = m;
    }
    return worst;
}
