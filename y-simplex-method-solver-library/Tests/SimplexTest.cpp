#include "gtest/gtest.h"

#include <Fraction.hpp>

#include "Simplex.hpp"
#include "vector"

using namespace yasuzume;

TEST( TestSimplex, SolvingCorrectnessMaximization )
{
  simplex::Simplex simplex_maximization_1 {};
  simplex_maximization_1.set_function( { 40, 30, 1 } );
  simplex_maximization_1.add_constraint( { 1, 1, 12 } );
  simplex_maximization_1.add_constraint( { 2, 1, 16 } );
  simplex_maximization_1.build( simplex::ProblemType::Maximization );
  simplex_maximization_1.compute_solution();
  const std::vector<math::Fraction> vec1 { 4, 8, 400 };
  EXPECT_EQ( simplex_maximization_1.get_solution(), vec1 );

  simplex::Simplex simplex_maximization_2 {};
  simplex_maximization_2.set_function( { 1, 2, 3, 1 } );
  simplex_maximization_2.add_constraint( { 1, 1, 1, 12 } );
  simplex_maximization_2.add_constraint( { 2, 1, 3, 18 } );
  simplex_maximization_2.build( simplex::ProblemType::Maximization );
  simplex_maximization_2.compute_solution();
  const std::vector<math::Fraction> vec2 { 0, 9, 3, 27 };
  EXPECT_EQ( simplex_maximization_2.get_solution(), vec2 );

  simplex::Simplex simplex_maximization_3 {};
  simplex_maximization_3.set_function( { 1, 2, 1, 1 } );
  simplex_maximization_3.add_constraint( { 1, 1, 3 } );
  simplex_maximization_3.add_constraint( { 0, 1, 1, 4 } );
  simplex_maximization_3.add_constraint( { 1, 0, 1, 5 } );
  simplex_maximization_3.build( simplex::ProblemType::Maximization );
  simplex_maximization_3.compute_solution();
  const std::vector<math::Fraction> vec3 { 0, 3, 1, 7 };
  EXPECT_EQ( simplex_maximization_3.get_solution(), vec3 );
}

TEST( TestSimplex, MaximizationSpecialCases )
{
  simplex::Simplex simplex_maximization_1 {};
  simplex_maximization_1.set_function( { 0, 0, 1, } );
  simplex_maximization_1.add_constraint( { 20, 90, 15 } );
  simplex_maximization_1.add_constraint( { 60, 80, 40 } );
  simplex_maximization_1.build( simplex::ProblemType::Maximization );
  simplex_maximization_1.compute_solution();
  const std::vector<math::Fraction> vec1 { 0 };
  EXPECT_EQ( simplex_maximization_1.get_solution(), vec1 );

  simplex::Simplex simplex_maximization_2 {};
  simplex_maximization_2.set_function( { 100, 200, 1, } );
  simplex_maximization_2.add_constraint( { 0, 0, 0 } );
  simplex_maximization_2.add_constraint( { 0, 0, 0 } );
  simplex_maximization_2.build( simplex::ProblemType::Maximization );
  simplex_maximization_2.compute_solution();
  const std::vector<math::Fraction> vec2 { 0 };
  EXPECT_EQ( simplex_maximization_2.get_solution(), vec2 );

  simplex::Simplex simplex_maximization_3 {};
  simplex_maximization_3.set_function( { 0, 0, 1, } );
  simplex_maximization_3.add_constraint( { 0, 0, 0 } );
  simplex_maximization_3.add_constraint( { 0, 0, 0 } );
  simplex_maximization_3.build( simplex::ProblemType::Maximization );
  simplex_maximization_3.compute_solution();
  const std::vector<math::Fraction> vec3 { 0 };
  EXPECT_EQ( simplex_maximization_3.get_solution(), vec3 );

  simplex::Simplex simplex_maximization_4 {};
  simplex_maximization_4.set_function( { 12, 20, 1, } );
  simplex_maximization_4.add_constraint( { 0, 1, 12 } );
  simplex_maximization_4.add_constraint( { 1, 0, 41 } );
  simplex_maximization_4.build( simplex::ProblemType::Maximization );
  simplex_maximization_4.compute_solution();
  const std::vector<math::Fraction> vec4 { 41, 12, 732 };
  EXPECT_EQ( simplex_maximization_4.get_solution(), vec4 );
}

TEST( TestSimplex, SolvingCorrectnessMinimization )
{
  simplex::Simplex simplex_minimization_1 {};
  simplex_minimization_1.set_function( { 12, 16, 1 } );
  simplex_minimization_1.add_constraint( { 1, 2, 40 } );
  simplex_minimization_1.add_constraint( { 1, 1, 30 } );
  simplex_minimization_1.build( simplex::ProblemType::Minimization );
  simplex_minimization_1.compute_solution();
  const std::vector<math::Fraction> vec1 { 20, 10, 400 };
  EXPECT_EQ( simplex_minimization_1.get_solution(), vec1 );

  simplex::Simplex simplex_minimization_2 {};
  simplex_minimization_2.set_function( { 6, 8, 1 } );
  simplex_minimization_2.add_constraint( { 2, 3, 7 } );
  simplex_minimization_2.add_constraint( { 4, 5, 9 } );
  simplex_minimization_2.build( simplex::ProblemType::Minimization );
  simplex_minimization_2.compute_solution();
  const std::vector<math::Fraction> vec2 { 0, math::Fraction( 7, 3 ), math::Fraction( 56, 3 ) };
  EXPECT_EQ( simplex_minimization_2.get_solution(), vec2 );

  simplex::Simplex simplex_minimization_3 {};
  simplex_minimization_3.set_function( { 5, 6, 7, 1 } );
  simplex_minimization_3.add_constraint( { 3, 2, 3, 10 } );
  simplex_minimization_3.add_constraint( { 4, 3, 5, 12 } );
  simplex_minimization_3.build( simplex::ProblemType::Minimization );
  simplex_minimization_3.compute_solution();
  const std::vector<math::Fraction> vec3 { math::Fraction( 10, 3 ), 0, 0, math::Fraction( 50, 3 ) };
  EXPECT_EQ( simplex_minimization_3.get_solution(), vec3 );

  simplex::Simplex simplex_minimization_4 {};
  simplex_minimization_4.set_function( { 4, 3, 1 } );
  simplex_minimization_4.add_constraint( { 1, 1, 10 } );
  simplex_minimization_4.add_constraint( { 3, 2, 24 } );
  simplex_minimization_4.build( simplex::ProblemType::Minimization );
  simplex_minimization_4.compute_solution();
  const std::vector<math::Fraction> vec4 { 4, 6, 34 };
  EXPECT_EQ( simplex_minimization_4.get_solution(), vec4 );
}