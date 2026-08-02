// Exact permanent ratio for permutation-word codes on C5/Mycielski graphs.
// A greedy independent set among all n! permutation words has size >= n!/D,
// D=per(M), M_uv=1 iff u=v or uv is a nonedge of triangle-free H.
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
vector<vector<int>> cycle5(){vector<vector<int>> a(5,vector<int>(5));for(int i=0;i<5;i++)a[i][(i+1)%5]=a[(i+1)%5][i]=1;return a;}
vector<vector<int>> myc(vector<vector<int>> a){int n=a.size(),N=2*n+1;vector<vector<int>> b(N,vector<int>(N));for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(a[i][j]){b[i][j]=1;b[i][n+j]=1;b[n+i][j]=1;}for(int i=0;i<n;i++)b[n+i][2*n]=b[2*n][n+i]=1;return b;}
long double permanent(const vector<vector<int>>& H){int n=H.size();uint64_t Z=1ULL<<n;vector<long double> dp(Z);dp[0]=1;for(uint64_t s=0;s<Z;s++){int i=__builtin_popcountll(s);if(i==n)continue;auto v=dp[s];if(!v)continue;for(int j=0;j<n;j++)if(!(s>>j&1) && (i==j || !H[i][j]))dp[s|1ULL<<j]+=v;}return dp.back();}
int main(int argc,char**argv){int lev=argc>1?stoi(argv[1]):2;auto H=cycle5();for(int i=0;i<lev;i++)H=myc(H);int n=H.size();if(n>=63){cerr<<"too large\n";return 2;}long double D=permanent(H),lf=lgammal(n+1),logN=lf-logl(D);cout<<setprecision(18)<<"n="<<n<<" D="<<D<<" log(n!/D)="<<logN<<" base="<<expl(logN/n)<<"\n";}
