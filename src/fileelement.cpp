#include"fileelement.h"


Fileelement::Fileelement(vector<string>& names, vector<int>& timespan): _filenames(names), _timespan(timespan)
{
}

vector<string> Fileelement::getnames(){
	return _filenames;
}

vector<int> Fileelement::gettimespan() {
	return _timespan;
}