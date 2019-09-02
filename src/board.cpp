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
		TiXmlDocument* theconf = new TiXmlDocument(confpath.c_str());
		bool loadsuccess = theconf->LoadFile();
		if (!loadsuccess) {
			std::cout << "cannot load conf file, please check your argument input" << std::endl;
			exit(1);
		}
		string newconfname = _xmlfilename + to_string(numf+1);
		_newconfnames.push_back(newconfname);
		TiXmlElement* RootElement = theconf->RootElement();
		TiXmlElement* beg = RootElement->FirstChildElement("gen")->FirstChildElement("beg");
		TiXmlNode* oldbeg = beg->FirstChild();
		string thenew = getnewtext(_matches[numf]);
		TiXmlText newText(thenew.c_str());
		beg->ReplaceChild(oldbeg, newText);
		// insert successfull, make it a comment: std::cout << beg->GetText(); 
		theconf->SaveFile(newconfname.c_str());
		//这个地方会把双引号转义，但是没有关系，anubis还是会照样读

		
	}

}

string Board::to2digitstr(int num)
{
	string tmp;
	if (num < 10) {
		tmp += "0";
	}
	tmp += to_string(num);
	return tmp;
}

string Board::getnewtext(Matches &currentmatch)
{
	string output ="";
	vector<int> timespan = currentmatch.gettimespan();
	output += '"' + to_string(timespan[0]) + "-" + to2digitstr(timespan[1]) + "-" + to2digitstr(timespan[2]) + " " + to2digitstr(timespan[3]) + ":" + to2digitstr(timespan[4]) + ":" + to2digitstr(timespan[5]) + '"';
	return output;
}
