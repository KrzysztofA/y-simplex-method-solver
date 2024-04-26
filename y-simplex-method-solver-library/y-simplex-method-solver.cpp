#include "y-simplex-method-solver.hpp"
#include <strtk.hpp>

std::vector<yasuzume::math::Fraction> convert_string_to_fraction_vector( const std::string& );

int main( int _argc, char* _argv[] )
{
  /*
   * First argument is a query, if the query is to:
   * a) retrieve solution of maximization problem : -maxsol
   * b) retrieve solution of minimization problem -minsol
   * c) steps of maximization problem -maxsteps
   * d) steps of minimization problem -minsteps, 
  */

  // 2 argument is function formatted as "[x1, x2, ..., xn, z]"

  // Following arguments are constraints formatted as "[x1, x2, ..., xn, c]"
  const char* commands[ ] { "-help", "-maxsol", "-minsol", "-maxsteps", "-minsteps" };

  if( _argc < 2 )
  {
    std::cerr << "Wrong number of arguments\n";
    return 0;
  }

  if( std::strcmp( _argv[ 1 ], commands[ 0 ] ) == 0 ) std::cout << "First argument is a query, if the query is to:\na) retrieve solution of maximization problem : -maxsol\nb) retrieve solution of minimization problem -minsol\nc) steps of maximization problem -maxsteps\nd) steps of minimization problem -minsteps\n2 argument is function formatted as \"x1, x2, ..., xn, z\"\nFollowing arguments are constraints formatted as \"x1, x2, ..., xn, c\"\n";
  else if( std::strcmp( _argv[ 1 ], commands[ 1 ] ) == 0 )
  {
    if( _argc < 4 )
    {
      std::cerr << "Wrong number of arguments\n";
      return 0;
    }
    yasuzume::simplex::Simplex simplex_method {};
    simplex_method.set_function( convert_string_to_fraction_vector( _argv[ 2 ] ) );

    for( auto i { 3 }; i < _argc; i++ ) simplex_method.add_constraint( convert_string_to_fraction_vector( _argv[ i ] ) );
    simplex_method.build( yasuzume::simplex::ProblemType::Maximization );
    simplex_method.compute_solution();
    for( const auto sol = simplex_method.get_solution(); auto fraction : sol ) std::cout << fraction.to_string() << " ";
  }
  else if( std::strcmp( _argv[ 1 ], commands[ 2 ] ) == 0 )
  {
    if( _argc < 4 )
    {
      std::cerr << "Wrong number of arguments\n";
      return 0;
    }
    yasuzume::simplex::Simplex simplex_method {};
    simplex_method.set_function( convert_string_to_fraction_vector( _argv[ 2 ] ) );

    for( auto i { 3 }; i < _argc; i++ ) simplex_method.add_constraint( convert_string_to_fraction_vector( _argv[ i ] ) );
    simplex_method.build( yasuzume::simplex::ProblemType::Minimization );
    simplex_method.compute_solution();
    for( const auto sol = simplex_method.get_solution(); auto fraction : sol ) std::cout << fraction.to_string() << " ";
  }
  else if( std::strcmp( _argv[ 1 ], commands[ 3 ] ) == 0 )
  {
    if( _argc < 4 )
    {
      std::cerr << "Wrong number of arguments\n";
      return 0;
    }
    yasuzume::simplex::Simplex simplex_method {};
    simplex_method.set_function( convert_string_to_fraction_vector( _argv[ 2 ] ) );
    for( auto i { 3 }; i < _argc; i++ ) simplex_method.add_constraint( convert_string_to_fraction_vector( _argv[ i ] ) );
    simplex_method.build( yasuzume::simplex::ProblemType::Maximization );
    simplex_method.compute_solution();
    for( const auto& step : simplex_method.get_steps() ) std::cout << step.to_string() << "\n";
    for( const auto sol = simplex_method.get_solution(); auto fraction : sol ) std::cout << fraction.to_string() << " ";
  }
  else if( std::strcmp( _argv[ 1 ], commands[ 4 ] ) == 0 )
  {
    if( _argc < 4 )
    {
      std::cerr << "Wrong number of arguments\n";
      return 0;
    }
    yasuzume::simplex::Simplex simplex_method {};
    simplex_method.set_function( convert_string_to_fraction_vector( _argv[ 2 ] ) );
    for( auto i { 3 }; i < _argc; i++ ) simplex_method.add_constraint( convert_string_to_fraction_vector( _argv[ i ] ) );
    simplex_method.build( yasuzume::simplex::ProblemType::Minimization );
    simplex_method.compute_solution();
    for( const auto& step : simplex_method.get_steps() ) std::cout << step.to_string() << "\n";
    for( const auto sol = simplex_method.get_solution(); auto fraction : sol ) std::cout << fraction.to_string() << " ";
  }
  else std::cerr << "Invalid query, use -maxsol, -minsol, -maxsteps, -minsteps, -help\n";

  return 0;
}

std::vector<yasuzume::math::Fraction> convert_string_to_fraction_vector( const std::string& _input_string )
{
  std::vector<yasuzume::math::Fraction>                            return_vector {};
  strtk::std_string::token_list_type                               split_input;
  std::vector<std::string>                                         split_vector {};
  const strtk::single_delimiter_predicate predicate( ',' );
  split( predicate, _input_string, std::back_inserter( split_input ), strtk::split_options::compress_delimiters );
  for( const auto& key : split_input | std::views::keys ) split_vector.emplace_back( key );
  for( auto& i : split_vector )
  {
    if( i.contains( "/" ) )
    {
      strtk::std_string::token_list_type split_number {};
      std::vector<std::string>           number_vector {};
      for( const auto& key : split_input | std::views::keys ) split_vector.emplace_back( key );
      split( predicate, i, std::back_inserter( split_number ), strtk::split_options::compress_delimiters );
      return_vector.emplace_back( std::stoi( number_vector.at( 0 ) ), std::stoi( number_vector.at( 1 ) ) );
    }
    else return_vector.emplace_back( std::stoi( i ) );
  }
  return return_vector;
}