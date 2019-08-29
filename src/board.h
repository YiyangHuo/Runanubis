#pragma once
#include "readofile.h"
#include "matchtime.h"
#include <experimental/filesystem> 
namespace fs = std::experimental::filesystem;
class Board {
public:
	Board(char**& argv);
	void runanubis();
	void getxtrs();
	void plot();

private:
	void getFileNames(const std::string dir, std::string ending);
	void classifytimes();
	void getinmatch(OFile thefile);
	string _xmlfilename;
	string _excufilename;
	string _plotfilename;
	vector<string> _ofilenames;
	vector<string> _xtrfilenames;
	vector<string> _nfilenames;
	vector<Matches> _matches;

};