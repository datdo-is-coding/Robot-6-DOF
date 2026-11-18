#include <vector>
#include <queue>
#include <cmath>
#include <cstdint>
#include <limits>
#include <algorithm>
struct Entry {float f,g;int id; bool operator<(const Entry& z)const{return f>z.f;}};
extern "C" int search_grid(const uint8_t* blocked,const uint8_t* via,int n,
 const int* starts,int ns,const int* goals,int ng,int* result,int capacity) {
 const int plane=n*n,total=4*plane;
 std::vector<float> cost(total,std::numeric_limits<float>::infinity());
 std::vector<int> parent(total,-2);
 std::priority_queue<Entry> heap;
 auto h=[&](int id){int x=id%n,y=(id/n)%n;float best=1e30;
  for(int k=0;k<ng;k++){int dx=std::abs(x-goals[k]%n),dy=std::abs(y-(goals[k]/n)%n);
   best=std::min(best,float(10*std::max(dx,dy)+4.142136*std::min(dx,dy)));}return best;};
 for(int k=0;k<ns;k++){cost[starts[k]]=0;parent[starts[k]]=-1;heap.push({h(starts[k]),0,starts[k]});}
 const int dx[]={1,-1,0,0,1,1,-1,-1},dy[]={0,0,1,-1,1,-1,1,-1};
 while(!heap.empty()){
  auto e=heap.top();heap.pop();int id=e.id;
  if(e.g!=cost[id])continue;
  for(int k=0;k<ng;k++)if(id==goals[k]){
   int count=0;for(int q=id;q!=-1;q=parent[q]){if(count==capacity)return -2;result[count++]=q;}
   std::reverse(result,result+count);return count;}
  int layer=id/plane,cell=id%plane,x=cell%n,y=cell/n;
  auto visit=[&](int next,float dc){float g=e.g+dc;if(g+.00001<cost[next]){
   cost[next]=g;parent[next]=id;heap.push({g+h(next),g,next});}};
  for(int k=0;k<8;k++){int nx=x+dx[k],ny=y+dy[k];if(nx<0||ny<0||nx>=n||ny>=n)continue;
   int next=layer*plane+ny*n+nx;if(blocked[next])continue;
   if(k>=4&&(blocked[layer*plane+y*n+nx]||blocked[layer*plane+ny*n+x]))continue;
   visit(next,k<4?10:14.142136);}
  if(!via[cell])for(int l=0;l<4;l++)if(l!=layer&&!blocked[l*plane+cell])visit(l*plane+cell,90);
 }
 return 0;
}
