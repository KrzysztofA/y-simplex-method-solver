cmake_minimum_required (VERSION 3.28)

# Enable Hot Reload for MSVC compilers if supported.
if (POLICY CMP0141)
  cmake_policy(SET CMP0141 NEW)
  set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>")
endif()

project ("y-simplex-method-solver" VERSION 0.0.5)

set(INCLUDEDIR "D:/Libraries/Include")
set(LIBDIR "D:/Libraries/Lib")
set(BINDIR "D:/Libraries/bin")

include(GNUInstallDirs)
include(${LIBDIR}/cmake/y-mathematics-library/y-mathematics-library.cmake)

include_directories(${INCLUDE_DIR})

SET(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)

# Add source to this project's dynamic library.
add_library (y-simplex-method-solver SHARED
			"Headers/Simplex.hpp"		
			"Headers/ProblemType.inl"
			"Source/Simplex.cpp"
)

# Add source to this project's executable.
add_executable (y-simplex-method-solver-executable 
				"y-simplex-method-solver.cpp" 
				"y-simplex-method-solver.hpp"
				"Headers/Simplex.hpp"		
				"Headers/ProblemType.inl"
				"Source/Simplex.cpp"
)

include_directories("Headers")

include(GenerateExportHeader)

target_link_libraries(y-simplex-method-solver-executable PUBLIC Y::y-mathematics-library)
target_link_libraries(y-simplex-method-solver PUBLIC Y::y-mathematics-library)

set_property(TARGET y-simplex-method-solver PROPERTY CXX_STANDARD 26)
set_property(TARGET y-simplex-method-solver-executable PROPERTY CXX_STANDARD 26)
set(CMAKE_CXX_STANDARD_REQUIRED ON)