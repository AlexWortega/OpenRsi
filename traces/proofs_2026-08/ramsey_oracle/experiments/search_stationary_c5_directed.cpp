// Exhaust all directed C5-state automata of row outdegree <=2 (loops allowed).
// Exact uint64 transfer counts for q=2..8.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
using Mat = std::vector<std::vector<uint64_t>>;
Mat mul(const Mat&a,const Mat&b){int n=a.size(); Mat c(n,std::vector<uint64_t>(n)); for(int i=0;i<n;i++)for(int k=0;k<n;k++)if(a[i][k])for(int j=0;j<n;j++)c[i][j]+=a[i][k]*b[k][j]; return c;}
uint64_t tr(const Mat&a){uint64_t s=0;for(int i=0;i<(int)a.size();i++)s+=a[i][i];return s;}
int main(){
 const int n=5,Q=8; bool H[n][n]={}; for(int i=0;i<n;i++)H[i][(i+1)%n]=H[(i+1)%n][i]=1;
 std::vector<std::pair<int,int>> P; for(int u=0;u<n;u++)for(int v=0;v<n;v++)if(!H[u][v])P.push_back({u,v});
 std::vector<int> opts; for(int m=0;m<(1<<n);m++)if(__builtin_popcount((unsigned)m)<=2)opts.push_back(m);
 std::array<uint64_t,Q+1> best{}, count{}; std::array<std::array<int,n>,Q+1> besta{};
 uint64_t total=1;for(int i=0;i<n;i++)total*=opts.size();
 for(uint64_t code=0;code<total;code++){
   uint64_t z=code; int rows[n]; Mat A(n,std::vector<uint64_t>(n));
   for(int i=0;i<n;i++){rows[i]=opts[z%opts.size()];z/=opts.size();for(int j=0;j<n;j++)A[i][j]=(rows[i]>>j)&1;}
   Mat B(P.size(),std::vector<uint64_t>(P.size()));
   for(int i=0;i<(int)P.size();i++)for(int j=0;j<(int)P.size();j++)B[i][j]=A[P[i].first][P[j].first]*A[P[i].second][P[j].second];
   Mat Ap=A,Bp=B;
   for(int q=1;q<=Q;q++){
     if(q>=2){uint64_t w=tr(Ap),wb=tr(Bp);if(wb==w){count[q]++;if(w>best[q]){best[q]=w;for(int i=0;i<n;i++)besta[q][i]=rows[i];}}}
     Ap=mul(Ap,A);Bp=mul(Bp,B);
   }
 }
 std::cout<<"enumerated "<<total<<" automata\n";
 for(int q=2;q<=Q;q++){std::cout<<"q="<<q<<" feasible="<<count[q]<<" bestW="<<best[q]<<" rows";for(int x:besta[q])std::cout<<" "<<x;std::cout<<"\n";}
}
