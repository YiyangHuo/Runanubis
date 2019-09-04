#pragma once
#include "readofile.h"
#include "matchtime.h"
#include <experimental/filesystem> 
#include "tinyxml.h"
#include <stdio.h> 
#include <iostream> 
namespace fs = std::experimental::filesystem;
class Board {
public:
	Board(char**& argv);
	void runanubis();
	void getxtrs();
	void plot();

private:
	void getFileNames(std::string dir, bool isonfiles);
	void classifyTimes();
	void getInMatch(OFile thefile);
	void writeXmlFiles();
	string fileNameStr(char filetype, Matches &currentmatch);
	string to2DigitStr(int num);
	string getNewTime(Matches &currentmatch, bool iso);
	string _path;
	string _xmlfilename;
	string _excufilename;
	string _plotfilename;
	vector<string> _ofilenames;
	vector<string> _xtrfilenames;
	vector<string> _nfilenames;
	vector<Matches> _matches;
	vector<string> _newconfnames;

};