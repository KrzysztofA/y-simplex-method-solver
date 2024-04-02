﻿#include "y-simplex-method-solver.hpp"

int main()
{
  yasuzume::simplex::Simplex simplex_maximization_1 {};
  simplex_maximization_1.set_function( { 40, 30, 1 } );
  simplex_maximization_1.add_constraint( { 1, 1, 12 } );
  simplex_maximization_1.add_constraint( { 2, 1, 16 } );
  simplex_maximization_1.build( yasuzume::simplex::ProblemType::Maximization );
  simplex_maximization_1.compute_solution();

  for( const auto& i : simplex_maximization_1.get_solution() )
  {
    std::cout << i << " ";
  }
  std::cout << "\n";

  yasuzume::simplex::Simplex simplex_maximization_2 {};
  simplex_maximization_2.set_function( { 1, 2, 3, 1 } );
  simplex_maximization_2.add_constraint( { 1, 1, 1, 12 } );
  simplex_maximization_2.add_constraint( { 2, 1, 3, 18 } );
  simplex_maximization_2.build( yasuzume::simplex::ProblemType::Maximization );
  simplex_maximization_2.compute_solution();

  for( const auto& i : simplex_maximization_2.get_solution() ) std::cout << i << " ";
  std::cout << "\n";

  yasuzume::simplex::Simplex simplex_maximization_3 {};
  simplex_maximization_3.set_function( { 1, 2, 1, 1 } );
  simplex_maximization_3.add_constraint( { 1, 1, 3 } );
  simplex_maximization_3.add_constraint( { 0, 1, 1, 4 } );
  simplex_maximization_3.add_constraint( { 1, 0, 1, 5 } );
  simplex_maximization_3.build( yasuzume::simplex::ProblemType::Maximization );
  simplex_maximization_3.compute_solution();

  for( const auto& i : simplex_maximization_3.get_solution() )
  {
    std::cout << i << " ";
  }
  std::cout << "\n";

  yasuzume::simplex::Simplex simplex_minimization_1 {};
  simplex_minimization_1.set_function( { 12, 16, 1 } );
  simplex_minimization_1.add_constraint( { 1, 2, 40 } );
  simplex_minimization_1.add_constraint( { 1, 1, 30 } );
  simplex_minimization_1.build( yasuzume::simplex::ProblemType::Minimization );
  simplex_minimization_1.compute_solution();

  for( const auto& i : simplex_minimization_1.get_solution() )
  {
    std::cout << i << " ";
  }
  std::cout << "\n";

  yasuzume::simplex::Simplex simplex_minimization_2 {};
  simplex_minimization_2.set_function( { 6, 8, 1 } );
  simplex_minimization_2.add_constraint( { 2, 3, 7 } );
  simplex_minimization_2.add_constraint( { 4, 5, 9 } );
  simplex_minimization_2.build( yasuzume::simplex::ProblemType::Minimization );
  simplex_minimization_2.compute_solution();

  for( const auto& i : simplex_minimization_2.get_solution() )
  {
    std::cout << i << " ";
  }
  std::cout << "\n";

  yasuzume::simplex::Simplex simplex_minimization_3 {};
  simplex_minimization_3.set_function( { 5, 6, 7, 1 } );
  simplex_minimization_3.add_constraint( { 3, 2, 3, 10 } );
  simplex_minimization_3.add_constraint( { 4, 3, 5, 12 } );
  simplex_minimization_3.build( yasuzume::simplex::ProblemType::Minimization );
  simplex_minimization_3.compute_solution();

  for( const auto& i : simplex_minimization_3.get_solution() ) std::cout << i << " ";
  std::cout << "\n";

  yasuzume::simplex::Simplex simplex_minimization_4 {};
  simplex_minimization_3.set_function( { 4, 3, 1 } );
  simplex_minimization_3.add_constraint( { 1, 1, 10 } );
  simplex_minimization_3.add_constraint( { 3, 2, 24 } );
  simplex_minimization_3.build( yasuzume::simplex::ProblemType::Minimization );
  simplex_minimization_3.compute_solution();

  for( const auto& i : simplex_minimization_3.get_solution() ) std::cout << i << " ";
  std::cout << "\n";

  return 0;
}
