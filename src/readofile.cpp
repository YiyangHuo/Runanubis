#include "readofile.h"

OFile::OFile(string& filename)
{
	fstream f(filename);
	string line;
	_filename = filename;
	while (getline(f, line)) {
		int pos = line.find("TIME");
		if (pos != line.npos) {
			string temp = "";
			for (int i = 0; i < line.length(); i++) {
				if (line[i] != ' ' && _timespan.size() < 7) {
					temp.push_back(line[i]);
				}
				else if (!temp._Equal("")) {
					_timespan.push_back(stoi(temp));
					temp = "";
				}
			}
		}
	}
}

vector<int> OFile::gettimespan()
{
	return _timespan;
}

string OFile::getfilename()
{
	return _filename;
}



//时间信息以整数记录，可以用这个找到结束时间
