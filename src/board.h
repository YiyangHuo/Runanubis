#pragma once
#include "readfile.h"

class Board {
public:
	Board(char**& argv);
	void runanubis();
	void getxtrs();
	void plot();
private:
	string _xmlfilename;
	string _excufilename;
	string _plotfilename;
	vector<string> _ofilenames;
	vector<string> _xtrfilenames;

};