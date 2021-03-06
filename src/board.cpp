#include "board.h"

Board::Board(char**& argv):_xmlfilename(argv[1]),_excufilename(argv[2]),_plotfilename(argv[3]){
	char buffer[100];
	_getcwd(buffer,100);
	string argv_str = buffer;
	_path = argv_str;
	//std::cout << _path;
	getFileNames(argv_str, true);
	classifyTimes();
	//std::cout << _matches[0].gettimespan()[0] << _matches[1].gettimespan()[0];
}

void Board::runanubis()
{
	writeXmlFiles();
	for (int num = 0; num < _newconfnames.size(); num++) {
		string runcommandline = _excufilename + " " + "-x " + _newconfnames[num];
		system(runcommandline.c_str());
	}//call cmd and run
}
void Board::getxtrs()

{
	getFileNames(_path, false);
}
void Board::plot()
{
	for (int num = 0; num < _xtrfilenames.size(); num++) {
		string plotcommandline = "python2 " + _plotfilename + " +skyplot " + _xtrfilenames[num];
		system(plotcommandline.c_str());
	}
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
	for (int i = 0; i < _matches.size();i++) {
		if (_matches[i].equals(thefile.gettimespan())) {
			_matches[i].addname(thefile.getfilename());
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
		string thenew = getNewTime(_matches[numf],true);
		TiXmlText newbeg(thenew.c_str());
		beg->ReplaceChild(oldbeg, newbeg);
		TiXmlElement* end = RootElement->FirstChildElement("gen")->FirstChildElement("end");
		TiXmlNode* oldend = end->FirstChild();
		string thenewend = getNewTime(_matches[numf], false);
		TiXmlText newend(thenewend.c_str());
		end->ReplaceChild(oldend, newend);

		// insert successfull, make it a comment: std::cout << beg->GetText(); 
		TiXmlElement* rinexo = RootElement->FirstChildElement("inputs")->FirstChildElement("rinexo");
		TiXmlElement* rinexn = RootElement->FirstChildElement("inputs")->FirstChildElement("rinexn");
		TiXmlNode* oldo = rinexo->FirstChild();
		TiXmlNode* oldn = rinexn->FirstChild();
		string newo = fileNameStr('o', _matches[numf]);
		string newn = fileNameStr('n', _matches[numf]);
		TiXmlText newoText(newo.c_str());
		TiXmlText newnText(newn.c_str());
		rinexo->ReplaceChild(oldo, newoText);
		rinexn->ReplaceChild(oldn, newnText);// change the input file name
		TiXmlElement* log = RootElement->FirstChildElement("outputs")->FirstChildElement("log");
		TiXmlNode* oldlog = log->FirstChild();
		string newlog = log->GetText() + to_string(numf+1);
		TiXmlText newlogText(newlog.c_str());
		log->ReplaceChild(oldlog, newlogText);
		//successfully get the value :cout << oldo->Value() << "\ ";
		TiXmlElement* outxtr = RootElement->FirstChildElement("outputs")->FirstChildElement("xtr");
		TiXmlNode* oldxtr = outxtr->FirstChild();
		string filename = _matches[numf].getnames()[0];
		string newxtr = "$(rec)" + filename.substr(filename.size() - 3, 2) + filename.substr(filename.size() - 8, 4) + ".xtr";
		TiXmlText newxtrText(newxtr.c_str());
		outxtr->ReplaceChild(oldxtr, newxtrText);

		TiXmlElement* outxqc = RootElement->FirstChildElement("outputs")->FirstChildElement("xml");
		TiXmlNode* oldxqc = outxqc->FirstChild();
		string newxqc = "$(rec)" + filename.substr(filename.size() - 3, 2) + filename.substr(filename.size() - 8, 4) + ".xqc";
		TiXmlText newxqcText(newxqc.c_str());
		outxqc->ReplaceChild(oldxqc, newxqcText);
		theconf->SaveFile(newconfname.c_str());
		delete theconf;
		//这个地方会把双引号转义，但是没有关系，anubis还是会照样读
		//还忘了把同类时间的文件对conf进行修改
		
	}

}

string Board::fileNameStr(char filetype, Matches& currentmatch)
{	
	string rtr;
	if (filetype == 'o') {
		for (int i = 0; i < currentmatch.getnames().size(); i++) {
			rtr += currentmatch.getnames()[i] + " ";
		}
	}
	else if (filetype == 'n') {
		for (int i = 0; i < currentmatch.getnames().size(); i++) {
			string nname = currentmatch.getnames()[i];
			nname = nname.substr(0, nname.size() - 1) + 'n' + " ";
			rtr += nname;
		}
	}
	return rtr;
}

string Board::to2DigitStr(int num)
{
	string tmp;
	if (num < 10) {
		tmp += "0";
	}
	tmp += to_string(num);
	return tmp;
}

string Board::getNewTime(Matches &currentmatch, bool iso)
{
	string output ="";
	vector<int> timespan = currentmatch.gettimespan();
	if (iso) {
		output += '"' + to_string(timespan[0]) + "-" + to2DigitStr(timespan[1]) + "-" + to2DigitStr(timespan[2]) + " " + to2DigitStr(timespan[3]) + ":" + to2DigitStr(timespan[4]) + ":" + to2DigitStr(timespan[5]) + '"';
	}
	else
	{
		output += '"' + to_string(timespan[0]) + "-" + to2DigitStr(timespan[1]) + "-" + to2DigitStr(timespan[2]+1) + " " + to2DigitStr(timespan[3]) + ":" + to2DigitStr(timespan[4]) + ":" + to2DigitStr(timespan[5]) + '"';
	}
	return output;
}
