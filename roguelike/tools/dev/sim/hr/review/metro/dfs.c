/* review H-A HA-03 (lane HFA): exhaustive DFS over gauntlet strike sets (as fm.c's rules): every metronome of period 8-30 and
   every start >= -200 gets at most MAXPP perfect parries. Prunes a prefix as soon as one train exceeds MAXPP (the model is
   causal: later strikes never change earlier results).
   gcc -O2 -o dfs dfs.c
   ./dfs N S1LO S1HI SNHI GAPMAX MAXPP base1..baseN gmin1..gmin(N-1)
   G1 (11-11): ./dfs 9 28 34 199 30 3 30 46 64 94 110 138 164 180 196 -> 33 311 sets (the nearest: 30 48 64 91 109 139 163 180 196)
   G2 (11-11): ./dfs 11 21 32 221 50 3 30 44 58 86 114 128 156 172 186 200 216 14 14 24 20 14 23 14 14 14 14 -> none
   (the gmins: chain cuts 14; a reappearance only after the vanish before it: the leap 24, the ring 20, the X 23) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define KMIN 8
#define KMAX 30
#define NK (KMAX - KMIN + 1)
#define LO (-200)
#define TMAX 260
#define NT (TMAX - LO + 1)
typedef struct { int parAt, parLk, parHit, parMl, ws, pp, nextp; } St;
static St *ST;            /* [depth][NK][NT] */
static int N, S1LO, S1HI, SNHI, GAPMAX, MAXPP, base[32], seq[32], nsol = 0, best_d = 1 << 30, bestseq[32];
static long nodes = 0;
static int GMIN[32], REST[33];
#define IDX(d, k, t) (((size_t)(d) * NK + (k)) * NT + (t))
static void press(St *s, int t) {
    if (t < s->parLk || t < s->parMl) { s->parMl = t + 3; return; }
    int d = t - s->parAt;
    if (s->parHit < s->parAt && d <= 80 && s->ws < 3) s->ws++;
    if (d > 80) s->ws = 0;
    s->parAt = t; s->parLk = t + 12 * (1 + s->ws);
}
static int strike(St *s, int st) {
    int jp = st - s->parAt;
    int usable = (s->parHit < s->parAt || s->parHit == st) && jp >= 0, tier = 0;
    if (usable && jp < 3) tier = 3; else if (usable && jp < 6) tier = 2; else if (usable && jp < 10) tier = 1;
    if (tier) { s->parHit = st; s->parLk = st + 1; if (tier >= 2) s->ws = 0; }
    return tier == 3;
}
static void dfs(int d, int prev) {
    int lo = d == 0 ? S1LO : prev + GMIN[d - 1], hi = d == 0 ? S1HI : prev + GAPMAX;
    if (hi > SNHI - REST[d]) hi = SNHI - REST[d];
    for (int sn = lo; sn <= hi; sn++) {
        nodes++;
        int bad = 0;
        for (int k = 0; k < NK && !bad; k++) {
            int per = KMIN + k;
            for (int t = 0; t < NT; t++) {
                St s = ST[IDX(d, k, t)];
                int t0 = LO + t;
                if (t0 <= sn) {
                    while (s.nextp <= sn) { press(&s, s.nextp); s.nextp += per; }
                    s.pp += strike(&s, sn);
                    if (s.pp > MAXPP) { bad = 1; break; }
                }
                ST[IDX(d + 1, k, t)] = s;
            }
        }
        if (bad) continue;
        seq[d] = sn;
        if (d + 1 == N) {
            int dist = 0;
            for (int i = 0; i < N; i++) dist += abs(seq[i] - base[i]);
            nsol++;
            if (dist < best_d) {
                best_d = dist; memcpy(bestseq, seq, sizeof(int) * N);
                printf("sol %d dist %d:", nsol, dist);
                for (int i = 0; i < N; i++) printf(" %d", seq[i]);
                printf("  (nodes %ld)\n", nodes); fflush(stdout);
            }
        } else dfs(d + 1, sn);
    }
}
int main(int argc, char **argv) {
    N = atoi(argv[1]); S1LO = atoi(argv[2]); S1HI = atoi(argv[3]); SNHI = atoi(argv[4]); GAPMAX = atoi(argv[5]); MAXPP = atoi(argv[6]);
    for (int i = 0; i < N; i++) base[i] = argc > 7 + i ? atoi(argv[7 + i]) : 0;
    for (int i = 0; i < N - 1; i++) GMIN[i] = argc > 7 + N + i ? atoi(argv[7 + N + i]) : 14;
    REST[N - 1] = 0;
    for (int d = N - 2; d >= 0; d--) REST[d] = REST[d + 1] + GMIN[d];
    ST = malloc(sizeof(St) * (size_t)(N + 1) * NK * NT);
    for (int k = 0; k < NK; k++) for (int t = 0; t < NT; t++) {
        St s = { -1000000, -1000000, -1000000, -1000000, 0, 0, LO + t };
        ST[IDX(0, k, t)] = s;
    }
    dfs(0, 0);
    printf("done: %d solutions, %ld nodes\n", nsol, nodes);
    return 0;
}
