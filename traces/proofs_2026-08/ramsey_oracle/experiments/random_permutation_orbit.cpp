// Random maximal triangle-free H; exact permanent orbit-code lower bound n!/per(bad).
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>
using namespace std;
long double per(const vector<vector<char>>&h){int n=h.size();uint64_t Z=1ULL<<n;vector<long double>d(Z);d[0]=1;for(uint64_t s=0;s<Z;s++){int i=__builtin_popcountll(s);if(i==n||!d[s])continue;for(int j=0;j<n;j++)if(!(s>>j&1)&&(i==j||!h[i][j]))d[s|1ULL<<j]+=d[s];}return d.back();}
int main(int ac,char**av){int n=ac>1?stoi(av[1]):20,T=ac>2?stoi(av[2]):20,seed=ac>3?stoi(av[3]):1;mt19937 R(seed);vector<pair<int,int>> E;for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)E.push_back({i,j});long double best=0,bD=0;int be=0;
for(int t=0;t<T;t++){shuffle(E.begin(),E.end(),R);vector<vector<char>>h(n,vector<char>(n));int e=0;for(auto [u,v]:E){bool tri=0;for(int w=0;w<n;w++)if(h[u][w]&&h[v][w]){tri=1;break;}if(!tri)h[u][v]=h[v][u]=1,e++;}auto D=per(h);auto base=expl((lgammal(n+1)-logl(D))/n);if(base>best)best=base,bD=D,be=e;cout<<t<<" e="<<e<<" base="<<setprecision(10)<<base<<" best="<<best<<"\n";}
cerr<<setprecision(18)<<"BEST n="<<n<<" e="<<be<<" D="<<bD<<" base="<<best<<"\n";}
