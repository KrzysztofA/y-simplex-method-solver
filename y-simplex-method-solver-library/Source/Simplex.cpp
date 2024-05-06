#include <cassert>
#include <Simplex.hpp>

#include <Enumerator.inl>
#include <sstream>
#include <string>

namespace yasuzume::simplex
{
  using namespace yasuzume::math;

  void Simplex::add_constraint( const std::initializer_list<Fraction> _list )
  {
    assert( !built );
    matrix_representation.append_row<std::initializer_list<Fraction>>( _list.begin(), _list.end() - 1, true );
    constraints_number++;
    variables_number = std::max( std::ssize( _list ), variables_number );
    result_column.emplace_back( *( _list.end() - 1 ) );
  }

  void Simplex::set_function( const std::initializer_list<Fraction> _list )
  {
    assert( !built );
    function = _list;
    function.pop_back();
    variables_number = std::max( std::ssize( _list ), variables_number );
    for( auto& f : function )
    {
      f /= *( _list.end() - 1 );
    }
  }

  void Simplex::add_constraint( std::vector<Fraction> _list )
  {
    assert( !built );
    matrix_representation.append_row<std::vector<Fraction>>( _list.begin(), _list.end() - 1, true );
    constraints_number++;
    variables_number = std::max( std::ssize( _list ), variables_number );
    result_column.emplace_back( *( _list.end() - 1 ) );
  }

  void Simplex::set_function( const std::vector<Fraction>& _list )
  {
    assert( !built );
    function = _list;
    function.pop_back();
    variables_number = std::max( std::ssize( _list ), variables_number );
    for( auto& f : function )
    {
      f /= *( _list.end() - 1 );
    }
  }

  void Simplex::build( const ProblemType _problem )
  {
    assert( !built );
    problem_type = _problem;
    if( problem_type == ProblemType::Minimization )
    {
      matrix_representation = matrix_representation.transpose();
      std::swap( result_column, function );
    }

    while( result_column.size() < function.size() ) result_column.emplace_back( 0 );
    for( auto& f : function ) f *= -1;

    matrix_representation.append_row<std::vector<Fraction>>( function.begin(), function.end(), true );
    matrix_representation.append_to_column_end( DMatrix<Fraction>::identity( constraints_number + 1 ), true );
    matrix_representation.append_column<std::vector<Fraction>>( result_column.begin(), result_column.end(), true );
    built = true;
  }

  void Simplex::next()
  {
    assert( built );
    if( non_feasible ) return;
    if( cache_steps ) steps.emplace_back( matrix_representation );

    std::stringstream string_stream {};

    // Identify most negative entry in the bottom row

    const auto sorted { matrix_representation.get_sorted_row_indexes( matrix_representation.column_size() - 1 ) };
    const auto pivot_x { sorted[ 0 ].index };

    // Find quotient

    // Get the column of the index but the last
    const auto last_column { matrix_representation.column( matrix_representation.row_size() - 1 ) };
    const auto index_column { matrix_representation.column( pivot_x ) };

    // Find Pivot by sorting the candidates

    std::vector<Fraction> candidates {};
    for( auto i { 0 }; i < std::ssize( index_column ) - 1; i++ ) candidates.emplace_back( index_column[ i ] != 0 ? last_column[ i ] / index_column[ i ] : 0 );
    auto                                                                      enumerated_candidates { enumerate<Fraction>( candidates ) };
    std::erase_if( enumerated_candidates, []( const Enumerator<Fraction>& _item ) { return _item.value <= 0; } );
    if( enumerated_candidates.empty() )
    {
      non_feasible = true;
      return;
    }
    std::ranges::sort( enumerated_candidates, []( const Enumerator<Fraction>& _item, const Enumerator<Fraction>& _item_2 ) { return _item.value < _item_2.value; } );
    const auto                                                                pivot_y { enumerated_candidates[ 0 ].index };

    // Apply row operation

    // Make pivot entry 1
    if( cache_operation_text ) string_stream << "{\nRow" << pivot_y + 1 << " = " << "Row" << pivot_y + 1 << "/(" << matrix_representation.at( pivot_x, pivot_y ) << ")\n";
    matrix_representation.row_operation_scale( pivot_y, Divide, matrix_representation.at( pivot_x, pivot_y ) );


    // Subtract pivot row from all other rows to get 0 in columns but pivot
    for( size_t x { 0 }; x < matrix_representation.column_size(); x++ )
    {
      if( x == pivot_y ) continue;
      if( cache_operation_text ) string_stream << "Row" << x + 1 << " = " << "Row" << x + 1 << " - " << "Row" << pivot_y + 1 << " * " << matrix_representation.at( pivot_x, x ) << "\n";
      matrix_representation.row_operation( x, Subtract, pivot_y, matrix_representation.at( pivot_x, x ) );
    }

    if( cache_operation_text )
    {
      string_stream << "}";
      operations.emplace_back( string_stream.str() );
    }

    // Check if constrains are satisfied
    solved = check_if_solved();

    if( !solved && steps.size() % 6 == 0 && check_if_looping() ) non_feasible = true;
  }

