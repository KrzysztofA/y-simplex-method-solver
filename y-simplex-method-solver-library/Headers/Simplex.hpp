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
    void add_constraint( std::vector<Fraction> );
    void set_function( const std::vector<Fraction>& );

    void build( ProblemType );
    void next();
    void compute_solution();
    void cache_solution();

    void set_cache_steps( const bool& );
    void set_cache_operation_text( const bool& );

    [[nodiscard]] std::vector<Fraction> get_solution() const;
    [[nodiscard]] std::string           to_string() const;
    [[nodiscard]] std::vector<DMatrix<Fraction>> get_steps() const;
    [[nodiscard]] std::vector<std::string> get_steps_operation_text() const;

  private:
    [[nodiscard]] std::vector<Fraction> get_maximization_solution() const;
    [[nodiscard]] std::vector<Fraction> get_minimization_solution() const;

    DMatrix<Fraction> matrix_representation {};

    std::vector<DMatrix<Fraction>> steps {};
    std::vector<std::string> operations {};

    std::vector<Fraction> result_column {};
    std::vector<Fraction> function {};

    [[nodiscard]] bool check_if_looping() const;
    [[nodiscard]] bool check_if_solved() const;

    bool built { false };
    bool solved { false };
    bool non_feasible { false };

    bool cache_steps { false };
    bool cache_operation_text { false };
    long long variables_number { 0 };
    long long constraints_number { 0 };
    ProblemType problem_type;
    std::vector<Fraction> solution {};
  };
}
