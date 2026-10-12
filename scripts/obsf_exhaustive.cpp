// All-ordered-splits OBS-F reference computation. No pruning or pivot restriction.
// Build: g++ -O3 -std=c++17 -march=native -fno-math-errno -fopenmp-simd \
//            scripts/obsf_exhaustive.cpp -o obsf_exhaustive
// Run: ./obsf_exhaustive 19 checks/obsf_19.csv
// Argument 19 means compute all N through 2^19 (the plotted phase level is 18).
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
int main(int argc, char** argv) {
 try {
  if (argc != 3) throw std::runtime_error("usage: obsf_exhaustive MAX_POWER OUTPUT.csv");
  const int k = std::stoi(argv[1]);
  if (k < 1 || k > 20) throw std::runtime_error("MAX_POWER must be 1..20");
  const std::size_t size = std::size_t(1) << k;
  const double p = std::log2(1.0 + std::sqrt(2.0));
  std::vector<double> U(size+1), W(size+1); U[1]=W[1]=1;
  const auto start=std::chrono::steady_clock::now();
  for (std::size_t N=2; N<=size; ++N) {
   const double u=U[N/2], v=U[(N+1)/2];
   U[N]=(u+v+std::sqrt(u*u+6*u*v+v*v))/2;
   double best=0.0;
   #pragma omp simd reduction(max:best)
   for (std::size_t m=1; m<N; ++m) {
    const double a=U[m], b=W[N-m];
    const double value=(4*a+b+std::sqrt(b*b+8*a*b))/2;
    best=std::max(best,value);
   }
   W[N]=best;
  }
  const double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::ofstream f(argv[2]); if (!f) throw std::runtime_error("cannot create output file");
  f<<"N,U_N,W_N,C_N\n"<<std::setprecision(17);
  for(std::size_t N=1;N<=size;++N) f<<N<<','<<U[N]<<','<<W[N]<<','<<std::pow(double(N),p)/W[N]<<'\n';
  if(!f) throw std::runtime_error("error writing output file");
  std::cerr<<std::setprecision(9)<<"maximum_N="<<size<<" candidates="<<std::uint64_t(size)*(size-1)/2
           <<" seconds="<<seconds<<"\n";
 } catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 1;}
}
