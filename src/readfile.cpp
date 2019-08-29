#include "readfile.h"

TheFile::TheFile(string& filename)
{
	TiXmlDocument* myDocument = new TiXmlDocument(filename.c_str());
}

vector<Fileelement> TheFile::getInfo()
{
	return _timeinfo;
}
//时间信息以整数记录，可以用这个找到结束时间
