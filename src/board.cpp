#include "board.h"

Board::Board(char**& argv):_xmlfilename(argv[1]),_excufilename(argv[2]),_plotfilename(argv[3]){
	std::string argv_str(argv[0]);
	getFileNames(argv_str, ".o");
	getFileNames(argv_str, ".n");
	classifytimes();
}

void Board::runanubis()
{

}
void Board::getFileNames(std::string dir, std::string ending)
{
	for (const auto& entry : fs::directory_iterator(dir)) {
		string fileName = entry.path().filename().string();
		int pos = fileName.rfind(".");
		string end = string(fileName, pos, fileName.size());
		if (end._Equal(ending)) {
			if (ending._Equal(".o")) {
				_ofilenames.push_back(fileName);
			}
			else if (ending._Equal(".xtr")) {
				_xtrfilenames.push_back(fileName);
			}
			else if (ending._Equal(".xtr")) {
				_nfilenames.push_back(fileName);
			}
		}
	}
}
void Board::classifytimes(){
	for (string filename : _ofilenames) {
		OFile thefile = OFile(filename);
		getinmatch(thefile);
	}
}

void Board::getinmatch(OFile thefile)
{
	for (Matches match : _matches) {
		if (match.equals(thefile.gettimespan())) {
			match.addname(thefile.getfilename());
			return;	
		}
	}
	vector<string> newmatch;
	newmatch.push_back(thefile.getfilename());
	_matches.push_back(Matches(newmatch, thefile.gettimespan()));
	return;
}
