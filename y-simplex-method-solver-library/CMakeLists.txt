cmake_minimum_required (VERSION 3.28)

# Enable Hot Reload for MSVC compilers if supported.
if (POLICY CMP0141)
  cmake_policy(SET CMP0141 NEW)
  set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>")
endif()

project ("y-simplex-method-solver" VERSION 0.0.7)

set(INCLUDEDIR $ENV{INCLDIR})
set(LIBDIR $ENV{LIBDIR})
set(BINDIR $ENV{BINDIR})

include(GNUInstallDirs)
include(${LIBDIR}/cmake/y-mathematics-library/y-mathematics-library.cmake)

find_path(STRTK_INCLUDE_DIRS "strtk.hpp")

include_directories(${INCLUDE_DIR})

SET(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)

# Add source to this project's dynamic library.
add_library (y-simplex-method-solver SHARED
			"Headers/Simplex.hpp"		
			"Headers/ProblemType.inl"
			"Source/Simplex.cpp"
			"y-simplex-method-solver.cpp" 
			"y-simplex-method-solver.hpp" 
)

# Add source to this project's executable.
add_executable (y-simplex-method-solver-executable 
				"y-simplex-method-solver.cpp" 
				"y-simplex-method-solver.hpp" 
)

add_executable(y-simplex-method-solver-tests 
			   "Tests/SimplexTest.cpp"
)	

enable_testing()

include_directories("Headers")
target_include_directories(y-simplex-method-solver-executable  PRIVATE ${STRTK_INCLUDE_DIRS})
target_include_directories(y-simplex-method-solver  PRIVATE ${STRTK_INCLUDE_DIRS})

include(GenerateExportHeader)

# Set the build shared libraries variable
option(BUILD_SHARED_LIBS "Build shared libraries" ON)

set(MY_HEADER_FILES "Headers/Simplex.hpp" "Headers/ProblemType.inl")

set_target_properties(y-simplex-method-solver
    PROPERTIES
    PUBLIC_HEADER "${MY_HEADER_FILES}"
)

install(TARGETS y-simplex-method-solver
        LIBRARY DESTINATION ${LIBDIR}
        PUBLIC_HEADER DESTINATION ${INCLUDEDIR}
)

find_package(GTest CONFIG REQUIRED)
include(GoogleTest)
gtest_discover_tests(y-simplex-method-solver-tests)

target_link_libraries(y-simplex-method-solver PUBLIC Y::y-mathematics-library)
target_link_libraries(y-simplex-method-solver-executable PUBLIC Y::y-mathematics-library PUBLIC y-simplex-method-solver)
target_link_libraries(y-simplex-method-solver-tests PRIVATE GTest::gtest GTest::gtest_main PRIVATE y-simplex-method-solver PRIVATE Y::y-mathematics-library)

set_property(TARGET y-simplex-method-solver PROPERTY CXX_STANDARD 26)
set_property(TARGET y-simplex-method-solver-executable PROPERTY CXX_STANDARD 26)
set_property(TARGET y-simplex-method-solver-tests PROPERTY CXX_STANDARD 26)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
