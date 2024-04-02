#include <cassert>
#include <Simplex.hpp>

#include <Enumerator.inl>
#include <string>

namespace yasuzume::simplex
{
  using namespace yasuzume::math;

  void Simplex::add_constraint( const std::initializer_list<Fraction> _list )
  {
    assert( !built );
    matrix_representation.append_row<std::initializer_list<Fraction>>( _list.begin(), _list.end() - 1, true );
    result_column.emplace_back( *( _list.end() - 1 ) );
  }

  void Simplex::set_function( const std::initializer_list<Fraction> _list )
  {
    assert( !built );
    function = _list;
    function.pop_back();
    for( auto& f : function )
    {
      f /= *( _list.end() - 1 );
    }
  }

  void Simplex::build( const ProblemType _problem )
  {
    assert( !built );
    if( _problem == ProblemType::Minimization )
    {
      matrix_representation = matrix_representation.transpose();
      std::swap( result_column, function );
    }
    std::cout << matrix_representation.to_string();
    for( auto i : result_column ) std::cout << i << " ";
    std::cout << "\n";
    for( auto i : function ) std::cout << i << " ";
    std::cout << "\n";
    for( auto& f : function ) f *= -1;
    matrix_representation.append_row<std::vector<Fraction>>( function.begin(), function.end(), true );
    matrix_representation.append_to_column_end( DMatrix<Fraction>::identity( matrix_representation.column_size() ), true );
    matrix_representation.append_column<std::vector<Fraction>>( result_column.begin(), result_column.end(), true );
    built = true;
    std::cout << matrix_representation.to_string();
  }

  void Simplex::next()
  {
    assert( built );
    if( non_feasible ) return;
    steps.emplace_back( matrix_representation );

    // Identify most negative entry in the bottom row

    const auto sorted { matrix_representation.get_sorted_row_indexes( matrix_representation.column_size() - 1 ) };
    const auto pivot_x { sorted[ 0 ].index };

    // Find quotient

    // Get the column of the index but the last
    const auto last_column { matrix_representation.column( matrix_representation.row_size() - 1 ) };
    const auto index_column { matrix_representation.column( pivot_x ) };

    // Find Pivot

    std::vector<Fraction> candidates {};
    for( auto i { 0 }; i < std::ssize( index_column ) - 1; i++ ) candidates.emplace_back( last_column[ i ] / index_column[ i ] );
    auto                                                                      enumerated_candidates { enumerate<Fraction>( candidates ) };
    std::ranges::sort( enumerated_candidates, []( const Enumerator<Fraction>& _item, const Enumerator<Fraction>& _item_2 ) { return _item.value < _item_2.value; } );
    const auto                                                                pivot_y { enumerated_candidates[ 0 ].index };

    // Apply row operation

    // Make pivot entry 1
    matrix_representation.row_operation_scale( pivot_y, Divide, matrix_representation.at( pivot_x, pivot_y ) );

    // Subtract pivot row from all other rows to get 0 in columns but pivot
    for( size_t x { 0 }; x < matrix_representation.column_size(); x++ )
    {
      if( x == pivot_y ) continue;
      matrix_representation.row_operation( x, Subtract, pivot_y, matrix_representation.at( pivot_x, x ) );
    }

    // std::cout << "\n" << matrix_representation.to_string() << "\n";

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
      if( non_feasible ) break;
    }
  }

  std::vector<Fraction> Simplex::get_solution() const
  {
    assert( solved );
    if( non_feasible ) return { 0 };
    const auto temp { matrix_representation.column( matrix_representation.row_size() - 1 ) };
    std::vector<Fraction> return_vector {};
    return_vector.resize( std::size( temp ), 0 );
    for( auto i { 0 }; i < std::ssize( temp ); i++ )
    {
      auto temp_column { matrix_representation.column( i ) };
      auto index { -1 };
      auto all_zero { true };
      for( auto j { 0 }; j < std::ssize( temp_column ); ++j )
      {
        // Find 1 index and if all others are 0
        if( temp_column.at( j ) == 1 && index == -1 ) index = j;
        else if( temp_column.at( j ) != 0 ) all_zero = false;
      }
      if( all_zero && index != -1 ) return_vector.at( i ) = temp.at( index );
    }

    return_vector.emplace_back( *( temp.end() - 1 ) );
    return return_vector;
  }

  std::string Simplex::to_string() const
  {
    return matrix_representation.to_string();
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
