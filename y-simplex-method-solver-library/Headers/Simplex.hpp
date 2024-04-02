#pragma once

#include <DMatrix.inl>

#include <vector>

#include <Fraction.hpp>
#include <ProblemType.inl>
#include <string>

namespace yasuzume::simplex
{
  using namespace yasuzume::math;

  class Simplex
  {
  public:
    Simplex() = default;
    Simplex( const Simplex& ) = default;
    Simplex( Simplex&& ) noexcept = default;
    ~Simplex() noexcept = default;

    Simplex& operator=( const Simplex& ) = default;
    Simplex& operator=( Simplex&& ) noexcept = default;

    void add_constraint( std::initializer_list<Fraction> );
    void set_function( std::initializer_list<Fraction> );

    void build( ProblemType );
    void next();
    void compute_solution();

    [[nodiscard]] std::vector<Fraction> get_solution() const;
    [[nodiscard]] std::string           to_string() const;


  private:
    DMatrix<Fraction> matrix_representation {};

    std::vector<DMatrix<Fraction>> steps {};

    std::vector<Fraction> result_column {};
    std::vector<Fraction> function {};

    [[nodiscard]] bool check_if_looping() const;
    [[nodiscard]] bool check_if_solved() const;

    bool built { false };
    bool solved { false };
    bool non_feasible { false };
  };
}
