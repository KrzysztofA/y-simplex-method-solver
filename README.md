<!--
{
  "meta":
  {
    "type": "PCSoftware",
    "ready": true,
    "version": "0.4.8",
    "main":
    [
      "Python",
      "CPP"
    ],
    "tags":
    [
      "PyQt6", 
      "API",
      "Subprocess",
      "Mathematics",
      "GUI",
      "Optimization",
      "Simplex",
      "Algorithms",
      "Education",
      "FullStack"
    ],
    "satisfaction": "8",
    "difficulty": "7",
    "challange": "7",
    "complexity": "8"
  }
}
-->

# y-simplex-method-solver v0.4.8 (Windows)

## Simplex Method Mathematical Software with C++ API and Python GUI

Project levereges speed of C++ with Python GUI, using subprocess communication to solve problems of constrained minimization/maximization with Simplex Method and passing the solution along with working out to the user. The user is then able to export the data in desired format.

## Stack

- C++23
- CMake #**3.28**
- Python #**3.12**
- PyQt6 #**6.7.0**
- Pypandoc #**1.13**

## Background

The idea for the software originated with my Mathematics final exam, where I had to plot the Simplex Method in a document to then send it off. The process was long, and even programming the method in Matlab was mundane.

Exploring different Simplex Method Solvers online I noticed that there is not a single one that would present the working out and solution in readable format that would be used in mathematics textbooks. The idea was to create a simplex method solver that would execute tasks quickly, allow for use in education, and present the data in a way that would be similar to the one seen in textbooks.

I started developing the program, to find out it is not an easy task for me back then, when I was also exhausted with working on my Master's degree. Which caused the project to be quickly dropped. Now, a year later, I decided to start the program from scratch, to see that with my current abilities it is achievable to complete it.

I decided to build small mathematics library to let me work with fractions, mathematically correct matrices and simplex method backend in C++. For front-end GUI I decided to use PyQt6 as a robust and fast GUI library, being able to compromise between the speed and simplicity.

## Features

- Solving Maximization/Minimization problems with Simplex Method
- C++ API to receive solution output
- Intuitive User Interface with Python
- Exporting Data to Html/Docx/Pdf
- Saving data in yse format to be able to return to working on the equation
- Customizable output

More coming...

## Simplex Method

Couple of links explaining what the simplex method is and how to work with it:

https://en.wikipedia.org/wiki/Simplex_algorithm
https://math.libretexts.org/Bookshelves/Applied_Mathematics/Applied_Finite_Mathematics_(Sekhon_and_Bloom)/04%3A_Linear_Programming_The_Simplex_Method

## Final Words

This is a first Readme, I plan on adding more to it and support the software for some time.
The project is one of the bigger ones I indenpendently worked on - I plan on expanding it's functionality. I am grateful for every single person reading it and even more grateful for every single person that will use the program. Feel free to contact me with any feature request or question.