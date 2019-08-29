// Runanubisandplot.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "tinyxml.h"
#include "board.h"

int main(int argc, char** argv)
{
	std::cout << "Please make sure that your config, datas and excutable Anubis file are in the same directory" << std::endl;
	if (argc < 4) {
		std::cout << "wrong input. please input as [config file name] [Anubis excutable name] [skyplot excutable name]"<<std::endl;
	}
	Board theboard(argv);
	theboard.runanubis();
	theboard.getxtrs();
	theboard.plot(); 
	string firststr = argv[2];
	firststr += " -x ";
	firststr += argv[1];
	const char* ha = firststr.c_str();
	system(ha);
	string nextstr = "python2 anubisplot.py +skyplot ABMF180010.xtr";
	const char* da = nextstr.c_str();
	system(da);
	return 0;
}



// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