  void Simplex::compute_solution()
  {
    assert( built );
    while( !solved )
    {
      next();
      if( non_feasible ) return;
    }
    if( cache_steps ) steps.emplace_back( matrix_representation );
    cache_solution();
  }

  void Simplex::cache_solution()
  {
    assert( solved );
    if( non_feasible ) return;
    solution = problem_type == ProblemType::Maximization ? get_maximization_solution() : get_minimization_solution();
  }

  void Simplex::set_cache_steps( const bool& _cache_steps )
  {
    cache_steps = _cache_steps;
  }

  void Simplex::set_cache_operation_text( const bool& _cache_operation_text )
  {
    cache_operation_text = _cache_operation_text;
  }

  std::vector<Fraction> Simplex::get_maximization_solution() const
  {
    assert( solved && problem_type == ProblemType::Maximization );
    std::vector<Fraction> return_vector {};
    const auto temp { matrix_representation.column( matrix_representation.row_size() - 1 ) };
    return_vector.resize( variables_number, 0 );
    for( auto i { 0 }; i < variables_number; i++ )
    {
      const auto temp_column { matrix_representation.column( i ) };
      auto index { -1 };
      auto all_zero { true };
      for( auto j { 0 }; j < std::ssize( temp_column ); ++j )
      {
        // Find 1 index and if all others are 0
        if( temp_column.at( j ) == 1 && index == -1 ) index = j;
        else if( temp_column.at( j ) != 0 )
        {
          all_zero = false;
          break;
        }
      }
      if( all_zero && index != -1 ) return_vector.at( i ) = temp.at( index );
    }
    return_vector.at( return_vector.size() - 1 ) = temp.at( temp.size() - 1 );
    return return_vector;
  }

  std::vector<Fraction> Simplex::get_minimization_solution() const
  {
    assert( solved && problem_type == ProblemType::Minimization );
    std::vector<Fraction> return_vector {};
    const auto temp { matrix_representation.column( matrix_representation.row_size() - 1 ) };
    return_vector.resize( variables_number, 0 );
    for( long long i { constraints_number }, k { 0 }; i < constraints_number * 2; i++, k++ ) return_vector.at( k ) = matrix_representation.column( i ).at( matrix_representation.column_size() - 1 );
    return_vector.at( return_vector.size() - 1 ) = temp.at( temp.size() - 1 );
    return return_vector;
  }

  std::vector<Fraction> Simplex::get_solution() const
  {
    assert( solved );
    if( non_feasible ) return { 0 };
    return solution;
  }

  std::string Simplex::to_string() const
  {
    return matrix_representation.to_string();
  }

  std::vector<DMatrix<Fraction>> Simplex::get_steps() const
  {
    return steps;
  }

  std::vector<std::string> Simplex::get_steps_operation_text() const
  {
    return operations;
  }

  bool Simplex::check_if_looping() const
  {
    for( const auto& i : steps )
    {
      auto equal { true };
      auto k { matrix_representation.at( matrix_representation.column_size() - 1 ).begin() };
      for( auto j : i.at( i.column_size() - 1 ) )
      {
        equal = equal && *k == j;
        ++k;
      }
      if( equal ) return true;
    }
    return false;
  }

  bool Simplex::check_if_solved() const
  {
    return !std::ranges::any_of( matrix_representation.at( matrix_representation.column_size() - 1 ), []( const Fraction& _i ) { return _i < 0; } );
  }
}
