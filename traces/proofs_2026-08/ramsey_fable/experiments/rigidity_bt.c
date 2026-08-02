/* Exhaustive backtracking refutation for the locally-3 K_16 rigidity theorem.
 *
 * Input (argv): m0 m1 m2 m3  — the missing-color group sizes (sum 16).
 * Vertices 0..15; vertex v's missing color = group[v] (first m0 vertices miss
 * color 0, etc.). Searches for an edge coloring of K_16 with:
 *   - edge (u,v) colored c in {0..3}, c != group[u], c != group[v];
 *   - no monochromatic triangle;
 *   - every vertex exactly 5-regular in each of its 3 allowed colors.
 * Prints FOUND + the coloring if one exists, else REFUTED + node count.
 * Exit code: 0 = refuted, 1 = found, 2 = error.
 *
 * Correctness of the regularity constraint: any locally-3 triangle-free K_16
 * is extremal (L_3 = 16 = 1 + 3 L_2), and the round1 equality lemma forces
 * exactly 3 incident colors with classes of size exactly 5 at every vertex.
 * So imposing 5-regularity loses no solutions.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 16
#define E 120

static int group_[N];
static int eu[E], ev[E];
static int dom[E][3], domn[E];
static signed char cmat[N][N];
static int deg[N][4];
static int remcap[N][4];
static long long nodes = 0;

static int bt(int i) {
    nodes++;
    if (i == E) return 1;
    int u = eu[i], v = ev[i];
    /* remove this edge from remcap */
    for (int t = 0; t < domn[i]; t++) {
        int c = dom[i][t];
        remcap[u][c]--; remcap[v][c]--;
    }
    for (int t = 0; t < domn[i]; t++) {
        int c = dom[i][t];
        if (deg[u][c] >= 5 || deg[v][c] >= 5) continue;
        int bad = 0;
        for (int w = 0; w < N; w++)
            if (cmat[u][w] == c && cmat[v][w] == c) { bad = 1; break; }
        if (bad) continue;
        deg[u][c]++; deg[v][c]++;
        cmat[u][v] = cmat[v][u] = (signed char)c;
        int ok = 1;
        for (int s = 0; s < 2 && ok; s++) {
            int x = s ? v : u;
            for (int cc = 0; cc < 4; cc++) {
                if (cc == group_[x]) continue;
                if (deg[x][cc] + remcap[x][cc] < 5) { ok = 0; break; }
            }
        }
        if (ok && bt(i + 1)) return 1;
        deg[u][c]--; deg[v][c]--;
        cmat[u][v] = cmat[v][u] = -1;
    }
    for (int t = 0; t < domn[i]; t++) {
        int c = dom[i][t];
        remcap[u][c]++; remcap[v][c]++;
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 5) { fprintf(stderr, "usage: rigidity_bt m0 m1 m2 m3\n"); return 2; }
    int idx = 0, sum = 0;
    for (int c = 0; c < 4; c++) {
        int m = atoi(argv[c + 1]);
        sum += m;
        for (int j = 0; j < m; j++) group_[idx++] = c;
    }
    if (sum != N) { fprintf(stderr, "sizes must sum to 16\n"); return 2; }
    int e = 0;
    for (int u = 0; u < N; u++)
        for (int v = u + 1; v < N; v++) {
            eu[e] = u; ev[e] = v;
            domn[e] = 0;
            for (int c = 0; c < 4; c++)
                if (c != group_[u] && c != group_[v]) dom[e][domn[e]++] = c;
            e++;
        }
    memset(cmat, -1, sizeof cmat);
    memset(deg, 0, sizeof deg);
    memset(remcap, 0, sizeof remcap);
    for (int i = 0; i < E; i++)
        for (int t = 0; t < domn[i]; t++) {
            remcap[eu[i]][dom[i][t]]++;
            remcap[ev[i]][dom[i][t]]++;
        }
    if (bt(0)) {
        printf("FOUND\n");
        for (int u2 = 0; u2 < N; u2++)
            for (int v2 = u2 + 1; v2 < N; v2++)
                printf("%d %d %d\n", u2, v2, cmat[u2][v2]);
        return 1;
    }
    printf("REFUTED nodes=%lld\n", nodes);
    return 0;
}
