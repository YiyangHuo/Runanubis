#include "board.h"

Board::Board(char**& argv):_xmlfilename(argv[1]),_excufilename(argv[2]),_plotfilename(argv[3]){
	std::string argv_str(argv[0]);
	for (int index = argv_str.size() - 1; index >= 0; index--) {
		if (argv_str[index] == '\\') {
			argv_str = argv_str.substr(0, index);
			break;
		}
	}
	_path = argv_str;
	getFileNames(argv_str, true);
	classifyTimes();
}

void Board::runanubis()
{
	writeXmlFiles();
}
void Board::getxtrs()
{
}
void Board::plot()
{
}
void Board::getFileNames(std::string dir, bool isonfiles)
{
	for (const auto& entry : fs::directory_iterator(dir)) {
		string fileName = entry.path().filename().string();
		int pos = fileName.rfind(".");
		
		if (pos == string::npos) continue;
		string end = string(fileName, pos, fileName.size());
		if (end.size() != 4) continue;
		
		if (isonfiles) {
			if (isdigit(end[1]) && isdigit(end[2])) {
				if (end[3] == 'o') {
					_ofilenames.push_back(fileName);
				}
				else if (end[3] == 'n') {
					_nfilenames.push_back(fileName);
				}
			}
		}
		else {
			if (end._Equal(".xtr")) {
				_xtrfilenames.push_back(fileName);
			}
		}
	}
}
void Board::classifyTimes(){
	for (string filename : _ofilenames) {
		OFile thefile = OFile(filename);
		getInMatch(thefile);
	}
}

void Board::getInMatch(OFile thefile)
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

void Board::writeXmlFiles()
{
	string confpath = _path +"\\"+ _xmlfilename;
	for (int numf = 0; numf < _matches.size(); numf++) {
		TiXmlDocument theconf(confpath.c_str());
		bool loadsuccess = theconf.LoadFile();
		if (!loadsuccess) {
			std::cout << "cannot load conf file, please check your argument input" << std::endl;
			exit(1);
		}
		string newconfname = _xmlfilename + to_string(numf+1);
		_newconfnames.push_back(newconfname);
		TiXmlElement* RootElement = theconf.RootElement();
		//std::cout << RootElement->Value(); successfull

		
	}

}
